# Day 1 - robots.txt, read the way RFC 9309 says.
#
# Do not use urllib.robotparser: the finding test compares your answers with it.
# Do not import from aeolab.panel.
#
#   parse(text) -> list[tuple[list[str], list[tuple[str, str]]]]
#       The groups in file order: (user agents lowercased, [(kind, path), ...]).
#       kind is "allow" or "disallow", lowercased. Comments (# to end of line) and
#       blank lines are ignored; field names are case-insensitive.
#       Consecutive User-agent lines share one group. A rule line before any
#       User-agent line is ignored. Other fields (Sitemap, Crawl-delay) are ignored
#       and do not end a group.
#
#   match(pattern, path) -> bool
#       Does the rule's pattern match the start of path? "*" matches any run of
#       characters; a "$" at the very end anchors the end of the path.
#       match("/learn/", "/learn/lead") is True; match("/*.pdf$", "/a.pdf?x") is False.
#
#   matched_rule(text, user_agent, path) -> tuple[str, str] | None
#       The rule that decides this path for this agent, or None if no rule matches.
#       The agent's token is the part before "/", lowercased ("GPTBot/1.1" -> "gptbot").
#       Use every group that names the token (merged); if none does, the "*" groups.
#       Of the rules that match, the one with the LONGEST pattern wins; on a tie in
#       length, allow wins. An empty "Disallow:" matches nothing.
#
#   allowed(text, user_agent, path) -> bool
#       True if no rule matches or the deciding rule is allow. "/robots.txt" itself
#       is always allowed.
#
# Why: RFC 9309 section 2.2.2 says the most specific match wins. Python's own parser
# takes the first match. On Tidewell's site, that difference is three pages.
