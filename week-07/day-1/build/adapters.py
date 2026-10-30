# Day 1 - three engines' answers in one shape.
#
# aeolab/live.py asks live engines and returns each vendor's raw JSON as a dict.
# aeolab/data/live/{claude,openai,perplexity}.json hold 30 answers per vendor in those
# shapes (invented content - read the README there). Today you parse all three.
#
#   normalise_url(url) -> str
#       lowercase scheme and host; drop the #fragment (including #:~:text=...); drop
#       query parameters whose name starts with utm_ (keep any others, in order); drop a
#       trailing "/" from the path, except a path of just "/". An empty path becomes "/".
#       normalise_url("https://T.example/faq/?utm_source=chatgpt.com#x") == "https://t.example/faq"
#
#   parse_claude(resp) -> dict
#       {"text": the text blocks' texts, stripped, joined by single spaces,
#        "citations": normalised urls of every citation of type
#                     "web_search_result_location" on those text blocks,
#                     in order, each once}
#   parse_openai(resp) -> dict
#       the same, from output items of type "message": their content parts of type
#       "output_text" give the text, and their annotations of type "url_citation" the urls.
#       Texts joined by single spaces.
#   parse_perplexity(resp) -> dict
#       text: choices[0].message.content ("" if no choices); citations: the "citations"
#       list, or if it is missing or empty, the urls of "search_results". Normalised, each once.
#
#   PARSERS = {"claude": parse_claude, "openai": parse_openai, "perplexity": parse_perplexity}
#
#   to_row(parsed, prompt_id, sample=0, run_id="live") -> dict
#       week 2's row: run_id, prompt_id, sample, cited_urls, cited_domains (each url's
#       host), answer (the text).
#
# Why: a citation from ChatGPT and one from Perplexity to the same page arrive as
# different strings. Counting them as different pages inflates every number after this.
