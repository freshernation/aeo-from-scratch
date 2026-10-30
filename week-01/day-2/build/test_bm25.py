import math

import pytest

DOCS = [
    {"heading": "Lead", "text": "Filters remove lead."},
    {"heading": "Chlorine", "text": "Carbon removes chlorine taste and chlorine smell."},
    {"heading": "Fluoride", "text": "Reverse osmosis removes fluoride and lead."},
]


def idf(n, df):
    return math.log((n - df + 0.5) / (df + 0.5) + 1)


class TestBM25:
    def test_score_by_hand(self, load):
        b = load("bm25.py").BM25(DOCS)
        # passage 0 tokens: lead filter remove lead -> 4 tokens; avgdl = (4 + 7 + 6) / 3
        avgdl = 17 / 3
        tf = 2
        expected = idf(3, 2) * tf * 2.2 / (tf + 1.2 * (1 - 0.75 + 0.75 * 4 / avgdl))
        assert b.score("lead", 0) == pytest.approx(expected, rel=1e-6), \
            "check idf, the term count (lead appears twice in heading+text) and the length part"

    def test_missing_term_adds_nothing(self, load):
        assert load("bm25.py").BM25(DOCS).score("arsenic", 0) == 0.0

    def test_repeated_query_term_counts_twice(self, load):
        b = load("bm25.py").BM25(DOCS)
        assert b.score("lead lead", 2) == pytest.approx(2 * b.score("lead", 2))

    def test_search_order(self, load):
        hits = load("bm25.py").BM25(DOCS).search("chlorine")
        assert len(hits) == 1 and hits[0][1]["heading"] == "Chlorine", "zero-score passages are left out"

    def test_shorter_passage_wins_a_tie_on_frequency(self, load):
        hits = load("bm25.py").BM25(DOCS).search("lead fluoride")
        assert [h[1]["heading"] for h in hits] == ["Fluoride", "Lead"]

    def test_k(self, load):
        assert len(load("bm25.py").BM25(DOCS).search("removes", k=2)) == 2

    def test_ties_keep_list_order(self, load):
        docs = [{"heading": "a", "text": "same words"}, {"heading": "a", "text": "same words"}]
        hits = load("bm25.py").BM25(docs).search("words")
        assert hits[0][1] is docs[0]


def test_finding_bm25_and_the_panel_disagree(load, pages, prompts, panel):
    """The day's finding: same web, same prompts - how often does plain BM25's top
    passage come from the page the panel cites first?"""
    load("passages.py")
    split = load("passages.py").split_passages
    b = load("bm25.py").BM25([p for url, html in pages.items() for p in split(url, html)])
    agree = sum(b.search(x["prompt"], 1)[0][1]["url"] == panel.ask(x["prompt"]).citations[0].url
                for x in prompts)
    assert agree == 9, f"expected 9 of 30, got {agree}: the panel is not BM25 - fan-out, boosts and its crawl all change the winner"
