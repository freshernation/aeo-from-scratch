# Day 3 - does structured data change what an engine cites?
#
# Copy jsonld.py from day 1.
#
#   strip_jsonld(html) -> str
#       The html with every <script type="application/ld+json">...</script> removed,
#       together with the whitespace before it. Nothing else changes.
#
#   without_jsonld(web, folder) -> list[str]
#       For every page of every domain in web that answers 200 and contains
#       "application/ld+json", write strip_jsonld(page) into folder at the page's file
#       path (folder/domain/index.html for "/", folder/domain/a/b.html for "/a/b").
#       Return the urls written. Lay folder over the web to run the experiment.
#
#   changed(rows_a, rows_b) -> int
#       Rows (matched by prompt_id and sample) whose cited_urls differ.
#
#   faq_passages(url, html) -> list[dict]
#       For a FAQPage node: one passage per question, {"id": f"{url}#faq{n}", "url",
#       "heading": the question's name, "text": its acceptedAnswer's text}.
#       An engine that indexed these would read markup as content.
#
# Why: Google says AI features have no additional requirements. Today you test that
# claim on two engines you can read - and say what the test cannot tell you.
