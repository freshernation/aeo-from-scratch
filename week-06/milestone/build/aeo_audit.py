# Week 6 milestone (Project 2) - the audit tool, version 3: one command, one report.
#
# Start from your week 5 aeo_audit.py. Copy into this folder: robots.py, fetchcheck.py,
# sitemap.py, access.py (week 3), jsonld.py, entities.py, schema.py (week 5), facts.py
# (week 4), and corroborate.py, contradict.py, offsite.py, attribution.py (this week).
# You may import load_pages and load_prompts from aeolab, FakeWeb, and Panel.
#
#   audit(web, domain, brand=None, facts=(), prompts=None) -> dict
#       week 5's dict, plus:
#         "offsite": {"mentions": mentions(pages, brand, domain),
#                     "inbound": inbound(pages, domain),
#                     "stale": stale(...) over the domain's own pages AND every page with
#                              a paragraph naming the brand,
#                     "contradictions": {spec: contradictions(fact_claims(pages, subject,
#                                        kind[, near]))} for each "SUBJECT:KIND[:NEAR]" in facts}
#         "manipulation": {"hidden": {url: injections(...)} for pages whose hidden text
#                                    holds an injection,
#                          "cloaked": every url on every domain that cloaked() flags}
#         "lost": attribute_all(Panel(web), prompts)    only when prompts is given
#
#   fix_first(result) -> list[str], in this order:
#       1 "{path}: {reason} (search crawlers cannot read it)" for each page invisible to
#         every search crawler, except canonical-elsewhere (a duplicate is fine)
#       2 "{path}: {mismatch}" for each markup mismatch
#       3 "{spec}: {n} different values across {m} pages" for each non-empty contradiction
#       4 "entity {attribute}: {value} / {value}" for each entity conflict
#       5 "stale: {url} ({date})" for each stale page
#
#   render(result) -> str
#       week 5's sections, then before "## Fix first":
#         "## Off-site"       "- mentioned on: d (n), ..."; "- linked from: d, ..."; one line
#                             per contradiction spec: "- {spec}: {value} ({urls}); ..." or
#                             "- {spec}: consistent"; "- stale: {url} ({date})" each
#         "## Manipulation"   "- hidden instruction: {url}: {phrases}"; "- cloaked: {url}"
#         "## Lost prompts"   (only with prompts) "- cited 17, no-page 3, ..." (sorted by
#                             kind), then "- {id}: {why}" for each not cited and not no-page
#       "## Fix first" is now a numbered list: "1. ...".
#
#   main(argv=None): week 5's options, plus --fact SPEC and --prompts FILE, both repeatable.
#
#   python3 week-06/milestone/build/aeo_audit.py tidewell.example --web aeolab/web2 \
#       --fact "UX3:price" --fact "Tidewell Pitcher:volume:cartridge" \
#       --prompts aeolab/prompts.csv --prompts aeolab/prompts_more.csv
