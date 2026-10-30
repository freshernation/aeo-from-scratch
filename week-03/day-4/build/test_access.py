from aeolab.fakeweb import FakeWeb


def mod(load):
    load("robots.py")
    load("fetchcheck.py")
    return load("access.py")


def test_bots(load):
    b = mod(load).BOTS
    assert len(b) == 9 and set(b.values()) == {"training", "search", "user"}
    assert b["OAI-SearchBot"] == "search" and b["GPTBot"] == "training" and b["Claude-User"] == "user"


def test_matrix_shape(load):
    m = mod(load).matrix(FakeWeb(), "tidewell.example", bots={"PanelBot": "search"})
    assert len(m) == 19 and m["https://tidewell.example/faq"] == {"PanelBot": ""}


def test_summary_small(load):
    m = {"u1": {"A": "", "B": "robots"}, "u2": {"A": "status-403", "B": "robots"}}
    s = mod(load).summary(m, bots={"A": "search", "B": "search"})
    assert s == {"pages": 2, "invisible_to_all_search": ["u2"], "unreadable_by_bot": {"A": 1, "B": 2},
                 "reasons": {"robots": 2, "status-403": 1}}


def test_finding_two_engines_cannot_see_tidewell_at_all(load):
    a = mod(load)
    s = a.summary(a.matrix(FakeWeb(), "tidewell.example"))
    assert s["unreadable_by_bot"]["OAI-SearchBot"] == 7
    assert s["unreadable_by_bot"]["Claude-SearchBot"] == 19 and s["unreadable_by_bot"]["PerplexityBot"] == 19, \
        "robots.txt welcomes them; the server refuses every request with a 403"
    assert s["unreadable_by_bot"]["ClaudeBot"] == 19, "robots.txt allows ClaudeBot to train; the server blocks it anyway"
    assert len(s["invisible_to_all_search"]) == 7
