import re

from site_checks import SITE, info, own_pages, part


def test_snapshot():
    data = info()
    folders = [p for p in (SITE / "snapshot").iterdir() if p.is_dir()]
    assert len(folders) >= 3, "snapshot your site and at least two of the sites in site.json"
    assert len(own_pages(SITE / "snapshot", data["domain"])) >= 5, "at least five pages of your own site"


def test_audit(source):
    text = source("AUDIT.md")
    assert "<!--" not in text, "Delete the instructions comment."
    assert len(text.split()) >= 150
    assert len(re.findall(r"^\d+\.", part(text, "Fix first"), re.M)) >= 3
