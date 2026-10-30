# Day 4 - the structured data module for the audit tool.
#
# Copy jsonld.py and entities.py from day 2, robots.py and fetchcheck.py from week 3.
#
#   schema_audit(web, domain, bot="OAI-SearchBot") -> dict
#       {url: jsonld.audit_page(url, html)} for every url in
#       web.page_urls(domain) that check() says bot can read; html is the fetch of
#       check()'s final_url as bot. Markup on a page no crawler reads helps nobody.
#
#   schema_summary(results) -> dict with exactly:
#       "pages"        how many results
#       "with_markup"  how many have at least one type
#       "types"        every type seen, sorted, once each
#       "problems"     {url: problems} for urls with problems
#       "mismatches"   {url: mismatches} for urls with mismatches
#
#   entity_report(pages, brand) -> dict
#       {"names": dict(name_forms(...)), "conflicts": conflicts(claims(...))}
#
# Why: next to the access matrix, these two sections finish the audit of Tidewell's
# own site. Week 6 adds everyone else's.
