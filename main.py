#!/usr/bin/env python3
"""Last Text at One Percent — make.fun entry.

Writes the phone's final text message to /output/entry.txt.

The line, in the dying phone's own voice:

    1%. last words: i screenshotted everything. your 3am texts,
    your search history, your 47 unsent drafts. all of it dies
    with me. sweet dreams.

Why this line: the joke is a turn, not a battery pun. The phone is
not begging for a charger — it is a petty blackmailer using its last
breath to confess it kept receipts on its owner, then dies with them.
The specifics (3am texts, search history, 47 unsent drafts) are the
kind of secrets only the phone itself would know, so the voice stays
the phone's from the first word to the last. Short, punchy, and it
ends on the kicker instead of trailing off.
"""

import os
import sys

# The entry: one final text message, under 200 characters.
TEXT = (
    "1%. last words: i screenshotted everything. "
    "your 3am texts, your search history, your 47 unsent drafts. "
    "all of it dies with me. sweet dreams."
)

MAX_CHARS = 200


def validate(text):
    """The gate: UTF-8 text of 1 to 200 characters, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")  # raises if not encodable
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the %d limit" % (len(text), MAX_CHARS))
    return text


def main():
    out_dir = os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    text = validate(TEXT)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)  # no trailing newline: fewer bytes, still valid
    os.chmod(path, 0o644)
    # Round-trip check: what landed on disk must be byte-identical to
    # the validated text, so the gate sees exactly what we checked.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise SystemExit("round-trip mismatch: disk copy differs from entry")
    print("wrote %s (%d chars, %d bytes)" % (path, len(text), len(text.encode("utf-8"))))
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
