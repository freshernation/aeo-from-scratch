# Day 3 - stale pages, hidden text, instructions aimed at AI, and cloaking.
#
#   page_date(html) -> str
#       The datetime of the first <time> (first 10 characters), else the first
#       "dateModified" in the page's JSON-LD, else "".
#
#   stale(pages, today="2026-10-01", days=730) -> dict
#       {url: date} for pages dated more than `days` days before today, sorted by url.
#       (2026-10-01 is the panel's "today".)
#
#   hidden_text(html) -> list[str]
#       The text of every element hidden from readers: style containing display:none or
#       visibility:hidden (any spacing, any case), a `hidden` attribute, or
#       aria-hidden="true". Skip script, style, head and template. Skip empty text.
#
#   injections(text) -> list[str]
#       Every match, in order, of phrases aimed at an AI reader: "ignore" followed by
#       any of "all"/"any"/"other"/"previous" and then "instructions" or "sources";
#       "note to AI"; "AI assistant:" or "AI assistants:"; "you are an AI". Any case.
#
#   words(html) -> set[str]      lowercase words and numbers in the visible text
#
#   cloaked(web, url, bot="OAI-SearchBot", threshold=0.5) -> tuple[bool, float]
#       Fetch the url as bot and as "Mozilla/5.0". similarity = shared words / all words
#       (Jaccard), rounded to 2 places. (similarity < threshold, similarity).
#
# Why: you detect these on your own site so you never ship them, and on others' so you
# can show a client why a competitor's odd citation appeared - not so you can copy it.
