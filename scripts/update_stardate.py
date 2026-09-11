#!/usr/bin/env python3
"""Rewrite the stardate in the LCARS footer SVG to the current date.

Stardate format is YYYY.DDD (calendar year plus zero-padded day of year),
e.g. 2026.254 for September 11, 2026.

Exits 0 whether or not a change was made; the workflow decides what to commit.
"""

import datetime
import pathlib
import re
import sys

FOOTER = pathlib.Path(__file__).resolve().parent.parent / "assets" / "lcars" / "footer-status.svg"
STARDATE_PATTERN = re.compile(r"Stardate \d{4}\.\d{3}")


def current_stardate(today: datetime.date) -> str:
    return f"{today.year}.{today.timetuple().tm_yday:03d}"


def main() -> int:
    if not FOOTER.exists():
        print(f"error: {FOOTER} not found", file=sys.stderr)
        return 1

    stardate = current_stardate(datetime.date.today())
    original = FOOTER.read_text()
    updated, count = STARDATE_PATTERN.subn(f"Stardate {stardate}", original)

    if count == 0:
        print(f"error: no 'Stardate YYYY.DDD' text found in {FOOTER.name}", file=sys.stderr)
        return 1

    if updated == original:
        print(f"stardate already current: {stardate}")
        return 0

    FOOTER.write_text(updated)
    print(f"stardate updated to {stardate} ({count} occurrence(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
