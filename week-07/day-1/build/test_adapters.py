import json
from pathlib import Path

LIVE = Path(__file__).parents[3] / "aeolab" / "data" / "live"

CLAUDE = {"content": [
    {"type": "server_tool_use", "id": "s", "name": "web_search", "input": {"query": "q"}},
    {"type": "web_search_tool_result", "tool_use_id": "s", "content": [{"type": "web_search_result", "url": "https://x.example/"}]},
    {"type": "text", "text": " Lead is removed. ", "citations": [
        {"type": "web_search_result_location", "url": "https://A.example/p/?utm_source=x&id=2#top", "title": "t", "cited_text": "c"}]},
    {"type": "text", "text": "Also this.", "citations": None},
    {"type": "text", "text": "Again.", "citations": [{"type": "web_search_result_location", "url": "https://a.example/p?id=2"}]}]}
OPENAI = {"output": [
    {"type": "web_search_call", "id": "ws", "status": "completed"},
    {"type": "message", "content": [{"type": "output_text", "text": "One.", "annotations": [
        {"type": "url_citation", "url": "https://b.example/?utm_medium=y", "start_index": 0, "end_index": 4}]}]}]}
PPLX = {"citations": [], "search_results": [{"url": "https://c.example/a/", "title": "t"}],
        "choices": [{"message": {"content": "Answer."}}]}


def test_normalise(load):
    n = load("adapters.py").normalise_url
    assert n("https://T.example/faq/?utm_source=chatgpt.com#x") == "https://t.example/faq"
    assert n("https://t.example/?a=1&utm_campaign=z&b=2") == "https://t.example/?a=1&b=2"
    assert n("https://t.example") == "https://t.example/"
    assert n("https://t.example/learn#:~:text=certified") == "https://t.example/learn"


def test_claude(load):
    assert load("adapters.py").parse_claude(CLAUDE) == {
        "text": "Lead is removed. Also this. Again.", "citations": ["https://a.example/p?id=2"]}, \
        "two citation strings, one page; search results that were not cited do not count"


def test_openai(load):
    assert load("adapters.py").parse_openai(OPENAI) == {"text": "One.", "citations": ["https://b.example/"]}


def test_perplexity_falls_back_to_search_results(load):
    assert load("adapters.py").parse_perplexity(PPLX) == {"text": "Answer.", "citations": ["https://c.example/a"]}


def test_row(load):
    a = load("adapters.py")
    assert a.to_row({"text": "x", "citations": ["https://a.example/p"]}, "P01", 2, "r") == {
        "run_id": "r", "prompt_id": "P01", "sample": 2, "cited_urls": ["https://a.example/p"],
        "cited_domains": ["a.example"], "answer": "x"}


def test_finding_half_the_strings_are_duplicates(load):
    a = load("adapters.py")
    counts = {}
    for vendor in ("claude", "openai", "perplexity"):
        data = json.loads((LIVE / f"{vendor}.json").read_text())
        counts[vendor] = len({u for resp in data.values() for u in a.PARSERS[vendor](resp)["citations"]})
    assert counts == {"claude": 45, "openai": 44, "perplexity": 46}, \
        f"{counts}: about 85 distinct citation strings per vendor are about 45 pages"
