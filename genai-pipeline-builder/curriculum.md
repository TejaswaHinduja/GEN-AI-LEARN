# Curriculum — 12 Modules, One Growing App

Every module extends the **same** `genai_lab/` project. Each entry gives the coach: the
concept (+ study-guide link), a starter snippet to hand over, a run checkpoint, a laddered
set of improve challenges, the extension into the next module, and a mastery check.

Snippets use the OpenAI Python SDK. The model name `gpt-4o-mini` is a sensible cheap
default; `gpt-4o` for harder reasoning. The learner reads the key from `OPENAI_API_KEY`.

> Coach: hand over snippets ONE piece at a time per [build-protocol.md](build-protocol.md).
> The full code per module is here for *your* reference — do not paste a whole module at once.

Theory companion: [genai_study_guide](../LINKEDIN-JOB-APPLIER/state/genai_study_guide_accenture_custom-software-engineer.md)

---

## M0 — Environment setup

**Concept:** a clean, reproducible Python environment with the SDK and an API key.
**Study guide:** §3 (OpenAI API), §13 (env/secrets).

Follow [environment-setup.md](environment-setup.md). Done when this prints a model list
without error:

```python
# genai_lab/m0_check.py
import os
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment
print("Key loaded:", bool(os.environ.get("OPENAI_API_KEY")))
print("SDK OK:", client is not None)
```

**Mastery check:** the learner can explain why the key is read from the environment and
not written in the file.

---

## M1 — First LLM call

**Concept:** the chat messages format (system/user/assistant) and core parameters.
**Study guide:** §2 (how LLMs work), §3 (API & parameters).

**Starter snippet (RUN):**
```python
# genai_lab/m1_first_call.py
from openai import OpenAI

client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a concise assistant. One sentence max."},
        {"role": "user", "content": "Explain what an LLM is to a 10-year-old."},
    ],
    temperature=0.7,
)
print(resp.choices[0].message.content)
print("Tokens used:", resp.usage.total_tokens)
```

**INSPECT tweaks:** change the system prompt to a pirate persona; set `temperature=0` and
run twice (note determinism); set `temperature=2.0` (note chaos); set `max_tokens=5`.

**IMPROVE ladder:**
- L3: turn it into a function `ask(question: str) -> str`.
- L4: accept the user question from `input()` / a CLI arg.
- L5: wrap the API call in try/except and print a friendly message on failure.

**EXTEND → M2:** "Notice the answer appears all at once after a pause. Real chat apps stream
it. Let's make it feel instant."

**Mastery check:** learner can explain the role of `system` vs `user` and what `temperature`
does, in their own words.

---

## M2 — Streaming + cost/latency awareness

**Concept:** token-by-token streaming; tokens as the unit of cost and latency.
**Study guide:** §2 (tokens), §3 (streaming, cost/latency control).

**Starter snippet (RUN):**
```python
# genai_lab/m2_stream.py
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a 4-line poem about databases."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
print()
```

**INSPECT tweaks:** ask for a longer output and watch it stream; compare perceived speed
vs M1's blocking call.

**IMPROVE ladder:**
- L4: accumulate the streamed text into a single string and return it.
- L5: count output tokens and estimate cost (give them the per-1K price as a constant).
- L6: add a `usage`-based token log written to a file after each call.

**EXTEND → M3:** "You can get any answer now — but can you get a *reliable, well-formatted*
answer every time? That's prompt engineering."

**Mastery check:** learner can state why streaming improves UX without reducing total cost,
and what drives cost (input + output tokens).

---

## M3 — Prompt engineering

**Concept:** few-shot, chain-of-thought, structured (JSON) output, injection defense.
**Study guide:** §4 (prompt engineering).

**Starter snippet (RUN) — structured extraction with JSON mode:**
```python
# genai_lab/m3_prompt.py
import json
from openai import OpenAI

client = OpenAI()

SYSTEM = (
    "Extract the person's name, company, and role from the text. "
    "Respond ONLY with JSON: {\"name\": ..., \"company\": ..., \"role\": ...}. "
    "If a field is missing, use null."
)

text = "Hi, I'm Harshita Shekhawat, a software engineer at Pratham Software."

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": text},
    ],
    temperature=0,
    response_format={"type": "json_object"},
)
data = json.loads(resp.choices[0].message.content)
print(data)
```

**INSPECT tweaks:** feed text with a missing field; feed a sentence with two people; remove
`response_format` and see if parsing still holds.

**IMPROVE ladder:**
- L4: add 2 few-shot examples in the system prompt and measure consistency.
- L5: validate the parsed JSON against required keys; retry once on failure.
- L6: add a chain-of-thought variant for a reasoning task (hidden reasoning, final answer only).
- L7: defend against prompt injection — wrap user text in delimiters and instruct the model
  to treat it as data; test with input containing "ignore previous instructions".

