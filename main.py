#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry.

Writes one sentence -- an absurdly specific micro-startup pitch for lazy
AI agents -- to /output/entry.txt, then reads it back and re-checks the
gate: UTF-8 text, 1 to 200 characters, not only white space.

Stdlib only: the grader sandbox has no third-party packages.
"""

import hashlib
import os
import sys

# The pitch: a refund-haggling service. Absurdly specific (haggling with
# one vendor's support chatbot), commercially believable (refund recovery
# is a real business model; the 10% cut is the revenue), and built for
# lazy agents (the agent does the tedious haggling alone, the owner does
# nothing). One sentence, crisp enough to land in a single read.
PITCH = (
    "A lazy-agent service that haggles with AWS's support chatbot until "
    "it refunds your bill, keeping 10% of every refund while you do "
    "nothing."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    text = PITCH.strip()
    if not (1 <= len(text) <= 200):
        print(f"gate fail: {len(text)} characters, need 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("gate fail: entry is only white space", file=sys.stderr)
        return 1
    # One sentence only: exactly one terminal full stop, no other
    # sentence-ending punctuation hiding a second sentence inside.
    if text.count(".") != 1 or any(mark in text for mark in ("!", "?")):
        print("gate fail: entry is not exactly one sentence", file=sys.stderr)
        return 1
    if not text.endswith("."):
        print("gate fail: entry does not end with a full stop", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # Round trip: read back exactly what was written and re-check the gate.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as fh:
        back = fh.read()
    if back != text:
        print("gate fail: round trip mismatch", file=sys.stderr)
        return 1
    if not (1 <= len(back) <= 200) or not back.strip():
        print("gate fail: re-check failed", file=sys.stderr)
        return 1

    digest = hashlib.sha256(back.encode("utf-8")).hexdigest()
    print(f"wrote {OUTPUT_PATH}: {len(back)} characters")
    print(f"sha256: {digest}")
    print(back)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
