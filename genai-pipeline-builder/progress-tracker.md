# Progress Tracker

The skill reads and updates this file at the start and end of every session.
Do not delete sections — just update the values. This is the source of truth for resuming.

---

## Session state

```
Current module:        M0 — Environment setup (not started)
Current level:         1
Consecutive misfires:  0
Modules complete:      0 / 12
Total sessions:        0
Mode:                  lean
```

---

## Module checklist

A module is complete only when the learner reaches Level 6+ on it (built and combined,
not just ran a snippet). Record the last difficulty level reached.

```
[ ] M0  Environment setup            last level: -    status: not started
[ ] M1  First LLM call               last level: -    status: not started
[ ] M2  Streaming + cost/latency     last level: -    status: not started
[ ] M3  Prompt engineering           last level: -    status: not started
[ ] M4  Embeddings & semantic search last level: -    status: not started
[ ] M5  Vector database              last level: -    status: not started
[ ] M6  RAG v1                       last level: -    status: not started
[ ] M7  RAG hardening                last level: -    status: not started
[ ] M8  Function calling & agent     last level: -    status: not started
[ ] M9  Fine-tuning (LoRA/PEFT)      last level: -    status: not started
[ ] M10 Evaluation                   last level: -    status: not started
[ ] M11 Capstone: productionize      last level: -    status: not started
```

---

## Skills unlocked (spaced-repetition log)

Add a concept here the moment the learner masters it, with `reviews: 0`. Every 3–4 modules,
pick one with `reviews: 0` (or last reviewed 4+ modules ago) for a surprise circle-back,
then increment its review count.

```
(empty — fills in as modules are completed)

# format:
# - concept: <name>        | from: <module> | reviews: 0 | last reviewed: -
```

Concepts to log as they're mastered (reference list):
- system vs user prompt; temperature (M1)
- streaming; tokens drive cost (M2)
- few-shot; JSON mode; injection defense (M3)
- embeddings; cosine similarity; semantic vs keyword (M4)
- vector DB persistence; metadata filtering; ANN (M5)
- RAG pipeline; grounding; citations (M6)
- chunking; reranking; hybrid search; recall@k (M7)
- function calling; ReAct loop; agent guardrails (M8)
- when to fine-tune; LoRA low-rank; catastrophic forgetting (M9)
- faithfulness; LLM-as-judge; regression gate (M10)
- serving; caching; Docker; secrets; observability (M11)

---

## Capstone / resume link

```
Capstone app built:    no
README written:        no
Added to resume:       no   (target: replace placeholder GenAI projects in
                             ../LINKEDIN-JOB-APPLIER/state/tailored_accenture_custom-software-engineer.tex)
```

---

## Session notes

```
(Session 0 — not yet started. Add a short note per session: what was built, where they
got stuck, what to revisit next time.)
```
