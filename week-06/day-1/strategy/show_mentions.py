"""Given. Every paragraph on another site that names Tidewell, and who links to it.

    python3 week-06/day-1/strategy/show_mentions.py
"""
import re
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

from aeolab import load_pages, web2


def main():
    pages = load_pages(web2())
    links = set()
    for url, html in sorted(pages.items()):
        host = urlsplit(url).netloc
        if host == "tidewell.example":
            continue
        soup = BeautifulSoup(html, "html.parser")
        if any(urlsplit(urljoin(url, a["href"])).netloc == "tidewell.example" for a in soup.find_all("a", href=True)):
            links.add(host)
        for t in soup(["script", "style", "nav", "header", "footer", "head"]):
            t.decompose()
        for p in soup.find_all(["p", "li", "td"]):
            text = " ".join(p.get_text(" ").split())
            if re.search(r"\btidewell\b(?!\.\w)", text, re.I):
                print(f"{url}\n    {text}\n")
    print("Sites linking to tidewell.example:", ", ".join(sorted(links)))


if __name__ == "__main__":
    main()
