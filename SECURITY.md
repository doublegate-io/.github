# Security policy

## Reporting a vulnerability

**Email [eugene.korniichuk@gmail.com](mailto:eugene.korniichuk@gmail.com?subject=doublegate%20—%20security)
with `security` in the subject. Do not open a public issue.**

doublegate's most valuable attack surface is still on paper: the trust model the code is
being built against. This policy covers the design and the site today, and each release
joins it as it ships — release 2 in Q2 2027:

| In scope | |
|---|---|
| **The design itself** | a hole in the trust model is the most valuable report we can receive right now. If the gate can be bypassed on paper, it can be bypassed in code |
| **The site** | `doublegate-io.github.io` — anything that lets someone else change what visitors read |
| **Releases** | the published package, service and deployments — covered from the first release |

Expect a reply within a week. We are one person, so that is a realistic commitment rather
than a generous one.

## The reports we most want

The threat model this project exists to address is **content written to manipulate the
system that reviews it.** If you can describe a way for an artifact to reach a readable
state without an independent reviewer signing it, that is the report we most want — and
a hole in the design is worth more than a hole in the code, because it is cheaper to fix.

Concretely, we would rather hear about these before we build them:

- A path from a write to a readable state that skips the review step.
- A way for an author's identity to end up signing the verdict on its own artifact.
- Anything that makes a quarantined artifact reachable from a read path.
- A scan-evasion technique the deterministic checks would miss — bearing in mind that a
  cheap classifier may contribute a finding and may never clear one, which is already a
  recorded decision rather than an oversight.

## What we will do

- Confirm receipt, and tell you plainly whether we think it is a real finding.
- Fix it in the design, and record the fix as a numbered decision with the reasoning — so
  the reason survives the person who found it.
- Credit you, unless you would rather we didn't.

## What we will not do

- Pay a bounty. There is no budget; saying so is more useful than a vague hint that there
  might be.
- Quietly change a design document to make a reported hole disappear. Corrections are
  appended, dated, and the original wording stays — a decision record whose history has
  been edited is not a record.
