# FH-2 Scala tuning set (32 slots)

Scala scale (`.scl`) and keyboard-mapping (`.kbm`) files for the Expert Sleepers FH-2, plus a loader script. One `.scl` + one `.kbm` per slot, same slot number for both.

All mappings: **C4 (MIDI note 60) = 261.626 Hz = first scale degree** (for gamelans: pelog 1, or selisir ding). To retune, change line 6 of the `.kbm`.

## Loading (macOS)

```bash
cd fh2set
python3 -m venv .venv
source .venv/bin/activate
pip install mido python-rtmidi

python fh2_load.py --list                # find the FH-2 MIDI port
python fh2_load.py --dry-run             # show what will be sent
python fh2_load.py --only edo12          # test one slot first (should land in slot 1)
python fh2_load.py                       # load all 32 slots
python fh2_load.py --only gam_malm,bp_et # load selected entries
```

Slot numbers in `manifest.tsv` and below are as shown on the FH-2 screen (1-32). The script sends `slot - 1` as the SysEx slot byte. If everything lands one slot off, run again with `--sysex-base 1`.

Other options: `--port NAME` (substring of the MIDI output name, default `FH-2`), `--delay MS` (pause between messages, default 300), `--syx FILE` (write a single .syx instead of sending), `--scl a.scl --kbm a.kbm --slot N` (ad-hoc pair).

After loading, pick the slots in the MIDI/CV converter settings (Scala scale + keyboard map) and save the configuration/preset.

## Layout conventions

- Scales that fit in 12 keys use a normal 12-key mapping.
- Octave-repeating scales with more than 12 steps use a mapping block of 24, 48 or 72 keys (the smallest multiple of 24 that fits): consecutive keys = consecutive steps, surplus keys at the top of each block are silent, and the octave always lands on a C.
- Gamelans: white keys = pelog, black keys = slendro, from the same ensemble or tuning system.
- Non-octave tunings are mapped linearly: every key is the next step.


## EDO

| Slot | Name | Tuning | Keyboard |
|---|---|---|---|
| 1 | `edo12` | 12 equal divisions of the octave | Standard keyboard. Use as the "normal tuning" reference. |
| 2 | `edo15` | 15 equal divisions of the octave | 80.0 c per key. Block of 24 keys = one octave: 15 consecutive keys play, the top 9 keys of each block are silent. C4 -> C6 is the octave. |
| 3 | `edo16` | 16 equal divisions of the octave | 75.0 c per key. Block of 24 keys = one octave: 16 consecutive keys play, the top 8 keys of each block are silent. C4 -> C6 is the octave. |
| 4 | `edo17` | 17 equal divisions of the octave | 70.6 c per key. Block of 24 keys = one octave: 17 consecutive keys play, the top 7 keys of each block are silent. C4 -> C6 is the octave. |
| 5 | `edo19` | 19 equal divisions of the octave | 63.2 c per key. Block of 24 keys = one octave: 19 consecutive keys play, the top 5 keys of each block are silent. C4 -> C6 is the octave. |
| 6 | `edo22` | 22 equal divisions of the octave | 54.5 c per key. Block of 24 keys = one octave: 22 consecutive keys play, the top 2 keys of each block are silent. C4 -> C6 is the octave. |
| 7 | `edo24` | 24 equal divisions of the octave | 50.0 c per key, 24 keys = one octave (C4 -> C6). |
| 8 | `edo31` | 31 equal divisions of the octave | 38.7 c per key. Block of 48 keys = one octave: 31 consecutive keys play, the top 17 keys of each block are silent. C4 -> C8 is the octave. |
| 9 | `edo41` | 41 equal divisions of the octave | 29.3 c per key. Block of 48 keys = one octave: 41 consecutive keys play, the top 7 keys of each block are silent. C4 -> C8 is the octave. |
| 10 | `edo53` | 53 equal divisions of the octave | 22.6 c per key. Block of 72 keys = one octave: 53 consecutive keys play, the top 19 keys of each block are silent. C4 -> C10 is the octave. |
| 11 | `edo72` | 72 equal divisions of the octave | 16.7 c per key, 72 keys = one octave (C4 -> C10). |

## Gamelan

