"""The scripted fake model. Every model call in every test goes through this.

A real answer engine uses a language model twice: to rewrite your prompt into several
searches (query fan-out), and to write the answer from the passages it found. This fake
does both from scripts in aeolab/data/, so a run is repeatable and costs nothing.

    model = FakeModel()
    model.fan_out("Do water filters remove lead?")      # -> list of sub-queries
    model.synthesize(query, passages)                    # -> list of answer sentences

What it does NOT do: understand anything. synthesize() lifts the first sentence of each
passage it is handed, which is a fair model of what a real engine quotes, and then adds
any scripted extra sentence - a claim no passage supports, as real models sometimes make.
"""

import json
import re
from pathlib import Path

DATA = Path(__file__).parent / "data"
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


def first_sentence(text):
    text = text.strip()
    return _SENTENCE_END.split(text, maxsplit=1)[0] if text else ""


class FakeModel:
    def __init__(self, fanout=None, extras=None):
        self._fanout = fanout if fanout is not None else json.loads((DATA / "fanout.json").read_text())
        self._extras = extras if extras is not None else json.loads((DATA / "extras.json").read_text())
        self.calls = []

    def fan_out(self, query):
        """The sub-queries an engine would search for this prompt, original first.
        An unscripted prompt fans out to itself only."""
        self.calls.append(("fan_out", query))
        return [query] + [q for q in self._fanout.get(query, []) if q != query]

    def synthesize(self, query, passages):
        """passages: dicts or objects with a 'text'. Returns answer sentences in order."""
        self.calls.append(("synthesize", query))
        out = []
        for p in passages:
            text = p["text"] if isinstance(p, dict) else p.text
            s = first_sentence(text)
            if s and s not in out:
                out.append(s)
        if query in self._extras:
            out.append(self._extras[query])
        return out
