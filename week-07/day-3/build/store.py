# Day 3 - every run kept, and a check that says when something moved.
#
# Copy metrics.py, sampling.py and stats.py from week-02/milestone/build; import
# paired from stats. Use sqlite3 from the standard library.
#
#   class RunStore(path)
#       Opens (or creates) an SQLite file with one table, rows:
#         run_id, engine, run_date, prompt_id, sample, cited_urls, cited_domains, answer
#       (lists stored as JSON text). Open it with isolation_level=None and wrap each
#       save in BEGIN ... COMMIT.
#       .save(rows, engine, run_date)     append week 2's rows
#       .runs(engine=None) -> list[dict]  {"run_id", "engine", "run_date"} once per run,
#                                         sorted by run_date then run_id; only that
#                                         engine's runs when given
#       .rows(run_id) -> list[dict]       week 2's rows for that run, in saved order
#
#   rate(rows, domain) -> float           share of rows citing domain; 0.0 for none
#
#   drift(store, domain, engine, alpha=0.05) -> list[dict]
#       For each pair of consecutive runs of the engine (by date):
#         {"from": date, "to": date, "before": rate rounded to 3, "after": rate rounded
#          to 3, "wins", "losses", "p" (stats.paired, before -> after), "alert"}
#       alert is "drop" when p < alpha and losses > wins, "rise" when p < alpha and
#       wins > losses, else "".
#
# Why: a monitor that alerts on every wobble is switched off in a month. Week 2's paired
# test is the line between a wobble and a change.
