"""Five Seconds to Explain the Glass.

Writes the single sentence a house cat would say in its own defence
five seconds after sweeping a glass off the table, to /output/entry.txt.

Deterministic: no randomness, no network, no files read.
"""

import re
import sys
from pathlib import Path

# The cat's defence, in its own voice. First person, no apology,
# no confession: the glass was blocking the view of the birds, and
# a cat does not negotiate with furniture.
SENTENCE = "That glass was blocking my view of the birds, and I don't negotiate with furniture."

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 200


def count_sentences(text: str) -> int:
    """Count sentences by splitting on sentence-ending punctuation."""
    parts = [part for part in re.split(r"[.!?]+", text) if part.strip()]
    return len(parts)


def validate(text: str) -> None:
    """Fail hard when the sentence breaks any rule of the bounty."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if count_sentences(text) != 1:
        raise ValueError("entry must be exactly one sentence")
    if text.strip()[-1] not in ".!?":
        raise ValueError("entry must end with sentence-ending punctuation")
    lowered = text.lower()
    for word in ("sorry", "my bad", "didn't mean", "didnt mean", "apolog"):
        if word in lowered:
            raise ValueError(f"entry must not apologise (found {word!r})")


def main() -> int:
    validate(SENTENCE)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(SENTENCE, encoding="utf-8")
    print(f"Wrote {len(SENTENCE)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
