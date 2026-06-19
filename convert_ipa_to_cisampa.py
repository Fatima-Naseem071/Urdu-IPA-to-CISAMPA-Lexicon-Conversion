#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_ipa_to_cisampa.py
--------------------------
Converts a word-level IPA lexicon to CISAMPA (CLE Urdu Phonetic Inventory) format.

Input format  (tab-separated):  word <TAB> IPA_transcription
Output format (tab-separated):  word <TAB> /CISAMPA/tokens/

Usage:
    python convert_ipa_to_cisampa.py

Before running, set INPUT_FILE and OUTPUT_FILE below to your actual file paths.
"""

import os
import unicodedata

# ── Paths (edit these before running) ────────────────────────────────────────
#
# INPUT_FILE  : path to your IPA lexicon  (word TAB IPA, one entry per line)
# OUTPUT_FILE : where the CISAMPA lexicon will be written
#
INPUT_FILE  = r"path/to/your/lexicon_input.txt"   # <-- change this
OUTPUT_FILE = r"path/to/your/lexicon_cisampa.txt"  # <-- change this

# Optional: set to True to auto-resolve paths relative to this script's folder
USE_SCRIPT_DIR = False
if USE_SCRIPT_DIR:
    _DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE  = os.path.join(_DIR, "lexicon_input.txt")
    OUTPUT_FILE = os.path.join(_DIR, "lexicon_cisampa.txt")

# ── IPA → CISAMPA mapping ────────────────────────────────────────────────────
# Rules are ordered longest-first; the greedy tokeniser picks the longest
# match at each position so multi-character IPA sequences are handled before
# their individual characters.
MAPPINGS = [
    # Strip stress markers and spaces
    ('ˈ', ''), ('ˌ', ''), (' ', ''),

    # Diphthongs
    ('ɑːeː', 'A_A_A_Y'),  ('aːeː', 'A_A_A_Y'),
    ('ɑːiː', 'A_A_I_I'),  ('aːiː', 'A_A_I_I'),
    ('ɑ:e:', 'A_A_A_Y'),  ('a:e:', 'A_A_A_Y'),
    ('ɑ:i:', 'A_A_I_I'),  ('a:i:', 'A_A_I_I'),
    ('ɑːe',  'A_A_A_Y_H'),('aːe',  'A_A_A_Y_H'),
    ('ɑ:e',  'A_A_A_Y_H'),('a:e',  'A_A_A_Y_H'),
    ('ɑːɪ',  'A_A_I'),    ('aːɪ',  'A_A_I'),
    ('ɑ:ɪ',  'A_A_I'),    ('a:ɪ',  'A_A_I'),
    ('əiː',  'A_I_I'),    ('əi:',  'A_I_I'),
    ('əeː',  'A_A_Y'),    ('əe:',  'A_A_Y'),
    ('ɪũː',  'I_U_U_N'),  ('ɪũ:',  'I_U_U_N'),
    ('æɑː',  'A_E_H_A_A'),('æaː',  'A_E_H_A_A'),
    ('æɑ:',  'A_E_H_A_A'),('æa:',  'A_E_H_A_A'),
    ('ʊiː',  'U_U_I_I'),  ('ʊi:',  'U_U_I_I'),
    ('oːiː', 'O_O_I_I'),  ('o:i:', 'O_O_I_I'),
    ('eɑː',  'A_Y_H_A_A'),('eɑ:',  'A_Y_H_A_A'),

    # Aspirated consonants
    ('t̪ʰ', 'T_D_H'), ('d̪ʰ', 'D_D_H'),
    ('ɽʰ',  'R_R_H'),
    ('tʃʰ', 'T_S_H'), ('dʒʰ', 'D_Z_H'),
    ('ʧʰ',  'T_S_H'), ('ʤʰ',  'D_Z_H'),
    ('pʰ',  'P_H'),   ('bʰ',  'B_H'),  ('mʰ', 'M_H'),
    ('ʈʰ',  'T_H'),   ('ɖʰ',  'D_H'),
    ('nʰ',  'N_H'),   ('kʰ',  'K_H'),
    ('ɡʰ',  'G_H'),   ('gʰ',  'G_H'),
    ('lʰ',  'L_H'),   ('rʰ',  'R_H'),  ('jʰ', 'J_H'),

    # Nasalised long vowels
    ('ũː',  'U_U_N'), ('ũ:',  'U_U_N'),
    ('õː',  'O_O_N'), ('õ:',  'O_O_N'),
    ('ɔ̃ː',  'O_N'),   ('ɔ̃:',  'O_N'),
    ('ɑ̃ː',  'A_A_N'), ('ɑ̃:',  'A_A_N'),
    ('ãː',  'A_A_N'), ('ã:',  'A_A_N'),
    ('ĩː',  'I_I_N'), ('ĩ:',  'I_I_N'),
    ('ẽː',  'A_Y_N'), ('ẽ:',  'A_Y_N'),
    ('æ̃ː',  'A_E_N'), ('æ̃:',  'A_E_N'),

    # Short nasalised vowels
    ('ɪ̃',  'I_N'),
    ('ʊ̃',  'U_N'),
    ('ə̃',  'A_N'),
    ('ɔ̃',  'O_N'),
    ('ã',   'A_A_N'),
    ('ẽ',   'A_Y_N'),
    ('ĩ',   'I_I_N'),
    ('ũ',   'U_U_N'),

    # Long vowels
    ('uː', 'U_U'), ('u:', 'U_U'),
    ('oː', 'O_O'), ('o:', 'O_O'),
    ('ɔː', 'O'),   ('ɔ:', 'O'),
    ('ɑː', 'A_A'), ('ɑ:', 'A_A'),
    ('aː', 'A_A'), ('a:', 'A_A'),
    ('iː', 'I_I'), ('i:', 'I_I'),
    ('eː', 'A_Y'), ('e:', 'A_Y'),
    ('æː', 'A_E'), ('æ:', 'A_E'),

    # Affricates
    ('tʃ', 'T_S'), ('dʒ', 'D_Z'),
    ('ʧ',  'T_S'), ('ʤ',  'D_Z'),

    # Dental consonants (with U+032A combining diacritic)
    ('t̪', 'T_D'), ('d̪', 'D_D'), ('z̪', 'Z'), ('n̪', 'N'),

    # IPA consonants
    ('ŋ',  'N_G'), ('ɡ',  'G'),
    ('ʔ',  'Y'),   ('ʕ',  'Y'),
    ('ʋ',  'V'),   ('ɦ',  'H'), ('ħ', 'H'),
    ('ʃ',  'S_H'), ('ʒ',  'Z_Z'),
    ('ɣ',  'G_G'),
    ('ɾ',  'R'),   ('ɽ',  'R_R'),
    ('ʈ',  'T'),   ('ɖ',  'D'),

    # Short vowels
    ('ɪ',  'I'),  ('ə',  'A'),  ('ʊ',  'U'),
    ('æ',  'A_E_H'), ('ɛ', 'A_E_H'),
    ('ɔ',  'O'),
    ('ɑ',  'A_A'),
    ('ɚ',  'A'),   # r-coloured schwa

    # ASCII consonants
    ('p', 'P'), ('b', 'B'), ('m', 'M'), ('n', 'N'),
    ('k', 'K'), ('g', 'G'), ('q', 'Q'),
    ('f', 'F'), ('v', 'V'),
    ('s', 'S'), ('z', 'Z'), ('x', 'X'),
    ('h', 'H'), ('l', 'L'), ('r', 'R'), ('j', 'J'),
    ('t', 'T_D'), ('d', 'D_D'),
    ('w', 'V'),   # bilabial w in borrowed words

    # Retroflex nasal
    ('ɳ', 'N'),

    # ASCII vowels (residual / loanwords)
    ('e', 'A_Y_H'), ('o', 'O_O_H'),
    ('a', 'A_A'),   ('u', 'U_U'),   ('i', 'I_I'),

    # Standalone nasalised o (U+00F5)
    ('õ',  'O_O_N'),

    # Lone length marks left after other patterns (strip silently)
    ('ː', ''), (':', ''),

    # Residual combining/modifier marks (strip silently)
    ('̃', ''),   # combining tilde — stranded nasalisation
    ('̪', ''),   # combining dental diacritic
    ('̯', ''),   # combining inverted breve below (non-syllabic marker)
    ('ʰ', ''),   # modifier letter small h — lone aspiration mark
    ('6', ''),   # digit typo found in some lexicon entries
]

# Pre-sort once: longest pattern first for greedy matching
_SORTED = sorted(MAPPINGS, key=lambda x: len(x[0]), reverse=True)


def preprocess(ipa: str) -> str:
    """Normalise an IPA string before tokenising."""
    ipa = ipa.replace('ˈ', '').replace('ˌ', '').replace(' ', '')
    # Some transcriptions write vowel + ː + combining-tilde (U+0303).
    # Reorder to vowel + tilde + ː so NFC can form the precomposed form.
    ipa = ipa.replace('ː̃', '̃ː').replace(':̃', '̃:')
    # NFC: a + ̃ → ã, e + ̃ → ẽ, etc.
    return unicodedata.normalize('NFC', ipa)


def ipa_to_cisampa(ipa: str):
    """
    Convert one IPA string to CISAMPA.

    Returns:
        (cisampa_str, list_of_unknown_chars)
        cisampa_str is formatted as /TOKEN/TOKEN/.../ or '' if nothing mapped.
    """
    ipa = preprocess(ipa)
    tokens, unknowns = [], []
    i = 0
    while i < len(ipa):
        matched = False
        for pat, cis in _SORTED:
            if ipa[i:i + len(pat)] == pat:
                if cis:
                    tokens.append(cis)
                i += len(pat)
                matched = True
                break
        if not matched:
            ch = ipa[i]
            unknowns.append(f'{ch}(U+{ord(ch):04X})')
            i += 1
    if not tokens:
        return '', unknowns
    return '/' + '/'.join(tokens) + '/', unknowns


def main():
    all_unknown: dict = {}
    lines_written = 0

    print(f"Reading  : {INPUT_FILE}")
    print(f"Writing  : {OUTPUT_FILE}\n")

    with open(INPUT_FILE, encoding='utf-8') as fi, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as fo:
        for line in fi:
            line = line.rstrip('\n')
            parts = line.split('\t')
            if len(parts) >= 2:
                word, ipa = parts[0], parts[1]
                cisampa, unk = ipa_to_cisampa(ipa)
                fo.write(f'{word}\t{cisampa}\n')
                for u in unk:
                    all_unknown[u] = all_unknown.get(u, 0) + 1
            else:
                fo.write(line + '\n')
            lines_written += 1

    print(f"Done. {lines_written} lines written.\n")

    if all_unknown:
        print("Warning: unknown IPA characters (may need manual review):")
        for ch, cnt in sorted(all_unknown.items(), key=lambda x: -x[1]):
            print(f"  {ch}  x{cnt}")
    else:
        print("No unknown characters encountered.")

    print("\n--- Sample output (first 10 lines) ---")
    with open(OUTPUT_FILE, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            print(line, end='')


if __name__ == '__main__':
    main()
