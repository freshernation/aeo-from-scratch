# Day 4 - what the server log says about AI crawlers and AI referrals.
#
# aeolab/data/logs/tidewell-2026-09.log is Tidewell's access log for September 2026,
# combined log format. aeolab/data/ip_ranges/*.json are bot IP ranges in the vendors'
# published format (invented addresses - read the README there).
#
#   BOTS = {"GPTBot": "gptbot", "OAI-SearchBot": "searchbot", "ChatGPT-User": "chatgpt-user",
#           "PerplexityBot": "perplexitybot", "Perplexity-User": "perplexity-user",
#           "ClaudeBot": "claudebot", "Claude-SearchBot": "claude-searchbot", "Claude-User": "claude-user"}
#       user-agent token -> the stem of its ranges file
#   REFERRERS   referer host -> engine: chatgpt.com and chat.openai.com -> "ChatGPT",
#               perplexity.ai and www.perplexity.ai -> "Perplexity", claude.ai -> "Claude",
#               gemini.google.com -> "Gemini", copilot.microsoft.com -> "Copilot"
#
#   parse_line(line) -> dict | None
#       {"ip", "day" (the first 11 characters of the timestamp, e.g. "15/Sep/2026"),
#        "method", "path", "status" (int), "referer", "ua"}; None for a line that does not parse.
#   bot_of(ua) -> str | None       the first BOTS token found in the user agent, any case
#   load_ranges(folder) -> dict    {file stem: [ipaddress networks]} from every *.json
#   verified(ip, bot, ranges) -> bool      the ip is inside one of the bot's networks
#   referral(hit) -> str | None
#       the engine for the referer's host, else "ChatGPT" if the path's query has
#       utm_source=chatgpt.com or utm_source=openai, else None.
#
#   summarize(lines, ranges) -> dict
#       {"bots": {token: {"verified": n, "spoofed": n, "status-200": n, ...}} sorted by token
#                 (status counts for verified hits only; leave out zero counts),
#        "referrals": {engine: n} most first, "landing": {path without query: n} most first}
#       A hit from a bot is never a referral.
#   first_success(lines, ranges, bot) -> str | None
#       the day of the bot's first verified hit with status 200.
#
# Why: a user agent is a claim anyone can make. A log tells you who really came, and,
# through referrals, whether an answer engine sent a person.
