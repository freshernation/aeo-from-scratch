# Day 4 - every page against every AI crawler.
#
# Copy robots.py and fetchcheck.py in.
#
#   BOTS   a dict of the nine user agents to check, name -> kind, kind being
#          "training", "search" or "user":
#            training  GPTBot, ClaudeBot, Google-Extended
#            search    OAI-SearchBot, Claude-SearchBot, PerplexityBot
#            user      ChatGPT-User, Claude-User, Perplexity-User
#          (The vendors' own pages, linked from the day README, say which is which.)
#
#   matrix(web, domain, bots=BOTS) -> dict
#       {url: {bot: check(web, url, bot)["reason"]}} for every url in
#       web.page_urls(domain). "" means readable.
#
#   summary(m, bots=BOTS) -> dict with exactly:
#       "pages"                    how many urls
#       "invisible_to_all_search"  sorted urls no search bot can read
#       "unreadable_by_bot"        {bot: how many urls it cannot read}
#       "reasons"                  {reason: how many (url, bot) cells have it}
#
# Why the three kinds: blocking a training crawler and blocking a search crawler are
# different decisions with different costs. Most sites make the second by accident.
