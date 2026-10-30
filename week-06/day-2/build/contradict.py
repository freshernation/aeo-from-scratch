# Day 2 - the same fact, stated differently on different sites.
#
# Copy corroborate.py (day 1) and facts.py (week 4 day 2). Import paragraphs and
# extract_facts from them.
#
#   h1(html) -> str              the <h1>'s text, or ""
#
#   normalise(value) -> str
#       lowercase; "-" becomes a space; liter/liters/litres all become "litre";
#       whitespace collapsed. normalise("150 Litres") == "150 litre",
#       normalise("2.4-litre") == "2.4 litre".
#
#   fact_claims(pages, subject, kind, near=None) -> list[tuple[str, str]]
#       (url, normalised value) for every fact of `kind` in every paragraph that is
#       about the subject: the subject appears (ignore case) in the paragraph OR in the
#       page's h1 - and, if `near` is given, `near` appears in the paragraph too.
#
#   contradictions(claims) -> dict
#       {value: sorted urls} sorted by value, if there is more than one distinct value;
#       {} if every claim agrees.
#
# Why: a finder that lists candidates is useful; one that claims to know which are real
# is lying. Today's finding is how many candidates are real.
