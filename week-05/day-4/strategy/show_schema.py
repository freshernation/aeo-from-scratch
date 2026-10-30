"""Given. The structured data on every page of web2, as a crawler receives it.

    python3 week-05/day-4/strategy/show_schema.py
"""
import json

from bs4 import BeautifulSoup

from aeolab import web2


def main():
    web = web2()
    for d in web.domains():
        for url in web.page_urls(d):
            html = web.fetch(url, user_agent="OAI-SearchBot").text
            for tag in BeautifulSoup(html, "html.parser").find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(tag.string)
                    print(f"{url}\n    {json.dumps(data)[:400]}\n")
                except json.JSONDecodeError as e:
                    print(f"{url}\n    NOT VALID JSON: {e}\n")


if __name__ == "__main__":
    main()
