import pytest

PAGE = """<html><head><title>T</title><script>var x = 1;</script></head><body>
<header><nav><a href="/">Home</a> <a href="/faq">FAQ</a></nav></header>
<main><article><h1>The Pitcher</h1>
<p>It holds 2.4 litres.</p>
<h2>Cartridges</h2><p>Each lasts 150 litres.</p><p>They cost $12.</p>
<h3>Recycling</h3><ul><li>Send it back</li><li>We regenerate the carbon.</li></ul>
<h2>Compare</h2><table><thead><tr><th>Filter</th><th>Price</th></tr></thead>
<tbody><tr><td>Pitcher</td><td>$34</td></tr><tr><td>UX3</td><td>$189</td></tr></tbody></table>
<h2>Empty</h2>
</article></main><footer><p>(c) 2026 Tidewell</p></footer></body></html>"""


class TestTokenize:
    def test_example(self, load):
        assert load("passages.py").tokenize("Which filters remove PFAS?") == ["filter", "remove", "pfa"], \
            "lowercase, drop stopwords, strip a plural 's' from words longer than 3 letters"

    def test_keeps_double_s_and_short_words(self, load):
        assert load("passages.py").tokenize("glass gas bus") == ["glass", "gas", "bus"], \
            "'glass' ends in ss; 'gas' and 'bus' are 3 letters - all three stay"

    def test_numbers_are_words(self, load):
        assert load("passages.py").tokenize("NSF/ANSI 53, 2.4 litres") == ["nsf", "ansi", "53", "2", "4", "litre"]

    def test_empty(self, load):
        assert load("passages.py").tokenize("") == []


class TestSplit:
    def split(self, load):
        return load("passages.py").split_passages("https://t.example/p", PAGE)

    def test_one_passage_per_section(self, load):
        assert [p["heading"] for p in self.split(load)] == ["The Pitcher", "Cartridges", "Recycling", "Compare"], \
            "intro under the h1, then one per h2/h3; the empty section is skipped"

    def test_keys_and_ids(self, load):
        ps = self.split(load)
        assert set(ps[0]) == {"id", "url", "heading", "text", "words"}
        assert [p["id"] for p in ps] == [f"https://t.example/p#{n}" for n in range(4)]

    def test_paragraphs_joined(self, load):
        assert self.split(load)[1]["text"] == "Each lasts 150 litres. They cost $12."

    def test_list_items_become_sentences(self, load):
        assert self.split(load)[2]["text"] == "Send it back. We regenerate the carbon."

    def test_table_rows(self, load):
        assert self.split(load)[3]["text"] == "Filter: Pitcher; Price: $34. Filter: UX3; Price: $189."

    def test_nav_footer_script_ignored(self, load):
        text = " ".join(p["text"] for p in self.split(load))
        assert "Home" not in text and "2026" not in text and "var x" not in text

    def test_words(self, load):
        assert self.split(load)[1]["words"] == 7

    def test_no_headings_is_one_passage(self, load):
        ps = load("passages.py").split_passages("u", "<html><body><p>Just this.</p></body></html>")
        assert len(ps) == 1 and ps[0]["text"] == "Just this."

    def test_you_wrote_the_splitter(self, load, source):
        load("passages.py").split_passages  # write it first; this test checks how
        assert "aeolab.panel" not in source("passages.py", code_only=True), \
            "write your own splitter today - do not import the panel's"


def test_finding_tidewell_opens_with_it(load, pages):
    """The day's finding: count passages whose first word is a pronoun."""
    split = load("passages.py").split_passages
    ps = [p for url, html in pages.items() for p in split(url, html)]
    assert len(pages) == 50 and len(ps) == 104, f"50 pages should split into 104 passages, got {len(ps)}"
    pronouns = {"it", "this", "they", "these", "those", "that"}
    opens = lambda p: p["text"].split()[0].lower().strip(",.") in pronouns
    tidewell = [p for p in ps if "tidewell.example" in p["url"]]
    others = [p for p in ps if "tidewell.example" not in p["url"]]
    assert (sum(map(opens, tidewell)), len(tidewell)) == (9, 52)
    assert (sum(map(opens, others)), len(others)) == (0, 52), \
        "no other site opens a single passage with a pronoun - a passage lifted alone has to make sense alone"