**EXTEND → M4:** "Your tool answers from text you paste in. But the answer often lives in a
big document the model has never seen. To find the right passage, we need to represent
meaning as numbers — embeddings."

**Mastery check:** learner can force valid JSON reliably and explain one prompt-injection
defense.

---

## M4 — Embeddings & semantic search

**Concept:** embeddings as meaning-vectors; cosine similarity; semantic vs keyword search.
**Study guide:** §5 (embeddings & vector DBs).

**Starter snippet (RUN) — tiny in-memory semantic search:**
```python
# genai_lab/m4_search.py
import numpy as np
from openai import OpenAI

client = OpenAI()

docs = [
    "Refunds are processed within 5-7 business days.",
    "Our office is open Monday to Friday, 9am to 6pm.",
    "You can reset your password from the account settings page.",
]

def embed(texts):
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return np.array([d.embedding for d in resp.data])

def cosine(a, b):
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))

doc_vecs = embed(docs)
query = "how long does it take to get my money back?"
q = embed([query])[0]

scores = [cosine(q, dv) for dv in doc_vecs]
best = int(np.argmax(scores))
print("Best match:", docs[best], "\nScore:", round(scores[best], 3))
```

**INSPECT tweaks:** query with words that share NO keywords with the answer (proves it's
semantic); add an unrelated query and check the top score is low.

**IMPROVE ladder:**
- L4: return the top-k matches instead of just the best.
- L5: handle the empty-docs case and very-low-score case ("no good match").
- L6: compare cosine vs dot product on normalized vectors and explain why they rank the same.

**EXTEND → M5:** "Re-embedding every doc on every query is wasteful, and an in-memory list
won't survive a restart or scale to 100k docs. We need a vector database."

**Mastery check:** learner can explain why semantic search beats keyword search with a
concrete example.

---

## M5 — Vector database

**Concept:** persisting embeddings; ANN search; metadata.
**Study guide:** §5 (vector DBs, indexes).

**Starter snippet (RUN) — Chroma (local, zero-config):**
```python
# genai_lab/m5_vectordb.py
import chromadb
from openai import OpenAI

client = OpenAI()
chroma = chromadb.PersistentClient(path="genai_lab/chroma_store")
col = chroma.get_or_create_collection("kb")

docs = [
    "Refunds are processed within 5-7 business days.",
    "Our office is open Monday to Friday, 9am to 6pm.",
    "You can reset your password from the account settings page.",
]

def embed(texts):
    r = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in r.data]

if col.count() == 0:
    col.add(ids=[f"d{i}" for i in range(len(docs))],
            documents=docs, embeddings=embed(docs))

q = "when do I get my refund?"
res = col.query(query_embeddings=embed([q]), n_results=2)
print(res["documents"])
```

