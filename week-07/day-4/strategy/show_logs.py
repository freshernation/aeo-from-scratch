"""Given. Tidewell's September log: AI crawlers by name, whether their IP matches the
vendor's published range, what status they got, and people sent by answer engines.

    python3 week-07/day-4/strategy/show_logs.py
"""
import ipaddress
import json
import re
from collections import Counter, defaultdict

from aeolab import HERE

LINE = re.compile(r'(\S+) \S+ \S+ \[([^:]+)[^\]]*\] "\S+ (\S+) [^"]*" (\d{3}) \S+ "([^"]*)" "([^"]*)"')
TOKENS = {"GPTBot": "gptbot", "OAI-SearchBot": "searchbot", "ChatGPT-User": "chatgpt-user", "PerplexityBot": "perplexitybot",
          "Perplexity-User": "perplexity-user", "ClaudeBot": "claudebot", "Claude-SearchBot": "claude-searchbot",
          "Claude-User": "claude-user"}


def main():
    nets = {f.stem: [ipaddress.ip_network(p["ipv4Prefix"]) for p in json.loads(f.read_text())["prefixes"]]
            for f in (HERE / "data" / "ip_ranges").glob("*.json")}
    bots, refs, days = defaultdict(Counter), Counter(), defaultdict(set)
    for line in (HERE / "data" / "logs" / "tidewell-2026-09.log").read_text().splitlines():
        m = LINE.match(line)
        if not m:
            continue
        ip, day, path, status, ref, ua = m.groups()
        tok = next((t for t in TOKENS if t.lower() in ua.lower()), None)
        if tok:
            ok = any(ipaddress.ip_address(ip) in n for n in nets[TOKENS[tok]])
            bots[tok]["in range" if ok else "NOT in range"] += 1
            if ok:
                bots[tok][f"status {status}"] += 1
                days[(tok, status)].add(day)
        elif ref not in ("-", "") and any(h in ref for h in ("chatgpt", "perplexity", "claude.ai", "gemini")):
            refs[ref] += 1
    for tok, c in sorted(bots.items()):
        print(f"{tok:<18}", dict(c))
    for tok in ("Claude-SearchBot", "PerplexityBot"):
        print(f"{tok} 403 on {len(days[(tok, '403')])} days, 200 on {len(days[(tok, '200')])} days; "
              f"first 200: {min(days[(tok, '200')], key=lambda d: int(d.split('/')[0])) if days[(tok, '200')] else '-'}")
    print("\nReferrals:", dict(refs.most_common()))


if __name__ == "__main__":
    main()
