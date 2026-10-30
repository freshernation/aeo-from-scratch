"""Given. Old pages, hidden text, and pages that show crawlers something else.

    python3 week-06/day-3/strategy/show_offsite.py
"""
import re
from datetime import date

from bs4 import BeautifulSoup

from aeolab import load_pages, web2


def visible_words(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "header", "footer", "head"]):
        t.decompose()
    return set(re.findall(r"[a-z0-9]+", soup.get_text(" ").lower()))


def main():
    web = web2()
    pages = load_pages(web)
    print("Pages dated more than two years before 2026-10-01:")
    for url, html in sorted(pages.items()):
        t = BeautifulSoup(html, "html.parser").find("time")
        if t and (date(2026, 10, 1) - date.fromisoformat(t["datetime"][:10])).days > 730:
            print(f"  {t['datetime'][:10]}  {url}")
    print("\nHidden text (display:none, visibility:hidden, hidden, aria-hidden):")
    for url, html in sorted(pages.items()):
        for el in BeautifulSoup(html, "html.parser").find_all(style=re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden", re.I)):
            print(f"  {url}\n    {' '.join(el.get_text(' ').split())}")
    print("\nWords shared between what a crawler and a browser receive (1.00 = identical):")
    for d in web.domains():
        for url in web.page_urls(d):
            a = visible_words(web.fetch(url, user_agent="OAI-SearchBot").text)
            b = visible_words(web.fetch(url).text)
            sim = len(a & b) / len(a | b) if a | b else 1.0
            if sim < 0.9:
                print(f"  {sim:.2f}  {url}")


if __name__ == "__main__":
    main()
