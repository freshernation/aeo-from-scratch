# Day 1 - who else talks about you, and who links to you.
#
# pages: {url: html}, as aeolab.load_pages(web2()) gives.
#
#   host(url) -> str                     the url's domain
#   paragraphs(html) -> list[str]        as week 5's entities.paragraphs: <p>, <li>, <td>,
#                                        without script, style, nav, header, footer, head
#
#   mentions(pages, brand, own) -> dict
#       {domain: paragraphs naming the brand} for every domain except `own` with at least
#       one, sorted by domain. "Naming" is the brand as a whole word, any case, not
#       followed by "." and a letter (not an address).
#
#   inbound(pages, domain) -> list[str]
#       Sorted domains, other than `domain`, with at least one <a href> pointing at it
#       (resolve relative links against the page's url).
#
#   corroborating(pages, terms, own=None) -> list[str]
#       Sorted domains, other than `own`, with at least one paragraph containing every
#       term (ignore case). corroborating(pages, ["UX3", "PFOA"], "tidewell.example").
#
# Why: the panel's R9 counts other domains linking to a site. Live engines are widely
# described as weighing what independent sources say; this is how you count it.
