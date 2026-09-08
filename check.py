#!/usr/bin/env python3
"""Gate checks for the org profile. Same rule the site enforces on itself,
enforced here — because on 2026-09-08 the site stopped announcing its own
absence and the four policy files in this repo kept saying "design phase" for
three more hours. Nothing caught it: the site's gate reads the site, and this
repo had no gate.

Every check exists because the failure happened at least once.

  1. The profile sells the product; it never announces its absence.
     No "design phase", "not built", "no code", "nothing is shipped" in the
     visible copy. The phase is stated once, as a dated release, and every
     limit is a dated roadmap item. Same for defensive framing ("we are not
     claiming", "not just another") and negative chapter headings ("What we
     will not do") — the section may stay, its heading says what it is.
  2. The one public date lives on the site. Every file that says when
     release 2 ships must say the same thing the site's build.py says, and the
     site is what a reader is sent to for it. A date restated in a fourth
     place drifts like any other fact (design roadmap §1.1).
  3. Every local link resolves. Two of the four files link each other; a
     rename breaks one silently.
  4. Exactly one contact address, byte for byte, in every file that has one.
     The site's gate 16 caught a second literal address surviving a rename.

Visible copy only: link targets, image alt text and fenced code are not the
file's voice, and words inside a quotation belong to their source.

stdlib only. Exit non-zero on any failure. Run: python3 check.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = [
    ROOT / "profile" / "README.md",
    ROOT / "SECURITY.md",
    ROOT / "SUPPORT.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    *sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.md")),
]
SITE = "https://doublegate-io.github.io"
CONTACT = "eugene.korniichuk@gmail.com"

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def visible(markdown: str) -> str:
    """The reader's text: no code, no HTML tags, no link targets, no quotations."""
    t = re.sub(r"(?s)```.*?```", " ", markdown)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)                       # badges, the wordmark, <div align>
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)          # images: alt text is not copy
    t = re.sub(r"\]\([^)]*\)", "]", t)                   # keep link labels, drop targets
    t = re.sub(r"(?m)^\s*>.*$", " ", t)                  # blockquotes belong to their source
    t = re.sub(r"`[^`]*`", " ", t)                       # inline code names things, it does not argue
    return re.sub(r"\s+", " ", t)


# 1. THE PROFILE SELLS THE PRODUCT; IT NEVER ANNOUNCES ITS ABSENCE.
#    The three patterns are copied from the site's check.py gate 17 so the two
#    repos cannot disagree about what the rule is. Extend both or neither.
PHASE_LANGUAGE = re.compile(
    r"design[- ]phase"
    r"|\bnot (?:yet )?(?:shipped|built|running|implemented)\b"
    r"|\bno (?:design|code|dates?)\b(?! path)"
    r"|\bnothing (?:is |here is )?(?:built|shipped|scheduled)\b"
    r"|\bdesigned(?:,)? (?:rather than|but not|not) (?:shipped|built|running)\b"
    r"|\bdoes not exist yet\b|\bnot (?:yet )?scheduled\b|\bscheduled, not drawn\b"
    r"|\bplanned, not\b|\bnot a product yet\b|\bunbuilt\b",
    re.I)
DEFENSIVE_FRAMING = re.compile(
    r"not just another|we (?:are|'re) not claiming|we (?:do not|don't) claim"
    r"|to be clear|let'?s be clear|silver bullet|\bwe refuse\b|\bwe will not (?:tell|claim)\b",
    re.I)
NEGATIVE_HEADING = re.compile(
    r"(?im)^#{1,6}\s*what (?:we|this|it) (?:are|is|will|do|does|can)(?:n'?t| not) ")

for f in FILES:
    raw = f.read_text()
    body = visible(raw)
    rel = f.relative_to(ROOT)
    for m in PHASE_LANGUAGE.finditer(body):
        fail(f"{rel}: phase language in visible copy -> …{body[max(0, m.start() - 45): m.end() + 30]}…")
    for m in DEFENSIVE_FRAMING.finditer(body):
        fail(f"{rel}: defensive framing in visible copy -> …{body[max(0, m.start() - 45): m.end() + 30]}…")
    for m in NEGATIVE_HEADING.finditer(raw):
        fail(f"{rel}: negative chapter heading -> {m.group(0).strip()!r}")

# 2. THE ONE PUBLIC DATE LIVES ON THE SITE; RESTATEMENTS AGREE WITH IT.
#    We cannot read the site's build.py from here (separate repo, and a gate
#    must not reach across a repo boundary), so the rule is: every restatement
#    in this repo agrees with every other, and each file that restates it also
#    links the reader to the site. If the date moves, the site moves first and
#    this repo follows in the same hour.
DATE = re.compile(r"\bQ[1-4] 20\d\d\b")
dates: dict[str, set[str]] = {}
for f in FILES:
    found = set(DATE.findall(visible(f.read_text())))
    if found:
        dates[str(f.relative_to(ROOT))] = found
        if SITE not in f.read_text():
            fail(f"{f.relative_to(ROOT)}: restates the release date but never links the site that owns it")
all_dates = set().union(*dates.values()) if dates else set()
if len(all_dates) > 1:
    fail(f"release date restated inconsistently: {dates}")

# 3. EVERY LOCAL LINK RESOLVES.
for f in FILES:
    for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", f.read_text()):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (f.parent / target).resolve().exists():
            fail(f"{f.relative_to(ROOT)}: link to missing file {target!r}")

# 4. ONE CONTACT ADDRESS, BYTE FOR BYTE.
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
for f in [*FILES, ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml"]:
    for addr in set(EMAIL.findall(f.read_text())):
        if addr != CONTACT:
            fail(f"{f.relative_to(ROOT)}: second contact address {addr!r} (the one address is {CONTACT})")

if failures:
    print("FAIL")
    for msg in failures:
        print("  " + msg)
    sys.exit(1)
print(f"PASS — {len(FILES)} files: " + ", ".join(str(f.relative_to(ROOT)) for f in FILES))
print("  no phase language · one date, site-owned · links resolve · one contact address")
