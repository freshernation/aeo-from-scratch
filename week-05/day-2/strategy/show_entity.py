"""Given. Every sentence on web2 that names Tidewell next to a year or a place.

    python3 week-05/day-2/strategy/show_entity.py
"""
import re

from bs4 import BeautifulSoup

from aeolab import load_pages, web2


def main():
    for url, html in sorted(load_pages(web2()).items()):
        soup = BeautifulSoup(html, "html.parser")
        for t in soup(["script", "style", "nav", "header", "footer", "head"]):
            t.decompose()
        for p in soup.find_all(["p", "li", "td"]):
            text = " ".join(p.get_text(" ").split())
            if re.search(r"tide ?well", text, re.I) and re.search(r"\b(19|20)\d\d\b|based in|, [A-Z][a-z]+", text):
                print(f"{url}\n    {text}\n")


if __name__ == "__main__":
    main()
