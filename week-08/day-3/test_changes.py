from site_checks import SITE, check_sections, info, own_pages, part, visible_numbers


def test_three_pages_changed_and_nothing_invented():
    domain = info()["domain"]
    before = own_pages(SITE / "snapshot", domain)
    after = own_pages(SITE / "after", domain)
    assert len(after) >= 3, f"{len(after)} changed pages; change at least three"
    known = set().union(*(visible_numbers(p.read_text()) for p in before.values()))
    for rel, path in after.items():
        assert rel in before, f"{rel} is not a page in your snapshot"
        assert path.read_text() != before[rel].read_text(), f"{rel} is unchanged"
        invented = visible_numbers(path.read_text()) - known
        assert not invented, f"{rel}: numbers that are nowhere on your site: {sorted(invented)}"


def test_written(source):
    text = source("CHANGES.md")
    check_sections(text, (("Live on the real site", 20),))
    rows = [l for l in part(text, "The changes").splitlines() if l.startswith("|") and not l.startswith(("| File", "|---"))]
    assert len(rows) >= 3
