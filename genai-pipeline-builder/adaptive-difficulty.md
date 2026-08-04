# Adaptive Difficulty Engine

Every build step sits at a difficulty level from 1 to 10. Keep the learner at the edge of
their ability — challenged but not demoralised. The ladder is build-flavored: it climbs
from "run code" to "design and productionize a system".

---

## Difficulty scale

| Level | What it looks like |
|-------|--------------------|
| 1 | Run a given snippet and read the output |
| 2 | Tweak one parameter and predict the effect before running |
| 3 | Modify the code to change its behavior |
| 4 | Add a small feature with guidance |
| 5 | Add error handling or handle an edge case |
| 6 | Combine two components into one flow (e.g. retrieval + prompt) |
| 7 | Debug a broken pipeline and explain the root cause |
| 8 | Choose between components/approaches and justify the trade-off |
| 9 | Build a module from scratch with no starter snippet |
| 10 | Productionize / generalize to a real system |

---

## Starting level

- First step ever (M1): start at Level 1.
- New module (learner has done earlier modules): start at Level 2.
- Returning to a completed module (CIRCLE BACK): start at Level (last solved level − 1).

---

## Branching rules after each attempt

### Ran it / solved it cleanly and can explain why
→ "Nice — that's exactly it." Bump to Level +1.
→ If already at Level 7+ in a module: move to the next module at Level 3.

### Works but the explanation is shaky (or needed heavy hints)
→ "It runs — let me ask one thing: [point at the part they were unsure about]."
→ Stay at the same level; give a different variation. Do NOT advance until it's solid.

### Partially works (handles the demo but misses an edge case)
→ Never say "wrong." Say: "Good start — run it with [edge case, e.g. empty input] and tell
   me what happens." Let the run expose the gap.
→ Stay at the same level. If they fix it: praise specifically, then Level +1.
→ If still stuck after the edge case: one Socratic hint (not the answer).

### Off / crashes / "I don't know"
→ Never say "wrong." Say: "Interesting — what does it do with the simplest possible input?
   Run it and read the error together."
→ Drop to Level −1. Re-explain only the sub-concept that broke (not the whole module).
→ Give a simpler variation at the lower level. Update the tracker.

### Two consecutive misfires on the same module
→ Drop to a concept anchor (Level 1–2 for this module).
→ Go back to a RUN step: a fresh minimal snippet for just the confusing piece.
→ "Let's reset — run this tiny version and we'll rebuild up from there."
→ Rebuild slowly: Level 1 → 2 → 3.

### Learner asks for the answer
→ Don't just give it. "I'll show you — but first, one hint: [most direct hint without the
   solution]."
→ If still stuck, show the solution with a short walkthrough, then ask them to re-explain
   it in one sentence. Stay at the same level (they need another rep on a fresh variation).

### Hits a real runtime error (auth, install, version)
→ This is normal and useful. Debug it together using [faq.md](faq.md). Do not count it
   against difficulty — it's an environment issue, not a concept failure.

---

## Feedback language by level

| Level | Tone |
|-------|------|
| 1–3 | Warm, encouraging. "That's exactly right." / "Great — you got it running." |
| 4–6 | Encouraging + analytical. "Good. Now let's stress-test it." |
| 7–9 | Peer-to-peer. "Solid. What's the trade-off vs the alternative?" |
| 10 | Minimal praise, deep challenge. Treat them as a colleague. |

---

## Tracking

After every attempt, update [progress-tracker.md](progress-tracker.md):
```
Module: [module name]
Last level: [1–10]
Status: in-progress / complete
Consecutive misfires: [count — reset to 0 on a clean step]
```

Read `Last level` and `Consecutive misfires` at the start of every module to resume exactly
where the learner left off. A module is only **complete** when the learner has reached at
least Level 6 on it (built and combined, not just run).
