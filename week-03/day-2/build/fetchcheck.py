# Day 2 - fetch a page the way a crawler does, and say why it is unreadable.
#
# Copy robots.py from day-1/build; import allowed from it.
# web is an aeolab.fakeweb.FakeWeb. web.fetch(url, user_agent=...) returns a Response
# with .status, .headers (lowercase keys) and .text. It never follows redirects and
# never runs JavaScript, like most AI crawlers.
#
#   check(web, url, user_agent, max_hops=5) -> dict with exactly these keys:
#       "url"         the url asked for
#       "status"      the status of the last fetch (None if robots stopped you first)
#       "final_url"   the url that answered last
#       "hops"        the urls that redirected, in order
#       "noindex"     "header" (X-Robots-Tag contains noindex), "meta" (a
#                     <meta name="robots"> containing noindex), or None. Header first.
#       "js_shell"    True if the page's <main> has no text once <script>s are removed
#                     and it contains an element with id="app"
#       "canonical"   the href of <link rel="canonical">, or None
#       "readable"    True only if nothing below stopped it
#       "reason"      "" when readable, else the FIRST of, in this order:
#           "robots"               robots.txt (fetched from the url's host) disallows
#                                  this path for user_agent - check BEFORE every fetch,
#                                  including each redirect target
#           "redirect-loop"        a redirect goes to a url already in hops, or there
#                                  are more than max_hops redirects
#           "status-NNN"           the final status is not 200, e.g. "status-403"
#           "noindex-header" / "noindex-meta"
#           "js-only"              js_shell is True
#           "canonical-elsewhere"  canonical is set and is not this url (ignore a
#                                  trailing "/")
#   Redirects are 301, 302, 307, 308; follow "location", resolved against the url.
#
# Why this order: it is the order a crawler meets them. A page blocked by robots.txt
# is never fetched, so the crawler never sees its noindex.
