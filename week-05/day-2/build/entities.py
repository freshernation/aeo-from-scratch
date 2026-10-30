# Day 2 - one company, many descriptions.
#
# Copy jsonld.py from day 1; import extract and types from it.
#
#   paragraphs(html) -> list[str]
#       The text of every <p>, <li> and <td>, whitespace collapsed, ignoring <script>,
#       <style>, <nav>, <header>, <footer> and <head>. (Paragraphs, not sentences:
#       "Tidewell Water Co. was founded..." would split after "Co.".)
#
#   name_forms(pages, brand) -> Counter
#       pages: {url: html}. How often each written form of the brand appears in the
#       paragraphs: the brand with an optional space after its fourth letter, any case
#       ("TideWell", "Tide well"), followed optionally by " Water Co." or " Inc.".
#       Not when followed by "." and a letter: "tidewell.example" is an address, not a name.
#
#   claims(pages, brand) -> list[tuple[str, str, str]]
#       (url, attribute, value) for each claim about the brand:
#         in a paragraph that contains the brand (ignore case and spaces):
#           "founded"  from "founded in NNNN"
#           "city"     the first word of "based in City, Region" or "in City, Region"
#         in an Organization node whose name contains the brand:
#           "founded"  the first four characters of foundingDate
#           "city"     address.addressLocality
#
#   conflicts(claims) -> dict
#       {attribute: {value: sorted urls}} for attributes with more than one value.
#
# Why: an engine that reads two pages saying different things about you may quote
# either. You cannot fix what you have not found.
