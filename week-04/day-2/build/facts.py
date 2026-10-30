# Day 2 - the facts a passage carries.
#
#   PATTERNS   a list of (kind, regex) pairs, in this order:
#       "price"     $ then digits, with commas only BETWEEN digits, then optional
#                   decimals                                           $189  $1,299.00
#                   ("under $150," is "$150", not "$150,")
#       "percent"   digits, optional decimals, then %                    99%   2.5%
#       "volume"    digits (commas and dots allowed), an optional space or hyphen,
#                   then litre/litres/liter/liters                       3,000 litres  2.4-litre
#       "standard"  NSF/ANSI, optionally " Standard" or " Standards", a space, digits
#       "duration"  digits, optional space or hyphen, then month(s), year(s), week(s),
#                   day(s) or minute(s)                                  6 months  2-year
#       "year"      a whole four-digit number from 1900 to 2099          2016
#   Match case-insensitively. Only digits count: "six months" is not a fact here.
#
#   extract_facts(text) -> list[tuple[str, str]]
#       (kind, matched text) for every match, in the order they appear. Where two
#       matches overlap, keep the one that starts first (the longer one on a tie).
#       extract_facts("costs $189, lasts 3,000 litres") ==
#           [("price", "$189"), ("volume", "3,000 litres")]
#
#   fact_density(text) -> float        facts per 100 words; 0.0 for no words
#   first_sentence_has_fact(text) -> bool
#   site_facts(passages) -> tuple[float, float]
#       passages: dicts with "text". (mean fact_density, share of passages whose first
#       sentence has a fact). (0.0, 0.0) for none.
#
# Why: week 6 uses extract_facts to find the same fact stated two ways on two sites.
