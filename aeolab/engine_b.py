"""Engine B: a second answer engine, built to disagree with the panel.

Week 4 asks for a rewrite that wins on two engines, because real answer engines are
not one engine. Engine B shares the panel's crawler (the same access rules) and its
model, and differs in everything else:

  Split     windows of two consecutive sentences inside each section, sliding one
            sentence at a time; each window carries its section heading.
  Retrieve  query likelihood with Dirichlet smoothing (mu = 300): a window scores
            high when the prompt's words are dense in it. No fan-out: one search.
  Score     no boosts. An opening "It" costs nothing; a number earns nothing.
  Cite      the top 4 windows from different URLs, at most 2 per domain.

    from aeolab.engine_b import EngineB
    b = EngineB(web)                      # web: a FakeWeb, e.g. aeolab.web2()
    b.ask("Do water filters remove lead?").citations
    rows = b.run(prompts, samples=20, temperature=0.3, seed=1)

Its temperature works like the panel's: each score is multiplied by exp(N(0, t)).
"""

import math
import random
import re
from collections import Counter, defaultdict

from aeolab.llm import FakeModel
from aeolab.panel import MIN_WORDS, Answer, Citation, Panel, Passage, split_passages, tokenize

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


class EngineB:
    def __init__(self, web=None, bot="EngineB", model=None, mu=300, window=2):
        self._crawler = Panel(web, bot=bot)
        self.web = self._crawler.web
        self.model = model or FakeModel()
        self.mu, self.window = mu, window
        self._index = None

    def index(self):
        if self._index is None:
            pages, _ = self._crawler.crawl()
            windows = []
            for url, html in pages.items():
                for p in split_passages(url, html):
                    if len(p.text.split()) < MIN_WORDS:
                        continue
                    sents = [s for s in _SENT.split(p.text) if s.strip()]
                    for i in range(max(1, len(sents) - self.window + 1)):
                        text = " ".join(sents[i:i + self.window])
                        windows.append(Passage(f"{p.id}.{i}", p.url, p.domain, p.heading, text, p.date))
            docs = [Counter(tokenize(w.heading + " " + w.text)) for w in windows]
            coll = Counter()
            for d in docs:
                coll.update(d)
            total = sum(coll.values())
            self._index = {"windows": windows, "docs": docs,
                           "p_coll": {t: c / total for t, c in coll.items()}}
        return self._index

    @property
    def passages(self):
        return self.index()["windows"]

    def search(self, query, k=10):
        ix = self.index()
        terms = [t for t in tokenize(query) if t in ix["p_coll"]]
        if not terms:
            return []
        scored = []
        for i, d in enumerate(ix["docs"]):
            if not any(t in d for t in terms):
                continue
            n = sum(d.values())
            s = sum(math.log((d.get(t, 0) + self.mu * ix["p_coll"][t]) / (n + self.mu)) for t in terms)
            scored.append((s, i))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [(s, ix["windows"][i]) for s, i in scored[:k]]

    def ask(self, prompt, temperature=0.0, seed=0, sample=0, k=4):
        rng = random.Random(f"B|{seed}|{sample}|{prompt}")
        hits = self.search(prompt, k=30)
        rows = []
        for rank, (s, w) in enumerate(hits):
            score = 1 / (1 + rank)
            if temperature > 0:
                score *= math.exp(rng.gauss(0, temperature))
            rows.append((score, rank, w))
        rows.sort(key=lambda r: (-r[0], r[1]))
        cited, urls, per_domain = [], set(), defaultdict(int)
        for _, _, w in rows:
            if w.url in urls or per_domain[w.domain] >= 2:
                continue
            cited.append(w)
            urls.add(w.url)
            per_domain[w.domain] += 1
            if len(cited) == k:
                break
        sentences = self.model.synthesize(prompt, cited)
        return Answer(prompt, sentences, [Citation(w.url, w.domain, w.id, w.heading) for w in cited],
                      {"queries": [prompt], "cited": [w.id for w in cited]})

    def run(self, prompts, samples=1, temperature=0.0, seed=0, run_id="engine-b"):
        rows = []
        for pr in prompts:
            for s in range(samples):
                a = self.ask(pr["prompt"], temperature=temperature, seed=seed, sample=s)
                rows.append({"run_id": run_id, "prompt_id": pr["id"], "sample": s,
                             "cited_urls": [c.url for c in a.citations],
                             "cited_domains": [c.domain for c in a.citations],
                             "answer": " ".join(a.sentences)})
        return rows
