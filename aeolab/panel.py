"""The panel: the answer engine the whole course measures against.

It is a model of an answer engine, small enough to read in one sitting. It is not any
real engine. Every rule below says where it comes from - a published description, a
vendor's documentation, or "course assumption" when it is our guess. Week 7 checks which
rules hold on live engines.

    panel = Panel()                              # the seeded web, as bot "PanelBot"
    ans = panel.ask("Do water filters remove lead?")
    ans.sentences, ans.citations, ans.trace
    rows = panel.run(prompts, samples=10, temperature=0.3, seed=1)

The pipeline, and the rule at each step:

  1 Crawl    Start at each site's / and sitemap; follow same-site links.
             R1  obeys robots.txt for its user agent, RFC 9309 (longest match wins).
                 Source: the AI vendors' bot pages say their search bots obey robots.txt.
             R2  skips anything that is not status 200: 403, 404; follows up to 5 redirects.
             R3  skips pages marked noindex, in a meta tag or an X-Robots-Tag header.
             R4  does not run JavaScript: content that only arrives by script is not seen.
                 Source: published crawler studies; most AI crawlers fetch HTML only.
             R5  skips a page whose canonical link points at a different URL.
  2 Split    Each page becomes passages: one per h2 or h3 section, plus the text before
             the first heading. Navigation, header and footer are ignored. Passages under
             12 words are dropped as too thin to quote (course assumption).
             Source: engines retrieve and quote passages, not whole pages (GEO paper).
  3 Fan out  The model turns the prompt into several searches.
             Source: Google's description of AI Mode's "query fan-out".
  4 Retrieve TF-IDF cosine, top 10 passages per search, fused by reciprocal rank (k=60).
  5 Score    fused score x boosts:
             R6  self-contained: a passage opening with It/This/They/These... x 0.7
                 (course assumption: a lifted passage must make sense alone)
             R7  answer-first: first sentence <= 35 words and holds at least half the
                 prompt's terms x 1.25 (course assumption)
             R8  specific: x (1 + 0.08 per sentence-level number, up to 3)
                 Source: GEO paper - adding statistics raised visibility.
             R9  corroborated: x (1 + 0.04 per other domain linking to this domain, up to 5)
                 (course assumption, modelled on link-based authority)
             R10 fresh: a page dated more than two years before `today` x 0.85
                 (course assumption)
             temperature > 0 multiplies each score by exp(N(0, temperature)): real
             engines do not give the same answer twice.
  6 Cite     The top 4 passages from different URLs, at most 2 per domain.
  7 Answer   The model writes sentences from the cited passages.

JSON-LD is read for dates only. Its text is not indexed - see week 5.
"""

import math
import random
import re
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from datetime import date
from urllib.parse import urljoin, urldefrag

from bs4 import BeautifulSoup

from aeolab.fakeweb import FakeWeb, split_url
from aeolab.llm import FakeModel, first_sentence

STOPWORDS = frozenset("""a about above after again all am an and any are as at be because been
before being below between both but by can could did do does doing down during each few for from
further had has have having he her here hers him his how i if in into is it its itself just me
more most my no nor not now of off on once only or other our out over own same she should so some
such than that the their them then there these they this those through to too under until up very
was we were what when where which while who whom why will with would you your yours""".split())

MIN_WORDS = 12
PRONOUN_OPENERS = ("it", "this", "they", "these", "those", "that", "he", "she")


