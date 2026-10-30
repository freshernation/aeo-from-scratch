# Week 3 milestone - the audit tool, version 1: access.
#
# Copy robots.py, fetchcheck.py, sitemap.py and access.py into this folder.
#
#   audit(web, domain) -> dict
#       {"domain": domain,
#        "matrix": access.matrix(web, domain),
#        "summary": access.summary(that matrix),
#        "sitemap": sitemap.audit_sitemap(web, domain)}
#
#   render(result) -> str
#       Markdown, these sections in order:
#         "# Access audit: {domain}"
#         "## Search crawlers"  a table: | Page | OAI-SearchBot | Claude-SearchBot | PerplexityBot |
#                               one row per page (path only, e.g. /faq), "ok" or the reason
#         "## Every crawler"    one line per bot: "- {bot} ({kind}): {n} of {pages} pages unreadable"
#         "## Sitemap"          one line each:
#                               "- {n} listed, {b} broken, {u} listed but unreadable, {r} readable but unlisted"
#                               then "- broken: {url}" for each broken url
#         "## Fix first"        the pages invisible to every search crawler, one "- {path}: {reason}"
#                               each, using OAI-SearchBot's reason
#
#   main(argv=None) -> int
#       python aeo_audit.py DOMAIN [--json FILE] [--web DIR]
#       Prints render(audit(...)). --json also writes the audit dict as JSON.
#       --web is a folder of sites to lay over the seeded web (FakeWeb(overlay=DIR)),
#       so you can audit a fixed copy. Returns 0.
#
# Why a tool: weeks 5 and 6 add modules to it. In week 8 you point it at your own site.
