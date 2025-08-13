#!/usr/bin/env python3
"""
clean_text.py

Remove ANSI escape sequences, box-drawing characters, emojis, control characters,
trim lines, collapse repeated spaces and blank lines.

Usage:
    python clean_text.py input.txt -o clean.txt
    cat input.txt | python clean_text.py -   # read from stdin, write to stdout
"""

import argparse
import re
import sys

# Patterns
ANSI_RE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')          # ANSI CSI sequences
BOX_RE  = re.compile(r'[\u2500-\u257F\u2580-\u259F]+')    # box-drawing / block elements
EMOJI_RE = re.compile(
    "["                                 # common emoji / pictograph ranges
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map
    u"\U0001F1E0-\U0001F1FF"  # flags
    u"\u2600-\u26FF"          # miscellaneous symbols
    u"\u2700-\u27BF"          # dingbats
    "]+", flags=re.UNICODE)
CTRL_RE = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')  # C0 controls except newline (10) and tab (9)

def clean_text(text: str) -> str:
    # remove ANSI escapes and other junk
    text = ANSI_RE.sub('', text)
    text = BOX_RE.sub('', text)
    text = EMOJI_RE.sub('', text)
    text = CTRL_RE.sub('', text)

    # normalize spaces per-line and strip ends
    out_lines = []
    for raw_line in text.splitlines():
        # collapse multiple spaces/tabs into one, then strip ends
        line = re.sub(r'[ \t]+', ' ', raw_line).strip()
        out_lines.append(line)

    # collapse multiple blank lines to a single blank line
    cleaned_lines = []
    last_was_blank = False
    for line in out_lines:
        if line == '':
            if not last_was_blank:
                cleaned_lines.append('')   # keep a single blank line
            last_was_blank = True
        else:
            cleaned_lines.append(line)
            last_was_blank = False

    # final strip to remove leading/trailing blank lines, ensure file ends with newline
    result = '\n'.join(cleaned_lines).strip() + '\n'
    return result

def main():
    p = argparse.ArgumentParser(description="Clean ANSI/box/emoji and whitespace from text")
    p.add_argument('infile', help="input file path or '-' for stdin")
    p.add_argument('-o', '--outfile', default='-', help="output file path or '-' for stdout (default)")
    args = p.parse_args()

    if args.infile == '-':
        raw = sys.stdin.read()
    else:
        with open(args.infile, 'r', encoding='utf-8', errors='replace') as fh:
            raw = fh.read()

    cleaned = clean_text(raw)

    if args.outfile == '-':
        sys.stdout.write(cleaned)
    else:
        with open(args.outfile, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(cleaned)

if __name__ == '__main__':
    main()
