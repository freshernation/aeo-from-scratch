"""An offline web. Every lab and every test fetches through this, never the network.

    from aeolab.fakeweb import FakeWeb
    web = FakeWeb()                                   # the seeded sites in aeolab/web/
    r = web.fetch("https://tidewell.example/faq", user_agent="OAI-SearchBot")
    r.status, r.headers, r.text

What a site does lives in two places in its folder under aeolab/web/<domain>/:

    <path>.html, robots.txt, sitemap.xml, llms.txt   the files it serves
    _server.json                                     how its server behaves:

        "redirects":  {"/old": "/new"}           301 with a Location header
        "headers":    {"/path": {"x-robots-tag": "noindex"}}
        "ua_block":   ["ClaudeBot", ...]         403 for any user agent containing one
        "js_only":    ["/compare"]               the page's content arrives only by JavaScript
        "cloak":      {"/path": {"match": ["bot"], "file": "_cloak/path.html"}}
                                                 a different file for any user agent
                                                 containing one of the match tokens

fetch() never follows redirects and never runs JavaScript unless render_js=True, which
is what a browser does and most AI crawlers do not.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

WEB_ROOT = Path(__file__).parent / "web"
_RENDER = re.compile(r'<script type="text/x-render">(.*?)</script>', re.S)


@dataclass
class Response:
    url: str
    status: int
    headers: dict = field(default_factory=dict)
    text: str = ""


def split_url(url):
    """'https://a.example/x/y' -> ('a.example', '/x/y'). A missing path is '/'."""
    parts = urlsplit(url)
    return parts.netloc.lower(), parts.path or "/"


def path_to_file(path):
    """'/' -> 'index.html', '/faq' -> 'faq.html', '/robots.txt' -> 'robots.txt'."""
    path = path.strip("/")
    if not path:
        return "index.html"
    if "." in path.rsplit("/", 1)[-1]:
        return path
    return path + ".html"


class FakeWeb:
    def __init__(self, root=WEB_ROOT, overlay=None):
        """root: a folder of sites. overlay: a folder (or a list of folders, first wins)
        whose files win over root, file by file - a snapshot a student has edited."""
        if overlay is None:
            overlays = []
        elif isinstance(overlay, (list, tuple)):
            overlays = list(overlay)
        else:
            overlays = [overlay]
        self.roots = [Path(o) for o in overlays] + [Path(root)]

    def domains(self):
        found = set()
        for root in self.roots:
            if root.is_dir():
                found |= {p.name for p in root.iterdir() if p.is_dir() and "." in p.name}
        return sorted(found)

    def _file(self, domain, rel):
        for root in self.roots:
            p = root / domain / rel
            if p.is_file():
                return p
        return None

    def server(self, domain):
        p = self._file(domain, "_server.json")
        return json.loads(p.read_text()) if p else {}

    def page_urls(self, domain):
        """Every HTML page a domain has on disk - including ones nothing links to.
        Ground truth for audits; a crawler cannot see this list."""
        rels = set()
        for root in self.roots:
            base = root / domain
            if base.is_dir():
                rels |= {p.relative_to(base).as_posix() for p in base.rglob("*.html")
                         if not p.relative_to(base).as_posix().startswith("_")}
        urls = []
        for rel in sorted(rels):
            path = "/" if rel == "index.html" else "/" + rel[: -len(".html")]
            urls.append(f"https://{domain}{path}")
        return urls

    def fetch(self, url, user_agent="Mozilla/5.0", render_js=False):
        domain, path = split_url(url)
        if domain not in self.domains():
            return Response(url, 0, {}, "")
        conf = self.server(domain)
        ua = user_agent.lower()
        if any(token.lower() in ua for token in conf.get("ua_block", [])):
            return Response(url, 403, {"content-type": "text/html"}, "<h1>Access denied</h1>")
        if path in conf.get("redirects", {}):
            target = conf["redirects"][path]
            if target.startswith("/"):
                target = f"https://{domain}{target}"
            return Response(url, 301, {"location": target}, "")
        cloak = conf.get("cloak", {}).get(path)
        if cloak and any(t.lower() in ua for t in cloak["match"]):
            f = self._file(domain, cloak["file"])
        else:
            f = self._file(domain, path_to_file(path))
        if f is None:
            return Response(url, 404, {"content-type": "text/html"}, "<h1>Not found</h1>")
        text = f.read_text()
        kind = "text/plain" if f.suffix == ".txt" else "application/xml" if f.suffix == ".xml" else "text/html"
        headers = {"content-type": kind}
        headers.update({k.lower(): v for k, v in conf.get("headers", {}).get(path, {}).items()})
        if render_js:
            m = _RENDER.search(text)
            if m:
                text = text.replace('<div id="app"></div>', f'<div id="app">{m.group(1)}</div>')
        return Response(url, 200, headers, text)
