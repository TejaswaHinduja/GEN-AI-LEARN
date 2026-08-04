# FAQ & Troubleshooting

Honest answers to the questions learners actually ask, plus the runtime errors they'll
actually hit. When a learner is blocked, check the troubleshooting table first — most
"the concept is broken" moments are really an environment or API issue.

---

## Learning questions

**Do I need to be good at math or machine learning to build LLM apps?**
No. Building GenAI pipelines (the bulk of industry GenAI work) is software engineering:
calling APIs, wrangling data, designing prompts and retrieval. The heavy math lives inside
the models you call. You only need ML intuition (study guide §11) to make good choices and
to fine-tune — and even then, frameworks handle the math.

**Should I use LangChain instead of the raw OpenAI SDK?**
We learn with the raw SDK first on purpose — so you understand what every line does. Once
you've built RAG and an agent by hand, LangChain's abstractions make sense and you can spot
when they help vs hide things. Many production systems use thin wrappers over the raw SDK
for exactly this reason (study guide §7).

**RAG or fine-tuning — which should I learn to reach for?**
RAG for *knowledge* (facts, documents, anything that changes); fine-tuning for *behavior*
(tone, format, a consistent skill). Most real problems are solved with prompting + RAG;
fine-tuning is the smaller, later lever. We build them in that order for that reason.

**Is this enough to put "Generative AI" on my resume?**
The capstone (M11) is a real, deployable RAG/agent service — yes, that's a legitimate
project. The honest framing: you will have *built* GenAI pipelines end-to-end. Describe what
you actually built (architecture, metrics, trade-offs), and you can defend it (study guide
§17). Replace the placeholder projects on the tailored resume with this real one.

**Why are we writing code instead of just reading the study guide?**
Because you cannot fake having built something in an interview. Running the code, breaking
it, and fixing it is what turns "I read about RAG" into "I built RAG and here's what went
wrong." The study guide is the *why*; this skill is the *how*.

**How long does this take?**
There's no schedule. Some sessions are 30 minutes (one module's RUN + INSPECT), some are
hours. The tracker resumes you exactly where you stopped. Depth beats speed.

---

## Troubleshooting (runtime errors)

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `AuthenticationError` / `401` | Key not set or wrong | `echo $OPENAI_API_KEY`; re-`export` it; restart the shell/editor |
| `OPENAI_API_KEY` shows `False` | Env var not exported in this shell | `export OPENAI_API_KEY="sk-..."`; add to `~/.zshrc` to persist |
| `ModuleNotFoundError: openai` | Wrong env or not installed | `source .venv/bin/activate` then `pip install openai` |
| `RateLimitError` / `429` | Too many requests, or no credits | Wait/backoff; check billing has credits; slow down loops |
| `insufficient_quota` | No credits on the account | Add credits in the OpenAI billing dashboard |
| `chromadb` import error | Not installed in this env | `pip install chromadb` inside the active `.venv` |
| `from m5_vectordb import ...` fails | Running from the wrong directory | Run from repo root, or add `genai_lab/` to the path; keep files in `genai_lab/` |
| RAG answers "I don't know" for everything | Empty/irrelevant retrieval | Print the retrieved chunks; check docs were added; check `n_results` |
| RAG hallucinates despite context | Temperature too high / weak grounding prompt | Set `temperature=0`; strengthen the "answer only from context" instruction |
| JSON parse error in M3 | Model didn't return clean JSON | Use `response_format={"type":"json_object"}`, lower temperature, validate + retry |
| `tool_calls` is `None` in M8 | Model chose not to call a tool | Make the request clearly need the tool, or check the tool description |
| M9 install is huge / slow | `torch` is large | Expected; only install for M9; a tiny model (`distilgpt2`) keeps it CPU-friendly |
| Costs creeping up | Long prompts / big loops / large models | Use `gpt-4o-mini`, cap `max_tokens`, cache, log token usage (M2) |

---

## Debugging mindset (teach this)

When something breaks, resist guessing. Isolate:
1. **Print the inputs** — what exactly was sent (prompt, retrieved chunks, args)?
2. **Read the actual error** — the traceback usually names the cause.
3. **Shrink the problem** — run the smallest version that still fails.
4. **Check the boundary** — env/key/install issues masquerade as concept failures.

This is the same isolate-retrieval-vs-generation discipline used in RAG (study guide §6) —
debugging a pipeline means testing each stage on its own.
