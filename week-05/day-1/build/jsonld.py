# Day 1 - JSON-LD, read and checked by hand.
#
# Use json, re and BeautifulSoup. No schema library.
#
#   REQUIRED   the course's minimum properties per type (a subset of what Google asks
#              for rich results - not the whole rule book):
#       Product: name, offers         Offer: price, priceCurrency
#       Organization: name, url       FAQPage: mainEntity
#       Question: name, acceptedAnswer    Answer: text
#       Article: headline, datePublished
#
#   extract(html) -> tuple[list[dict], list[str]]
#       Every <script type="application/ld+json"> block, parsed. A block that is a list
#       gives each dict in it; a dict with "@graph" gives each dict in the graph; any
#       other dict is one node. A block that is not valid JSON adds "invalid JSON" to
#       the errors list and nothing to the nodes.
#
#   types(node) -> list[str]           "@type" as a list (a string becomes a list of one)
#
#   validate(node, as_type=None) -> list[str]
#       "Type: missing prop" for each REQUIRED property that is absent, None, "" or []
#       - checked against as_type if given, else against each of the node's types.
#       Then recurse: "offers" items are checked as Offer, "mainEntity" items as
#       Question, "acceptedAnswer" as Answer (each may be a dict or a list of dicts).
#
#   visible_text(html) -> str          the page's text without <script>, <style>, <head>
#
#   prices(node) -> list[str]          str(price) of each of the node's offers that has one
#
#   mismatches(html, nodes) -> list[str]
#       "price {p} in markup is not on the page" for every markup price that does not
#       appear on the page as a $ amount. Compare with commas removed and a trailing
#       ".00" dropped, so "34.00" matches "$34" and "1299.00" matches "$1,299".
#
#   audit_page(url, html) -> dict
#       {"types": every node's types, flattened, "problems": errors then every node's
#        validate(), "mismatches": mismatches(html, nodes)}
#
# Why: valid markup and true markup are different checks. Today you write both.
