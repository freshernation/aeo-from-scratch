# Day zero

About an hour. Do it before week 1, not on Monday morning.

---

## 1. Python 3.12 or newer

```bash
python3 --version
```

## 2. Your own repository

Make your own copy of this repository on GitHub (**Use this template**), then clone it:

```bash
git clone https://github.com/YOUR-USERNAME/aeo-from-scratch.git
cd aeo-from-scratch
```

## 3. The environment

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

The second install makes `aeolab` importable from every week's folder.

## 4. Check it

```bash
python3 check_setup.py
pytest aeolab -q
```

Every line of `check_setup.py` should say OK except the last, about your baseline.
`pytest aeolab` should pass: that is the given code. `pytest week-01` should fail,
because you have not written week 1 yet.

## 5. Meet the panel

```bash
python3 -c "from aeolab.panel import Panel; a = Panel().ask('Do water filters remove lead?'); print(a.sentences); print([c.url for c in a.citations])"
```

That is the answer engine the course measures against. Read the docstring at the top of
`aeolab/panel.py` before Monday: it is one page, and every rule in it is marked with
where it comes from.

## 6. Your baseline interview

Open a fresh chat with any capable AI. Paste the whole of `ai/advisor.md`. Answer its
questions honestly. It will also ask which track you are on. At the end it prints a
`BASELINE` block. Paste it into `logs/baseline.md`, replacing the bracketed lines, and push.

## 7. Accounts and keys

None until week 7. In week 7 you may add one or more of these to a `.env` file (never
committed) for the optional live runs:

| Variable | For |
|---|---|
| `ANTHROPIC_API_KEY` | Claude with web search (or log in with `ant auth login`) |
| `OPENAI_API_KEY` and `OPENAI_MODEL` | ChatGPT's web search; choose a current model that supports it |
| `PERPLEXITY_API_KEY` | Perplexity's Sonar |

Load them into your shell before a live run with `set -a; source .env; set +a`.
Week 7 day 2 teaches you to price a run before you make it. You can finish the course
without any key: every test runs offline.

## 8. Week 8

You need a website you may change: your own, an employer's with written permission, or one
your instructor provides. Choose it before week 8.
