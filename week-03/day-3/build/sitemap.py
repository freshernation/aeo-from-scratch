# Day 3 - the sitemap, audited; and an llms.txt, generated.
#
# Copy robots.py and fetchcheck.py in. Use xml.etree.ElementTree for the XML.
#
#   sitemap_urls(xml_text) -> list[str]
#       Every <loc> in a sitemaps.org sitemap, in order, stripped. The elements are in
#       the namespace http://www.sitemaps.org/schemas/sitemap/0.9.
#
#   audit_sitemap(web, domain, user_agent="PanelBot") -> dict with exactly:
#       "listed"             how many urls the sitemap lists
#       "listed_broken"      listed urls whose own fetch is not 200 (a 404, or a
#                            redirect: a sitemap should list the final url)
#       "listed_unreadable"  listed urls that return 200 but that check() says the bot
#                            cannot index
#       "unlisted_readable"  pages in web.page_urls(domain) that check() says are
#                            readable but that the sitemap does not list
#       Lists keep sitemap order (the first three) or page_urls order (the last).
#
#   llms_txt(name, summary, sections) -> str
#       The llms.txt format from llmstxt.org:
#           "# {name}", blank line, "> {summary}", blank line, then for each section
#           (sections is a dict, heading -> list of (title, url, note)):
#           "## {heading}", blank line, one "- [{title}]({url}): {note}" per link
#           (no ": " part when note is empty), then a blank line.
#
# Why: a sitemap is a promise of what to crawl. Tidewell's promises pages that do not
# exist and hides one that does.
