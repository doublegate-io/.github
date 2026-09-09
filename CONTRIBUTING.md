# Contributing

doublegate's two gates run end to end, and release 2 — the one you can point an agent at —
is Q2 2027. Until the code opens, the design package and its evidence are what there is to
argue with, and that changes what a useful contribution looks like. This file says what
actually helps now, rather than copying a workflow built for a later stage.

## The most useful thing you can send

**A correction to the evidence.** The [evidence page](https://doublegate-io.github.io/evidence.html)
carries every load-bearing claim with a primary source, including the findings that work
against the project. If a number is stale, a citation doesn't say what we claim it says, or
a source has been superseded — that is the highest-value issue anyone can open, and it goes
straight into the design.

Second most useful: **an argument the design has to answer.** Not "have you considered X"
but "X breaks this, here's why." The design package already contains an argued case for
killing the project; adding to it is a contribution, not an attack.

## Where to send what

| | Where |
|---|---|
| A wrong number, a bad citation, a broken link | [issue on the site repo](https://github.com/doublegate-io/doublegate-io.github.io/issues) |
| An argument against the design | same — an issue, stated as a claim we must answer |
| A hole in the trust model | [SECURITY.md](SECURITY.md) — email, not a public issue |
| "Would this work for my org" | [email](mailto:eugene.korniichuk@gmail.com?subject=doublegate%20—%20deployment%20and%20pricing) |
| A pull request to the site | fine — read the site repo's `AGENTS.md` first, and run `python3 check.py` |

## If you send a pull request to the site

The site has a gate of its own, which is a decent preview of how the product thinks:

```
python3 build.py     # pages/*.html are the sources; the root *.html files are generated
python3 check.py     # must pass — it checks links, anchors, nav parity, alt text,
                     # metadata, and that internal vocabulary never reaches a client page
```

Two rules that will fail a PR fastest:

1. **Never edit a root `*.html` file.** They are generated from `pages/`. Edit the source
   and rebuild, or your change is deleted by the next build.
2. **No internal vocabulary on a client-facing page.** Component identifiers, requirement
   numbers, store filenames, milestone codes and internal jargon all fail the check by
   design — `check.py` holds the current pattern list, which is the authoritative version
   rather than a copy here that would drift. If the plain-language word for something
   doesn't exist yet, that's the actual problem to solve.

## What we won't merge

- **A claim without a source.** Rewriting a cited number to a better-sounding one is the
  single worst change anyone can make here.
- **Marketing language.** "Powerful", "seamless", "revolutionary", "enterprise-grade" —
  the site's own check has a vocabulary bar, and copy that leans on adjectives instead of
  facts fails the sniff test even where the check doesn't catch it.
- **Defensive framing.** "Why this isn't just another memory provider" argues with an
  objection the reader hadn't raised. State what it does instead.
- **A design change without the trade-off named.** Every decision in this project is
  recorded with what it costs and what was rejected. A proposal with no stated cost is
  incomplete, not elegant.

## Attribution

Contributor credit survives. If your correction changes the design, it lands as a dated
decision record naming what changed and why — and if you'd rather not be named, say so and
you won't be.
