# Day 1 - split a page into the passages an answer engine retrieves and quotes.
#
# You may use BeautifulSoup (from bs4 import BeautifulSoup) and the re module.
# Do not import anything from aeolab.panel: the panel has its own splitter, and the
# point of today is writing yours.
#
#   STOPWORDS    a frozenset of common English words to drop. Copy the list from
#                aeolab/panel.py, or write your own of at least 100 words.
#
#   tokenize(text) -> list[str]
#       Lowercase, then every run of letters and digits is a word.
#       Drop stopwords. If a word is longer than 3 letters and ends in "s" but not
#       "ss", drop the final "s" (filters -> filter, PFAS -> pfa, glass stays glass).
#       tokenize("Which filters remove PFAS?") == ["filter", "remove", "pfa"]
#       tokenize("") == []
#
#   split_passages(url, html) -> list[dict]
#       One dict per passage, in page order, each with exactly these keys:
#           "id"       f"{url}#{n}", n counting from 0
#           "url"      the url given
#           "heading"  the heading the passage sits under
#           "text"     the passage's text, blocks joined by single spaces
#           "words"    len(text.split())
#       A new passage starts at every <h2> and every <h3>. Text before the first one
#       belongs to a passage whose heading is the <h1>'s text.
#       Ignore <header>, <nav>, <footer>, <script> and <style> entirely.
#       Read <p>, <ul>, <ol> and <table> elements:
#           a list item becomes a sentence: add a "." if it does not end in . ! or ?
#           a table row becomes "Head: cell; Head: cell." using the <th> texts
#       Skip a passage with no text. A page with no headings at all is one passage.
#       Why: engines quote passages, not pages. A heading is the cheapest signal of
#       where one answer stops and the next starts.