def tokenize(text):
    """Lowercase words and numbers, stopwords dropped, a trailing plural 's' removed."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    out = []
    for w in words:
        if w in STOPWORDS:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(w)
    return out


# ------------------------------------------------------------------ robots.txt (R1)

def _robots_groups(text):
    groups, agents, rules, last_was_agent = [], [], [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (s.strip() for s in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if not last_was_agent and agents:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
            last_was_agent = True
        elif key in ("allow", "disallow"):
            if agents:
                rules.append((key, value))
            last_was_agent = False
        else:
            last_was_agent = False
    if agents:
        groups.append((agents, rules))
    return groups


def _rule_matches(pattern, path):
    regex = "".join(".*" if c == "*" else re.escape(c) for c in pattern.rstrip("$"))
    return re.match(regex + ("$" if pattern.endswith("$") else ""), path) is not None


def robots_allows(robots_text, user_agent, path):
    """RFC 9309: the group naming this agent (or *), longest matching rule, Allow wins ties."""
    if path == "/robots.txt":
        return True
    token = user_agent.split("/")[0].lower()
    groups = _robots_groups(robots_text)
    mine = [r for agents, r in groups if token in agents]
    if not mine:
        mine = [r for agents, r in groups if "*" in agents]
    rules = [rule for g in mine for rule in g if rule[1] != ""]
    best = None
    for kind, pattern in rules:
        if _rule_matches(pattern, path):
            length = len(pattern)
            if best is None or length > best[0] or (length == best[0] and kind == "allow"):
                best = (length, kind)
    return best is None or best[1] == "allow"


# ------------------------------------------------------------------ data

@dataclass
class Passage:
    id: str
    url: str
    domain: str
    heading: str
    text: str
    date: str = ""

    @property
    def first_sentence(self):
        return first_sentence(self.text)


@dataclass
class Citation:
    url: str
    domain: str
    passage_id: str
    heading: str


@dataclass
class Answer:
    prompt: str
    sentences: list
    citations: list
    trace: dict = field(default_factory=dict)

    @property
    def cited_domains(self):
        return [c.domain for c in self.citations]


def _block_text(el):
    if el.name == "table":
        heads = [th.get_text(" ", strip=True) for th in el.find_all("th")]
        rows = []
        for tr in el.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
            if cells:
                rows.append(", ".join(f"{h} {c}".strip() if h else c for h, c in zip(heads or [""] * len(cells), cells)))
        return ". ".join(rows) + "."
    if el.name in ("ul", "ol"):
        return "; ".join(li.get_text(" ", strip=True) for li in el.find_all("li")) + "."
    return el.get_text(" ", strip=True)


def page_date(soup):
    t = soup.find("time")
    if t and t.get("datetime"):
        return t["datetime"][:10]
    m = re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', str(soup))
    return m.group(1) if m else ""


def split_passages(url, html):
    """Passages of one page, in order. Used by the panel; week 1 builds its own."""
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("article") or soup.find("main") or soup.body
    if body is None:
        return []
    domain = split_url(url)[0]
    when = page_date(soup)
    h1 = body.find("h1")
    heading = h1.get_text(" ", strip=True) if h1 else (soup.title.get_text(strip=True) if soup.title else url)
    passages, buf = [], []

    def flush():
        text = " ".join(t for t in buf if t).strip()
        if text:
            passages.append(Passage(f"{url}#{len(passages)}", url, domain, heading, text, when))

    for el in body.find_all(["h2", "h3", "p", "ul", "ol", "table"]):
        if el.find_parent(["ul", "ol", "table"]) is not None:
            continue
        if el.name in ("h2", "h3"):
            flush()
            buf = []
            heading = el.get_text(" ", strip=True)
        elif not (el.name == "p" and "meta" in (el.get("class") or [])):
            buf.append(_block_text(el))
    flush()
    return passages


# ------------------------------------------------------------------ the engine

class Panel:
    def __init__(self, web=None, bot="PanelBot", model=None, today="2026-10-01"):
        self.web = web or FakeWeb()
        self.bot = bot
        self.model = model or FakeModel()
        self.today = date.fromisoformat(today)
        self._index = None

    # 1. crawl --------------------------------------------------------------
    def fetch_final(self, url, max_hops=5):
        """Follow redirects. Returns (response, hops) - response is None on a loop or too many hops."""
        seen = []
        for _ in range(max_hops + 1):
            r = self.web.fetch(url, user_agent=self.bot)
            if r.status in (301, 302, 307, 308):
                seen.append(url)
                url = urljoin(url, r.headers.get("location", ""))
                if url in seen:
                    return None, seen
                continue
            return r, seen
        return None, seen

    def readable(self, url):
        """(True, '') if the panel can index this URL, else (False, reason)."""
        domain, path = split_url(url)
        robots = self.web.fetch(f"https://{domain}/robots.txt", user_agent=self.bot)
        robots_text = robots.text if robots.status == 200 else ""
        if not robots_allows(robots_text, self.bot, path):
            return False, "robots"
        r, hops = self.fetch_final(url)
        if r is None:
            return False, "redirect-loop"
        if r.status != 200:
            return False, f"status-{r.status}"
        final_path = split_url(r.url)[1]
        if hops and not robots_allows(robots_text, self.bot, final_path):
            return False, "robots"
        if "noindex" in r.headers.get("x-robots-tag", "").lower():
            return False, "noindex-header"
        soup = BeautifulSoup(r.text, "html.parser")
        meta = soup.find("meta", attrs={"name": "robots"})
        if meta and "noindex" in meta.get("content", "").lower():
            return False, "noindex-meta"
        canon = soup.find("link", rel="canonical")
        if canon and canon.get("href") and canon["href"].rstrip("/") != r.url.rstrip("/"):
            return False, "canonical-elsewhere"
        if not split_passages(r.url, r.text):
            return False, "no-text"
        return True, ""

    def crawl(self):
        pages, inbound = {}, defaultdict(set)
        for domain in self.web.domains():
            start = [f"https://{domain}/"]
            sm = self.web.fetch(f"https://{domain}/sitemap.xml", user_agent=self.bot)
            if sm.status == 200:
                start += re.findall(r"<loc>(.*?)</loc>", sm.text)
            queue, seen = deque(start), set(start)
            while queue and len(seen) < 500:
                url = queue.popleft()
                ok, _ = self.readable(url)
                if not ok:
                    continue
                r, _ = self.fetch_final(url)
                final = r.url
                if final in pages:
                    continue
                pages[final] = r.text
                soup = BeautifulSoup(r.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    link = urldefrag(urljoin(final, a["href"]))[0]
                    target = split_url(link)[0]
                    if target == domain and link not in seen:
                        seen.add(link)
                        queue.append(link)
                    elif target and target != domain:
                        inbound[target].add(domain)
        return pages, inbound

    def index(self):
        if self._index is None:
            pages, inbound = self.crawl()
            passages = [p for url, html in pages.items() for p in split_passages(url, html)
                        if len(p.text.split()) >= MIN_WORDS]
            docs = [Counter(tokenize(p.heading + " " + p.text)) for p in passages]
            df = Counter(t for d in docs for t in d)
            n = len(docs)
            idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
            vecs = []
            for d in docs:
                v = {t: (1 + math.log(c)) * idf[t] for t, c in d.items()}
                norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
                vecs.append({t: x / norm for t, x in v.items()})
            self._index = {"pages": pages, "inbound": inbound, "passages": passages,
                           "vecs": vecs, "idf": idf}
        return self._index

    @property
    def passages(self):
        return self.index()["passages"]

    def inbound_domains(self, domain):
        return sorted(self.index()["inbound"].get(domain, set()))

    # 4. retrieve -----------------------------------------------------------
    def search(self, query, k=10):
        """Plain TF-IDF search: the top k passages for one query, no boosts."""
        ix = self.index()
        q = Counter(tokenize(query))
        qv = {t: (1 + math.log(c)) * ix["idf"].get(t, 0.0) for t, c in q.items()}
        scored = []
        for i, v in enumerate(ix["vecs"]):
            s = sum(w * v.get(t, 0.0) for t, w in qv.items())
            if s > 0:
                scored.append((s, i))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [ix["passages"][i] for _, i in scored[:k]]

    # 5. score --------------------------------------------------------------
    def boosts(self, passage, prompt):
        b = {}
        words = passage.text.split()
        b["self_contained"] = 0.7 if words and words[0].lower().strip(",.:") in PRONOUN_OPENERS else 1.0
        first = passage.first_sentence
        terms = set(tokenize(prompt))
        hit = len(terms & set(tokenize(first))) / len(terms) if terms else 0
        b["answer_first"] = 1.25 if len(first.split()) <= 35 and hit >= 0.5 else 1.0
        numbers = len(re.findall(r"\d+(?:[.,]\d+)*", passage.text))
        b["specific"] = 1 + 0.08 * min(numbers, 3)
        b["corroborated"] = 1 + 0.04 * min(len(self.index()["inbound"].get(passage.domain, ())), 5)
        old = passage.date and (self.today - date.fromisoformat(passage.date)).days > 730
        b["fresh"] = 0.85 if old else 1.0
        return b

    def ask(self, prompt, temperature=0.0, seed=0, sample=0, k=4):
        queries = self.model.fan_out(prompt)
        fused = defaultdict(float)
        by_id = {}
        for q in queries:
            for rank, p in enumerate(self.search(q, k=10), start=1):
                fused[p.id] += 1 / (60 + rank)
                by_id[p.id] = p
        rng = random.Random(f"{seed}|{sample}|{prompt}")
        rows = []
        for pid, rrf in fused.items():
            p = by_id[pid]
            b = self.boosts(p, prompt)
            score = rrf * math.prod(b.values())
            if temperature > 0:
                score *= math.exp(rng.gauss(0, temperature))
            rows.append({"id": pid, "url": p.url, "domain": p.domain, "heading": p.heading,
                         "rrf": round(rrf, 5), "boosts": b, "score": score})
        rows.sort(key=lambda r: (-r["score"], r["id"]))
        cited, urls, per_domain = [], set(), Counter()
        for r in rows:
            if r["url"] in urls or per_domain[r["domain"]] >= 2:
                continue
            cited.append(by_id[r["id"]])
            urls.add(r["url"])
            per_domain[r["domain"]] += 1
            if len(cited) == k:
                break
        sentences = self.model.synthesize(prompt, cited)
        citations = [Citation(p.url, p.domain, p.id, p.heading) for p in cited]
        trace = {"queries": queries, "candidates": rows[:12], "all": rows, "cited": [p.id for p in cited]}
        return Answer(prompt, sentences, citations, trace)

    def run(self, prompts, samples=1, temperature=0.0, seed=0, run_id="run"):
        """prompts: list of dicts with 'id' and 'prompt'. One row per prompt per sample."""
        rows = []
        for pr in prompts:
            for s in range(samples):
                a = self.ask(pr["prompt"], temperature=temperature, seed=seed, sample=s)
                rows.append({"run_id": run_id, "prompt_id": pr["id"], "sample": s,
                             "cited_urls": [c.url for c in a.citations],
                             "cited_domains": [c.domain for c in a.citations],
                             "answer": " ".join(a.sentences)})
        return rows
