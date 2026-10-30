"""Given. Checks shared by week 8's tests."""
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

from strategy_checks import check_sections, part  # noqa: F401

SITE = Path(__file__).parent / "site"
NUMBER = re.compile(r"\d[\d,.]*\d|\d")


def info():
    data = json.loads((SITE / "site.json").read_text())
    assert data.get("domain"), "write your site's domain in week-08/site/site.json"
    return data


def visible_numbers(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "header", "footer", "head", "time"]):
        t.decompose()  # an "Updated" date is not a fact about the product
    return {n.rstrip(".,") for n in NUMBER.findall(soup.get_text(" "))}


def own_pages(folder, domain):
    base = Path(folder) / domain
    return {p.relative_to(base).as_posix(): p for p in base.rglob("*.html")} if base.is_dir() else {}
