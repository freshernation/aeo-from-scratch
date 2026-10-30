"""Given. Copy real websites into the folder layout FakeWeb serves. Week 8.

    from aeolab.snapshot import take_snapshot
    take_snapshot(["https://www.your-site.com/", "https://a-competitor.com/"],
                  "week-08/site/snapshot", max_pages=40)
    # then:  FakeWeb(root="week-08/site/snapshot")  - your site, offline, for every week's tools

What it does, politely: identifies itself (USER_AGENT), reads each site's robots.txt and
obeys it, waits `delay` seconds between requests, follows links and the sitemap within the
start URL's host, skips URLs with a query string, and stops at max_pages per site.
It saves what the server sends: HTML pages, robots.txt, sitemap.xml, and in _server.json
the redirects and any X-Robots-Tag headers - so week 3's access checks work on the copy.

What it cannot see: JavaScript is not run (like most AI crawlers - that is the point), and
a CDN rule that blocks AI crawlers by user agent or address will not show, because this
tool is not an AI crawler. Check that in your server log or your CDN's bot settings.

Only snapshot sites you may read this way, keep it small, and keep other sites' pages on
your machine: week-08/site/snapshot/ is in .gitignore.
"""

import json
import time
from collections import deque
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit

from bs4 import BeautifulSoup

from aeolab.fakeweb import path_to_file
from aeolab.panel import robots_allows

USER_AGENT = "aeo-from-scratch-snapshot/1.0 (course exercise; respects robots.txt)"


def take_snapshot(start_urls, out_dir, max_pages=40, user_agent=USER_AGENT, delay=1.0, client=None):
    import httpx

    own = client is None
    client = client or httpx.Client(timeout=20, headers={"User-Agent": user_agent})
    out_dir = Path(out_dir)
    counts = {}
    try:
        for start in start_urls:
            host = urlsplit(start).netloc.lower()
            base = f"{urlsplit(start).scheme}://{host}"
            folder = out_dir / host
            folder.mkdir(parents=True, exist_ok=True)
            server = {"redirects": {}, "headers": {}}

            def get(url):
                time.sleep(delay)
                return client.get(url, headers={"User-Agent": user_agent}, follow_redirects=False)

            robots = get(base + "/robots.txt")
            robots_text = robots.text if robots.status_code == 200 else ""
            if robots_text:
                (folder / "robots.txt").write_text(robots_text)
            queue, seen = deque([start]), {start}
            sm = get(base + "/sitemap.xml")
            if sm.status_code == 200 and "<urlset" in sm.text:
                (folder / "sitemap.xml").write_text(sm.text)
                for loc in BeautifulSoup(sm.text, "html.parser").find_all("loc"):
                    u = loc.get_text(strip=True)
                    if urlsplit(u).netloc.lower() == host and u not in seen:
                        seen.add(u)
                        queue.append(u)
            pages = 0
            while queue and pages < max_pages:
                url = queue.popleft()
                path = urlsplit(url).path or "/"
                if urlsplit(url).query or not robots_allows(robots_text, user_agent, path):
                    continue
                r = get(url)
                if r.status_code in (301, 302, 307, 308):
                    target = urljoin(url, r.headers.get("location", ""))
                    if urlsplit(target).netloc.lower() == host:
                        server["redirects"][path] = urlsplit(target).path or "/"
                        if target not in seen:
                            seen.add(target)
                            queue.append(target)
                    continue
                if r.status_code != 200 or "html" not in r.headers.get("content-type", ""):
                    continue
                if "x-robots-tag" in r.headers:
                    server["headers"][path] = {"X-Robots-Tag": r.headers["x-robots-tag"]}
                f = folder / path_to_file(path)
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(r.text)
                pages += 1
                for a in BeautifulSoup(r.text, "html.parser").find_all("a", href=True):
                    link = urldefrag(urljoin(url, a["href"]))[0]
                    if urlsplit(link).netloc.lower() == host and link not in seen:
                        seen.add(link)
                        queue.append(link)
            (folder / "_server.json").write_text(json.dumps(server, indent=2) + "\n")
            counts[host] = pages
    finally:
        if own:
            client.close()
    return counts


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("usage: python3 -m aeolab.snapshot OUT_DIR URL [URL ...]")
        raise SystemExit(2)
    print(take_snapshot(sys.argv[2:], sys.argv[1]))
