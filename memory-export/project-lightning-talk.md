---
name: project-lightning-talk
description: Lightning talk "1-2-3": three detergent-style ads (reference docs, ggarch, team method), red thread how to fix things; state after session 85, slide plan in DECK.md
metadata:
  type: project
---

The user is preparing a lightning talk (Google Slides) tied to the reference doc overhaul and ggarch. Notes, the argument, the story, cautions and the candidate arc are in `~/git/misc/juju-reference/talk/NOTES.md`; read it first.

**Why:** a customer migrated about 400 models and hit owner and credential errors they took for bugs; the point is "document your data model", because an error message is a pointer into the data model. The doc PR is juju/juju 23661; the work is in `~/git/misc/juju-reference` (HANDOFF.md) and `~/git/ggarch`.
**How to apply:** describe slides, logic, and props (no speaker notes; the user copies slides into a work account Claude must not connect to); keep the cautions in NOTES.md (the data model alone would not have prevented the errors; the messages are probably 3.x and unverified in 4.1; the form's reader benefit is not shown). Related: [[project-epic-9635-state]], [[project-entity-reference-form]].

**State after session 85 (2026-10-20):** the talk is three detergent-shaped ads (stain, why, product, clean result, tagline). Slide plan: `~/git/misc/juju-reference/talk/DECK.md` (draft 6); decisions and claims to verify: NOTES.md; next-session launch prompt: `talk/PROMPT.md`. Claude describes slides, logic, and props only and never writes spoken lines ([[feedback-talk-voice]]). Next: settle four open points, build props.
