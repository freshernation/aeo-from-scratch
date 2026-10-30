"""Given. What a crawler receives for a URL, against what a browser shows.

    python3 week-03/day-2/strategy/view_as_bot.py /filters/under-sink
    python3 week-03/day-2/strategy/view_as_bot.py /faq Claude-SearchBot
"""
import sys

from bs4 import BeautifulSoup

from aeolab.fakeweb import FakeWeb
from aeolab.panel import Panel


def text_of(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "header", "footer"]):
        t.decompose()
    main = soup.find("main") or soup.body or soup
    return " ".join(main.get_text(" ", strip=True).split())


def main(path, bot="PanelBot"):
    url = "https://tidewell.example" + path
    web = FakeWeb()
    r = web.fetch(url, user_agent=bot)
    print(f"{url}  as {bot}\n")
    print(f"status   {r.status}")
    for k, v in r.headers.items():
        print(f"header   {k}: {v}")
    soup = BeautifulSoup(r.text, "html.parser")
    for m in soup.find_all("meta", attrs={"name": "robots"}):
        print(f"meta     robots: {m.get('content')}")
    for l in soup.find_all("link", rel="canonical"):
        print(f"link     canonical: {l.get('href')}")
    print(f"\nwhat the bot reads ({len(text_of(r.text).split())} words):\n  {text_of(r.text)[:300]}")
    browser = web.fetch(url, render_js=True)
    print(f"\nwhat a browser shows ({len(text_of(browser.text).split())} words):\n  {text_of(browser.text)[:300]}")
    ok, why = Panel(bot=bot).readable(url)
    print(f"\npanel can index it: {ok}  {why}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/", sys.argv[2] if len(sys.argv) > 2 else "PanelBot")
