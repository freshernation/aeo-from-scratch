# Week 5 milestone - the audit tool, version 2: access, structured data, entity.
#
# Start from your week 3 aeo_audit.py. Copy into this folder: robots.py, fetchcheck.py,
# sitemap.py, access.py (week 3) and jsonld.py, entities.py, schema.py (this week).
# You may import load_pages from aeolab and FakeWeb from aeolab.fakeweb.
#
# Changes from week 3:
#   audit(web, domain, brand=None) -> dict
#       as before, plus
#         "schema": schema_summary(schema_audit(web, domain))
#         "entity": entity_report(load_pages(web), brand)
#       brand defaults to the domain's first label, capitalised ("tidewell.example" -> "Tidewell").
#   render(result) -> str
#       "# Audit: {domain}" (was "Access audit"), then the week 3 sections, then before
#       "## Fix first":
#         "## Structured data"
#             "- {with_markup} of {pages} readable pages have markup: {types, comma-separated}"
#             then "- {path}: {problem}" per problem and "- {path}: {mismatch}" per mismatch
#         "## Entity"
#             "- names: Form (n), Form (n)" sorted by form
#             one line per conflict: "- {attribute}: {value} ({domains}); {value} ({domains})"
#             domains: the host of each url, comma-separated, in the conflict's order
#   main(argv=None)
#       --web may now be given more than once (argparse action="append"); the folders are
#       laid over the seeded web in that order. --brand overrides the brand.
#
# Run it on the web weeks 4 to 6 use:
#   python3 week-05/milestone/build/aeo_audit.py tidewell.example --web aeolab/web2
