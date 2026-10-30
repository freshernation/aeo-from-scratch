# Day 1 - a passage linter: what stops a passage being quoted alone.
#
# Copy passages.py from week-01/milestone/build into this folder.
#
#   PRONOUNS = ("it", "this", "they", "these", "those", "that")
#
#   first_sentence(text) -> str
#       Up to and including the first . ! or ? followed by whitespace; the whole text
#       if there is none.
#
#   lint_passage(heading, text) -> list[str]
#       Codes, in this order, for each problem the passage has:
#         "pronoun-opener"       first word, lowercased, stripped of , . : ; is in PRONOUNS
#         "long-first-sentence"  first sentence over 35 words
#         "thin"                 under 12 words in all
#         "buried-answer"        the heading's tokens (your tokenize) appear in the text
#                                but none of them in the first sentence
#       [] for a clean passage.
#
#   lint_site(web, domain) -> dict
#       {url: [(heading, codes), ...]} for every url in web.page_urls(domain) that
#       answers 200 when fetched with render_js=True (lint the content as a reader
#       sees it), one entry per passage from your split_passages.
#
#   flag_rate(web, domain) -> float
#       Share of the site's passages with at least one code. 0.0 for none.
#
# Why: four problems that a writer can fix in an afternoon and an engine punishes
# every time it quotes.
