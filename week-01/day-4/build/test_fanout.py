import pytest
from aeolab.llm import FakeModel


class TestRRF:
    def test_example(self, load):
        out = load("fanout.py").rrf([["a", "b"], ["b"]])
        assert [i for i, _ in out] == ["b", "a"]
        assert out[0][1] == pytest.approx(1 / 62 + 1 / 61)

    def test_ties_keep_first_seen(self, load):
        assert [i for i, _ in load("fanout.py").rrf([["x"], ["y"]])] == ["x", "y"]

    def test_k(self, load):
        assert load("fanout.py").rrf([["a"]], k=0) == [("a", 1.0)]


class TestFanout:
    DOCS = [{"id": "1", "url": "u1", "heading": "Lead", "text": "Filters remove lead."},
            {"id": "2", "url": "u2", "heading": "Boiling", "text": "Boiling concentrates lead."},
            {"id": "3", "url": "u3", "heading": "Fluoride", "text": "Reverse osmosis removes fluoride."}]

    def test_uses_every_search(self, load):
        load("passages.py")
        b = load("bm25.py").BM25(self.DOCS)
        model = FakeModel(fanout={"lead": ["boiling"]}, extras={})
        ids = [p["id"] for p in load("fanout.py").search_fanout(b, model, "lead")]
        assert ids[0] == "2", "passage 2 is found by both searches, so fusion puts it first"
        assert model.calls == [("fan_out", "lead")]

    def test_top_k(self, load):
        load("passages.py")
        b = load("bm25.py").BM25(self.DOCS)
        assert len(load("fanout.py").search_fanout(b, FakeModel(fanout={}, extras={}), "removes lead", k=1)) == 1


def test_finding_fanout_moves_the_winner(load, pages, prompts):
    split = load("passages.py").split_passages
    b = load("bm25.py").BM25([p for url, html in pages.items() for p in split(url, html)])
    fo, m = load("fanout.py"), FakeModel()
    changed = found_without = found_with = 0
    for x in prompts:
        plain = [p["url"] for _, p in b.search(x["prompt"], 10)]
        fused = [p["url"] for p in fo.search_fanout(b, m, x["prompt"], 10)]
        changed += plain[0] != fused[0]
        if x["best_url"]:
            found_without += x["best_url"] in plain[:4]
            found_with += x["best_url"] in fused[:4]
    assert changed == 12, f"fan-out changed the top passage on {changed}/30 prompts, expected 12"
    assert (found_without, found_with) == (19, 20), \
        "Tidewell's best page reaches the top 4 on 19 of 28 prompts alone, 20 with fan-out: it moves winners more than it finds pages"