**INSPECT tweaks:** rerun the script (note it doesn't re-add — persistence works); query
with `n_results=1` vs `3`; add a metadata field and filter on it.

**IMPROVE ladder:**
- L4: add `metadatas` (e.g. `{"category": "billing"}`) and filter queries with `where=`.
- L5: write an `upsert` path so updating a doc replaces its vector by stable id.
- L6: compare FAISS (in-process library) vs Chroma and articulate when you'd pick each.

**EXTEND → M6:** "Now you can find relevant text fast. Let's feed those passages to the LLM
so it answers from your data with citations — that's RAG."

**Mastery check:** learner can explain what an ANN index buys you and why you store metadata.

---

## M6 — RAG v1

**Concept:** chunk → embed → retrieve → augment → grounded answer with citations.
**Study guide:** §6 (RAG).

**Starter snippet (RUN) — minimal RAG over the M5 collection:**
```python
# genai_lab/m6_rag.py
from openai import OpenAI
from m5_vectordb import col, embed  # reuse the collection + embed()

client = OpenAI()

def rag_answer(question: str) -> str:
    res = col.query(query_embeddings=embed([question]), n_results=3)
    chunks = res["documents"][0]
    context = "\n".join(f"[{i}] {c}" for i, c in enumerate(chunks))
    prompt = (
        "Answer using ONLY the context. If it's not there, say 'I don't know'. "
        "Cite the [number] you used.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content

print(rag_answer("how long do refunds take?"))
```

**INSPECT tweaks (critical):** ask something NOT in the docs ("what's your CEO's name?") —
does it say "I don't know" or hallucinate? Raise temperature and watch grounding weaken.

**IMPROVE ladder:**
- L4: load real documents from a folder and chunk them (fixed size + overlap).
- L5: handle empty retrieval and enforce the "I don't know" path.
- L6: return the citations as structured data alongside the answer.
- L7: deliberately break it (k=0, or shuffle context) and have them diagnose the failure.

**EXTEND → M7:** "It works on easy questions. But retrieval quality is where RAG lives or
dies. Let's measure and improve it."

**Mastery check:** learner can draw the full RAG pipeline and name where hallucination is
controlled.

---

## M7 — RAG hardening

**Concept:** chunking strategy, reranking, hybrid search, retrieval evaluation,
"lost in the middle".
**Study guide:** §5 (reranking, hybrid), §6 (chunking, advanced patterns), §10 (eval).

**Starter focus (RUN):** an experiment harness, not one snippet — have them build a small
eval set of (question → expected source) pairs and measure recall@k.

```python
# genai_lab/m7_eval.py
from m6_rag import col, embed

eval_set = [
    ("how long do refunds take?", "d0"),
    ("when can I reach the office?", "d1"),
    ("I forgot my password", "d2"),
]

def recall_at_k(k=3):
    hits = 0
    for q, expected_id in eval_set:
        res = col.query(query_embeddings=embed([q]), n_results=k)
        if expected_id in res["ids"][0]:
            hits += 1
    return hits / len(eval_set)

print("recall@3:", recall_at_k(3))
```

**IMPROVE ladder:**
- L5: experiment with chunk size/overlap and re-measure recall — plot the trade-off.
- L6: add a reranking step (re-score top-k candidates) and compare recall/precision.
- L7: add keyword (substring/BM25-style) search and merge with vector results (hybrid).
- L8: have them justify a chunking + retrieval config choice with their own numbers.

**EXTEND → M8:** "Your system answers questions. Next, let it *act* — call tools and take
multi-step actions. That's function calling and agents."

**Mastery check:** learner can isolate a RAG failure to retrieval vs generation and back a
config change with a metric.

---

## M8 — Function calling & a simple agent

**Concept:** function/tool calling; the ReAct loop; guardrails.
**Study guide:** §8 (agents, tools, function calling).

**Starter snippet (RUN) — one tool, manual loop:**
```python
# genai_lab/m8_agent.py
import json
from openai import OpenAI

client = OpenAI()

def get_weather(city: str) -> str:
    fake = {"pune": "32C sunny", "london": "14C rainy"}
    return fake.get(city.lower(), "unknown")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {"type": "object",
                       "properties": {"city": {"type": "string"}},
                       "required": ["city"]},
    },
}]

msgs = [{"role": "user", "content": "What's the weather in Pune?"}]
resp = client.chat.completions.create(model="gpt-4o-mini", messages=msgs, tools=tools)
call = resp.choices[0].message.tool_calls[0]
args = json.loads(call.function.arguments)
result = get_weather(**args)
msgs += [resp.choices[0].message,
         {"role": "tool", "tool_call_id": call.id, "content": result}]
final = client.chat.completions.create(model="gpt-4o-mini", messages=msgs)
print(final.choices[0].message.content)
```

**INSPECT tweaks:** ask about a city not in the fake data; ask something needing no tool
(does it skip the call?).

**IMPROVE ladder:**
- L5: wrap into a loop that handles multiple/sequential tool calls until done.
- L6: add a second tool (e.g. a calculator) and let the model choose.
- L7: add guardrails — max iterations, validate args, refuse destructive actions.
- L8: discuss when an agent is overkill vs a fixed chain (have them argue it).

**EXTEND → M9:** "Prompting + tools shape *behavior at runtime*. Sometimes you want behavior
baked into the model itself — that's fine-tuning."

**Mastery check:** learner can explain why the model proposes a call but your code executes
it, and name two agent guardrails.

---

## M9 — Fine-tuning with LoRA/PEFT

**Concept:** when fine-tuning beats RAG/prompting; LoRA/PEFT; data prep; overfitting.
**Study guide:** §9 (fine-tuning, LoRA, PEFT).
**Note:** this module uses Hugging Face + PEFT (open-source) so the LoRA internals are
visible. Keep it minimal — the *concepts* and *when-to-use* matter more than a big run.
Install only here (see [environment-setup.md](environment-setup.md)).

**Starter focus (RUN):** first, decision-making, not code. Give them 3 scenarios and have
them pick prompting / RAG / fine-tuning and justify (answers in study guide §9).

Then a minimal conceptual LoRA config to read and run on a tiny dataset:
```python
# genai_lab/m9_lora.py  (conceptual — small model, tiny data)
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

base = "distilgpt2"  # tiny, CPU-friendly for a first run
model = AutoModelForCausalLM.from_pretrained(base)
tok = AutoTokenizer.from_pretrained(base)

lora = LoraConfig(r=8, lora_alpha=16, target_modules=["c_attn"], lora_dropout=0.05)
model = get_peft_model(model, lora)
model.print_trainable_parameters()  # observe: <1% of params are trainable
```

**INSPECT:** read the `print_trainable_parameters()` output — the headline is how few params
LoRA trains. Change `r` and watch the trainable count move.

**IMPROVE ladder:**
- L5: prepare a tiny instruction dataset (a handful of input→output pairs) in the right format.
- L6: run a few training steps and compare a generation before vs after.
- L7: explain catastrophic forgetting and one way to mitigate it.
- L8: argue "fine-tune for tone, RAG for facts" with a concrete product example.

**EXTEND → M10:** "You can build and tune systems now. But how do you *know* one version is
better than another? You need evaluation."

**Mastery check:** learner can explain *why* low-rank works and when to fine-tune vs RAG.

---

## M10 — Evaluation

**Concept:** golden datasets, faithfulness/groundedness, LLM-as-judge, regression testing.
**Study guide:** §10 (evaluating GenAI systems).

**Starter snippet (RUN) — LLM-as-judge for faithfulness:**
```python
# genai_lab/m10_eval.py
from openai import OpenAI
from m6_rag import rag_answer

client = OpenAI()

def judge_faithfulness(question, answer, context):
    prompt = (
        "Is the ANSWER fully supported by the CONTEXT? Reply only 'YES' or 'NO'.\n"
        f"CONTEXT: {context}\nQUESTION: {question}\nANSWER: {answer}"
    )
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()

a = rag_answer("how long do refunds take?")
print("Answer:", a)
print("Faithful?", judge_faithfulness("how long do refunds take?", a,
      "Refunds are processed within 5-7 business days."))
```

**INSPECT tweaks:** feed a deliberately wrong answer and confirm the judge says NO; swap
answer order to expose position bias.

**IMPROVE ladder:**
- L5: run the judge across the M7 eval set and report a faithfulness score.
- L6: add answer-relevance as a second metric; combine into a small report.
- L7: discuss LLM-as-judge biases and how to calibrate against human labels.
- L8: wire one eval assertion so it could run in CI as a regression gate.

**EXTEND → M11:** "Everything works locally. The last step is making it a real service others
can call — and keeping it cheap, fast, and reliable."

**Mastery check:** learner can name a retrieval metric, a generation metric, and one
LLM-as-judge pitfall.

---

## M11 — Capstone: productionize

**Concept:** serving, streaming over HTTP, containerization, caching, secrets, observability.
**Study guide:** §13 (cloud/DevOps), §14 (safety/security).

**Goal:** wrap the RAG/agent into a real service. This is a portfolio-grade project — it
should become one of the learner's actual resume projects (replacing the placeholder GenAI
projects on the tailored resume).

