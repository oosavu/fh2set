#!/usr/bin/env python3
"""
Load Scala .scl/.kbm files into an Expert Sleepers FH-2 via MIDI SysEx.

SysEx (FH-2 manual, "Scala/MIDI Tuning Standard"):
    F0 00 21 27 2F 11 <slot> <.scl text> F7   install .scl
    F0 00 21 27 2F 12 <slot> <.kbm text> F7   install .kbm

Requires:  pip install mido python-rtmidi

Examples:
    python3 fh2_load.py --list                         # show MIDI outputs
    python3 fh2_load.py                                # load everything from manifest.tsv
    python3 fh2_load.py --only edo12,gam_malm         # load selected entries
    python3 fh2_load.py --dry-run                      # print what would be sent
    python3 fh2_load.py --syx out.syx                  # write one .syx file instead of sending
    python3 fh2_load.py --scl my.scl --kbm my.kbm --slot 20   # single ad-hoc pair

Slot numbers (manifest.tsv, --slot) are as shown on the FH-2 screen: 1..32.
SysEx byte = slot - 1 by default; use --sysex-base 1 if the module expects byte = slot.
"""
import argparse, os, sys, time, unicodedata

HDR = [0x00, 0x21, 0x27, 0x2F]
CMD = {'scl': 0x11, 'kbm': 0x12}
HERE = os.path.dirname(os.path.abspath(__file__))


def payload(path):
    """File text as 7-bit ASCII, LF line endings. Non-ASCII is transliterated or dropped."""
    raw = open(path, 'rb').read().decode('latin-1')
    txt = unicodedata.normalize('NFKD', raw).encode('ascii', 'ignore').decode('ascii')
    txt = txt.replace('\r\n', '\n').replace('\r', '\n')
    data = list(txt.encode('ascii'))
    assert all(b < 0x80 for b in data)
    return data


def build(kind, slot, path, base):
    if not 1 <= slot <= 32:
        sys.exit(f'slot {slot} out of range 1..32')
    return HDR + [CMD[kind], slot - 1 + base] + payload(path)   # mido adds F0/F7


def read_manifest(path):
    jobs = []
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        slot, name = line.split('\t')[:2]
        jobs.append((int(slot), name))
    return jobs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default=HERE, help='folder with .scl/.kbm and manifest.tsv')
    ap.add_argument('--port', default='FH-2', help='substring of MIDI output name (default: FH-2)')
    ap.add_argument('--list', action='store_true', help='list MIDI outputs and exit')
    ap.add_argument('--only', help='comma-separated names from manifest')
    ap.add_argument('--sysex-base', type=int, choices=(0, 1), default=0,
                    help='SysEx slot byte for screen slot 1 (default 0)')
    ap.add_argument('--delay', type=float, default=300, help='ms between messages (flash writes)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--syx', help='write all messages into this .syx instead of sending')
    ap.add_argument('--scl'); ap.add_argument('--kbm'); ap.add_argument('--slot', type=int)
    a = ap.parse_args()

    if a.list:
        import mido
        print('\n'.join(mido.get_output_names()) or '(no MIDI outputs)')
        return

    # collect (kind, slot, path)
    msgs = []
    if a.scl or a.kbm:
        if a.slot is None:
            sys.exit('--slot is required with --scl/--kbm')
        for kind, p in (('scl', a.scl), ('kbm', a.kbm)):
            if p:
                msgs.append((kind, a.slot, p))
    else:
        jobs = read_manifest(os.path.join(a.dir, 'manifest.tsv'))
        if a.only:
            want = set(a.only.split(','))
            missing = want - {n for _, n in jobs}
            if missing:
                sys.exit(f'not in manifest: {", ".join(sorted(missing))}')
            jobs = [j for j in jobs if j[1] in want]
        for slot, name in jobs:
            for kind in ('scl', 'kbm'):
                msgs.append((kind, slot, os.path.join(a.dir, f'{name}.{kind}')))

    built = [(k, s, p, build(k, s, p, a.sysex_base)) for k, s, p in msgs]

    if a.dry_run or a.syx:
        blob = b''
        for k, s, p, d in built:
            print(f'{k} slot {s:2d} (sysex {d[5]:2d})  {len(d) + 2:5d} bytes  {os.path.basename(p)}')
            blob += bytes([0xF0] + d + [0xF7])
        if a.syx:
            open(a.syx, 'wb').write(blob)
            print(f'wrote {a.syx} ({len(blob)} bytes)')
        return

    import mido
    names = [n for n in mido.get_output_names() if a.port.lower() in n.lower()]
    if not names:
        sys.exit(f'no MIDI output matching "{a.port}". Available:\n  ' +
                 '\n  '.join(mido.get_output_names()))
    print(f'-> {names[0]}')
    with mido.open_output(names[0]) as out:
        for k, s, p, d in built:
            out.send(mido.Message('sysex', data=d))
            print(f'  {k} slot {s:2d} (sysex {d[5]:2d})  {os.path.basename(p)}')
            time.sleep(a.delay / 1000)
    print('done. Check slots on the FH-2 (Scala selection in the converter).')


if __name__ == '__main__':
    main()
