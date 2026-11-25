#!/usr/bin/env python3
"""Print the one-line Monday review stored in entry.txt.

Revised entry: the reviewer gives Monday one star, and Monday replies
like a business answering a bad review -- blaming the alarm clock
and asking for a reconsideration.

Deterministic: standard library only, no network, no randomness,
no wall-clock time. Prints the review, then runs a gate self-check
(length under 200 characters, exactly one sentence, single line,
and a write-then-read-back round trip that must match byte for byte).
"""

import pathlib
import re
import sys
import tempfile

ENTRY_FILE = pathlib.Path(__file__).with_name("entry.txt")
MAX_CHARS = 200


def load_entry() -> str:
    """Read the review, stripping only the trailing newline."""
    return ENTRY_FILE.read_text(encoding="utf-8").strip()


def sentence_count(text: str) -> int:
    """Count sentence-ending punctuation marks."""
    return len(re.findall(r"[.!?]", text))


def self_check(text: str) -> None:
    """Gate self-check: length, sentence count, line count, round trip."""
    assert text, "entry is empty"
    assert "\n" not in text, "entry must be exactly one line"
    assert len(text) < MAX_CHARS, (
        f"entry is {len(text)} characters, must be under {MAX_CHARS}"
    )
    assert sentence_count(text) == 1, (
        f"entry has {sentence_count(text)} sentences, must have exactly 1"
    )
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(text)
        tmp_path = pathlib.Path(tmp.name)
    try:
        round_tripped = tmp_path.read_text(encoding="utf-8")
    finally:
        tmp_path.unlink(missing_ok=True)
    assert round_tripped == text, "write-then-read-back mismatch"


def main() -> int:
    text = load_entry()
    self_check(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