| Slot | Name | Tuning | Keyboard |
|---|---|---|---|
| 12 | `gam_udanmas` | Gamelan Udan Mas, pelog + slendro (approx. JI) | White = pelog 1-7, black = slendro 1 2 3 5 6. Shared tones: F = G# (p4 = s5), A = A# (p6 = s6). |
| 13 | `gam_kanyut` | Gamelan Kyahi Kanyut Mesem (Mangkunegaran, Solo), measured | White = pelog 1-7, black = slendro 1 2 3 5 6. Shared tone: G = G# (p5 = s5). |
| 14 | `gam_alves` | Bill Alves just-intonation gamelan, pelog + slendro | White = pelog 1-7, black = slendro 1 2 3 5 6. Shared tone: G = G# (p5 = s5). |
| 15 | `gam_peliatan` | Peliatan (Bali): gong kebyar selisir + gender wayang slendro, measured | White C D E G A = selisir ding dong deng dung dang (pelog 1 2 3 5 6 positions), F and B silent; black = slendro. Two ensembles of the same village, both measured in Hz. |
| 16 | `gam_malm` | Javanese pelog + slendro (Malm), two measured stretched octaves, tumbuk 6 | Stretched octave. 24-key block = two gamelan octaves (~2444 c instead of 2400). White = pelog, black = slendro, both over two octaves. p6 = s6 (tumbuk 6, assumed alignment). |
| 17 | `gam_javavg` | Average Javanese pelog + slendro, octave stretched to 1208 c, tumbuk 6 | Stretched octave (+8 c per octave). White = pelog, black = slendro. p6 = s6. |

## Other

| Slot | Name | Tuning | Keyboard |
|---|---|---|---|
| 18 | `ji_5lim` | 5-limit just intonation, 12 notes on C | Standard keyboard, tonic C. Pure thirds and fifths in C major. |
| 19 | `ji_7lim` | 7-limit just intonation, 12 notes on C | Standard keyboard, tonic C. Septimal minor third on D#, harmonic seventh on A#. |
| 20 | `pythag` | Pythagorean 12, chain of pure fifths Gb..B | Standard keyboard. Pure fifths, wide thirds; wolf fifth B-Gb. |
| 21 | `meantone` | Quarter-comma meantone, Eb..G# | Standard keyboard. Pure major thirds; wolf fifth G#-Eb. |
| 22 | `werck3` | Werckmeister III well temperament (1681) | Standard keyboard. All keys playable, each with its own colour (Bach era). |
| 23 | `harm08` | Harmonic series 8-16 | Harmonics on nearest keys: C=8 D=9 E=10 F#=11 G=12 G#=13 A#=14 B=15; other keys silent. |
| 24 | `harm16` | Harmonic series 16-32 | 24-key block = one octave: harmonics 16..31 on 16 consecutive keys, top 8 keys silent. |
| 25 | `partch43` | Harry Partch's 43-tone just scale | 48-key block = one octave: 43 consecutive keys, top 5 keys silent. C4 -> C8 is the octave. |
| 26 | `maqam_rast` | Maqam Rast on C (24-EDO neutral E and B) | White keys only: C D E-half-flat F G A B-half-flat; black keys silent. |
| 27 | `bp_et` | Bohlen-Pierce equal, 13 steps of 3/1 | Non-octave. Linear: each key = 146.3 c, 13 keys = tritave 3/1 (C4 -> C#5). |
| 28 | `bp_ji` | Bohlen-Pierce just, 13 steps of 3/1 | Non-octave. Linear, 13 keys = tritave 3/1. Pure 3:5:7 intervals. |
| 29 | `carlos_a` | Wendy Carlos Alpha, 77.965 c step | Non-octave. Linear: each key = 77.965 c; 9 steps ~ a fifth (701.7 c). |
| 30 | `carlos_b` | Wendy Carlos Beta, 63.833 c step | Non-octave. Linear: each key = 63.833 c; 11 steps ~ a fifth (702.2 c). |
| 31 | `carlos_g` | Wendy Carlos Gamma, 35.099 c step | Non-octave. Linear: each key = 35.099 c; 20 steps ~ a fifth (702.0 c). |
| 32 | `cet88` | Gary Morrison 88-cent equal temperament | Non-octave. Linear: each key = 88 c; 8 steps = 704 c. |

## Notes

- Large EDOs need many keys per octave: 41-EDO uses 48 keys, 53- and 72-EDO use 72 keys per octave, so the 128 MIDI notes cover less than two octaves. Transpose your controller or sequencer accordingly.
- `gam_malm`: the source gives no relation between its pelog and slendro sets; they are aligned by tumbuk 6 (p6 = s6), the usual Javanese practice. Pelog and slendro octaves differ slightly (2447 vs 2441 c over two octaves); the average is used.
- `gam_javavg` combines two different surveys (Kunst 1949 pelog, Surjodiningrat 1993 slendro) and applies the measured 1208 c slendro octave to both.
- `gam_peliatan` combines two ensembles of Peliatan village (gamelan gong, gender wayang); their relative pitch comes from the measured frequencies (280 Hz and 305.5 Hz).
- Pitch data comes from the Scala archive by Manuel Op de Coul (Huygens-Fokker Foundation), via the copy bundled with music21. Measured gamelan tunings are snapshots of real instruments.

## SysEx format

```
F0 00 21 27 2F 11 <slot> <.scl text> F7   install .scl
F0 00 21 27 2F 12 <slot> <.kbm text> F7   install .kbm
```
