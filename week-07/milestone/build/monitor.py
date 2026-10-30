# Week 7 milestone - a monitor: run on a schedule, store every run, alert on drift.
#
# Copy adapters.py, budget.py, store.py (this week) and metrics.py, sampling.py,
# stats.py (week 2) into this folder. You may import load_prompts and web2 from aeolab,
# Panel and EngineB.
#
#   OFFLINE = {"panel": Panel, "engine_b": EngineB}
#
#   load_config(path) -> dict
#       A JSON file with domain, prompts (a list of csv paths), engines (names: "panel",
#       "engine_b", "claude", "openai", "perplexity"), samples, temperature, budget_usd,
#       store (an SQLite path) and prices (prices.json). ValueError naming the first
#       missing key.
#
#   live_rows(engine, prompts, samples, run_id, ask) -> list[dict]
#       For every prompt and sample: ask(engine, prompt text) -> raw JSON ->
#       PARSERS[engine] -> to_row. `ask` is aeolab.live.ask in real use; tests pass a fake.
#
#   run_once(config, run_date, web=None, ask=None) -> dict
#       1 prompts from every csv; cost = budget.run_cost(...). ValueError if cost is None
#         ("...no price...") or above budget_usd ("...over the ... budget").
#       2 for each engine: run_id f"{engine}-{run_date}"; offline engines run on `web`
#         (web2() if None) with seed int(run_date without "-") % 10000; live ones via live_rows;
#         save to the store; drift() for that engine.
#       3 return {"date", "cost", "engines": {engine: {"rate": rounded to 3,
#                 "last": the last drift entry or None}}}
#
#   report(result, domain) -> str
#       "# Monitor: {domain}, {date}", "Cost of this run: $x.xx", then a table
#       | Engine | Cited | Change | Alert | with Cited as "83.3%", Change as
#       "86.3% -> 56.3% (4 up, 18 down, p = 0.004)" or "first run", Alert the alert or "-";
#       then "## Alerts" with "- {engine}: citation rate dropped beyond noise. Check access
#       first." per drop, or "- none".
#
#   main(argv=None): python monitor.py CONFIG --date YYYY-MM-DD [--web DIR ...] [--out FILE]