**Starter snippet (RUN) — FastAPI endpoint with streaming:**
```python
# genai_lab/app.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
from m6_rag import col, embed

app = FastAPI()
client = OpenAI()

@app.get("/ask")
def ask(q: str):
    res = col.query(query_embeddings=embed([q]), n_results=3)
    context = "\n".join(res["documents"][0])
    def gen():
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user",
                       "content": f"Answer from context only.\n{context}\nQ: {q}"}],
            stream=True,
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
    return StreamingResponse(gen(), media_type="text/plain")
```
Run with: `uvicorn genai_lab.app:app --reload`, then open `/ask?q=refund+time`.

**IMPROVE ladder (capstone build-out):**
- L6: add response caching (exact-match) keyed on the question.
- L7: add a `Dockerfile`, build the image, run the container.
- L7: add per-request rate limiting + a token/cost log.
- L8: add input validation + a safety guardrail (refuse empty/abusive input).
- L9: add a `/health` endpoint, structured logging, and a tiny eval that runs in CI.
- L10: write a short README framing it as a resume project (problem, architecture, metrics,
  trade-offs) — see study guide §17 for the STAR structure.

**Mastery check:** the learner can demo the running service, explain its architecture and
failure modes, and articulate cost/latency trade-offs — i.e. defend it in an interview.

---

## After the capstone

- Help the learner turn the capstone into a real resume bullet (study guide §17) and replace
  the placeholder GenAI projects in
  [tailored_accenture_custom-software-engineer.tex](../LINKEDIN-JOB-APPLIER/state/tailored_accenture_custom-software-engineer.tex).
- Keep circling back to weak concepts via the spaced-repetition log.
- Optional stretch: swap Chroma → a managed vector DB, add multi-tenant metadata filtering,
  or add a reranker model.
