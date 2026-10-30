# Week 2 milestone - the visibility report, from the command line.
#
# Copy metrics.py, sampling.py, stats.py and report.py into this folder.
#
#   build(run, against=None, domain="tidewell.example", brand="Tidewell") -> str
#       run: a run file name or path, for aeolab.load_runs.
#       The text of report.report(rows, load_prompts(), domain, brand,
#                                 title=f"Visibility report: {stem of run}").
#       When `against` is given, append:
#           "\n## Change against {stem of against}\n\n"
#           "Paired by prompt: {wins} better, {losses} worse, {ties} the same. "
#           "Sign test p = {p:.3f}: {verdict}.\n"
#       where the pairing is stats.paired(against_rows, run_rows, domain) and verdict is
#       "a real change" when p < 0.05, else "not distinguishable from noise".
#
#   main(argv=None) -> int
#       python visibility.py RUN [--against RUN] [--domain D] [--brand B] [--out FILE]
#       Writes the report to --out, or prints it. Returns 0. Use argparse.
#
# Why a command: on Friday you run it on a run file you have not seen.
