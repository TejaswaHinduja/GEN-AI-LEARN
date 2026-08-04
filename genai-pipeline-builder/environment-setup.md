# Environment Setup

Do this once before Module 1. Fix any failure here before writing concept code — a broken
environment masquerades as a broken concept.

---

## 1. Python & virtual environment

Require Python 3.10+. Create an isolated environment so installs don't pollute the system:

```bash
cd /Users/sme/Documents/harshita-interview-prep
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
```

Confirm:
```bash
python --version                 # should print 3.10 or higher
```

> A `.venv` already exists in this repo (used by the resume tooling). Reusing it is fine —
> just install the packages below into it.

---

## 2. Project folder

All module code lives in one growing folder:
```bash
mkdir -p genai_lab
```

Every module adds files here (`m1_first_call.py`, `m2_stream.py`, ...). Do not scatter code
elsewhere — the capstone reuses these files.

---

## 3. Core install (Modules 1–8, 10–11)

```bash
pip install openai numpy chromadb
```

For the capstone service (M11), also:
```bash
pip install fastapi uvicorn
```

---

## 4. Fine-tuning install (Module 9 ONLY)

Install these only when you reach M9, to keep the base environment light:
```bash
pip install torch transformers peft datasets
```

---

## 5. API key

The learner needs an OpenAI API key with available credits. Set it as an environment
variable — **never** write it in a code file, notebook, or prompt.

```bash
export OPENAI_API_KEY="sk-..."   # add to ~/.zshrc to persist across shells
```

Confirm it's visible to Python:
```bash
python -c "import os; print('key set:', bool(os.environ.get('OPENAI_API_KEY')))"
```

The OpenAI SDK reads `OPENAI_API_KEY` automatically, so `OpenAI()` needs no arguments.

### Why env var, not in code
- Keeps the secret out of git history and out of any prompt sent to the model.
- Lets the same code run in dev, CI, and prod with different keys.
- This is the §13/§14 "secrets" practice the learner should be able to explain.

---

## 6. Smoke test

Run the M0 check before starting:
```python
# genai_lab/m0_check.py
import os
from openai import OpenAI

client = OpenAI()
print("Key loaded:", bool(os.environ.get("OPENAI_API_KEY")))

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Reply with the single word: ready"}],
)
print("Model says:", resp.choices[0].message.content)
```

```bash
python genai_lab/m0_check.py
```

Expected: `Key loaded: True` and `Model says: ready` (or similar). If it errors, see
[faq.md](faq.md) before continuing — do not proceed to M1 until this passes.

---

## Quick reference: which install for which module

| Modules | Install |
|---------|---------|
| M1–M3 | `openai` |
| M4–M7, M10 | `openai numpy chromadb` |
| M8 | (already covered) |
| M9 | `torch transformers peft datasets` |
| M11 | `fastapi uvicorn` |
