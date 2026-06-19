# Urdu IPA to CISAMPA Lexicon Conversion

Converts a word-level IPA (International Phonetic Alphabet) lexicon into **CISAMPA** format — the phonetic inventory used by the CLE (Centre for Language Engineering) Urdu TTS system.

---

## What It Does

Takes a plain-text lexicon where each line is:

```
word    /IPA_transcription/
```

And outputs:

```
word    /CISAMPA/tokens/like/this/
```

---

## Requirements

- Python 3.7+
- No external libraries needed (uses only `os` and `unicodedata` from the standard library)

---

## Setup

1. **Clone or download** this repository.
2. Open `convert_ipa_to_cisampa.py` and edit the two path variables near the top:

```python
INPUT_FILE  = r"path/to/your/lexicon_input.txt"   # your IPA lexicon
OUTPUT_FILE = r"path/to/your/lexicon_cisampa.txt"  # where output goes
```

Alternatively, set `USE_SCRIPT_DIR = True` to resolve both paths relative to the script's own folder (useful if you drop your lexicon file next to the script).

---

## Input Format

Plain UTF-8 text file, one entry per line, tab-separated:

```
پانی	paːniː
گھر	ɡʰər
دل	d̪ɪl
```

Lines with fewer than two tab-separated columns are passed through unchanged.

---

## Output Format

Same structure, CISAMPA transcription in slash-delimited token notation:

```
پانی	/P/A_A/N/I_I/
گھر	/G_H/A/R/
دل	/D_D/I/L/
```

---

## Example Conversions

Real entries from an Urdu lexicon showing IPA → CISAMPA conversion:

| اردو (Urdu) | Meaning | IPA | CISAMPA |
|---|---|---|---|
| پانی | water | `paːniː` | `/P/A_A/N/I_I/` |
| گھر | house | `ɡʰər` | `/G_H/A/R/` |
| دل | heart | `d̪ɪl` | `/D_D/I/L/` |
| کتاب | book | `kɪt̪aːb` | `/K/I/T_D/A_A/B/` |
| محبت | love | `məhəbbət̪` | `/M/A/H/A/B/B/A/T_D/` |
| خوشی | happiness | `xuʃiː` | `/X/U_U/S_H/I_I/` |
| زندگی | life | `zɪnd̪əɡiː` | `/Z/I/N/D_D/A/G/I_I/` |
| آواز | voice | `aːʋaːz` | `/A_A/V/A_A/Z/` |
| رات | night | `raːt̪` | `/R/A_A/T_D/` |
| ماں | mother | `mãː` | `/M/A_A_N/` |

---

## Running

```bash
python convert_ipa_to_cisampa.py
```

The script prints:
- Paths it is reading from / writing to
- Total lines written
- Any IPA characters it could not map (with counts), so you can extend `MAPPINGS` if needed
- A 10-line sample of the output

---

## Mapping Coverage

The `MAPPINGS` table in the script handles:

| Category | Examples |
|---|---|
| Diphthongs | `ɑːeː`, `aːiː`, `ʊiː`, … |
| Aspirated consonants | `pʰ`, `bʰ`, `kʰ`, `tʃʰ`, `ɽʰ`, … |
| Nasalised long vowels | `ũː`, `ãː`, `ĩː`, … |
| Nasalised short vowels | `ɪ̃`, `ʊ̃`, `ə̃`, … |
| Long vowels | `uː`, `iː`, `eː`, `ɑː`, … |
| Affricates | `tʃ`, `dʒ`, `ʧ`, `ʤ` |
| Dental consonants | `t̪`, `d̪`, `n̪` |
| IPA consonants | `ʃ`, `ʒ`, `ɣ`, `ʔ`, `ʋ`, `ɽ`, … |
| ASCII consonants/vowels | `p b m n k g … a e i o u` |

Unknown characters are reported but not silently dropped — they appear in the warning list at the end so you can decide how to handle them.

---

## Extending the Mapping

Add new rules to the `MAPPINGS` list in `convert_ipa_to_cisampa.py`:

```python
('your_ipa_symbol', 'YOUR_CISAMPA'),
```

The script automatically re-sorts by length so longer patterns always take priority over shorter ones — you do not need to worry about insertion order.

---

## Project Context

Built as part of an Urdu TTS data preparation pipeline. The CISAMPA symbol set follows the CLE Urdu Phonetic Inventory specification.
