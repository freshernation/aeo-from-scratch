from aeolab import load_runs


def vis(load):
    for f in ("metrics.py", "sampling.py", "stats.py", "stability_check.py", "report.py"):
        load(f)
    return load("visibility.py")


def test_title_from_file_name(load):
    assert vis(load).build("baseline.jsonl").startswith("# Visibility report: baseline\n")


def test_no_change_section_without_against(load):
    assert "## Change" not in vis(load).build("baseline.jsonl")


def test_rerun_is_noise(load):
    text = vis(load).build("rerun.jsonl", against="baseline.jsonl")
    assert ("## Change against baseline\n\nPaired by prompt: 9 better, 8 worse, 13 the same. "
            "Sign test p = 1.000: not distinguishable from noise.") in text


def test_fix_is_real(load):
    text = vis(load).build("fixed.jsonl", against="baseline.jsonl")
    assert "15 better, 4 worse, 11 the same. Sign test p = 0.019: a real change." in text
    assert "Tidewell is cited in 83.5% of 600 answers (72.7% to 93.2%" in text, \
        "note the intervals of baseline (61-84) and fixed (73-93) overlap - and the paired test still says real"


def test_cli_writes_file(load, tmp_path):
    out = tmp_path / "R.md"
    assert vis(load).main(["fixed.jsonl", "--against", "baseline.jsonl", "--out", str(out)]) == 0
    assert out.read_text().startswith("# Visibility report: fixed")


def test_works_on_any_domain(load):
    text = vis(load).build("baseline.jsonl", domain="clearflow.example", brand="ClearFlow")
    assert "ClearFlow is cited in 76.7% of 600 answers" in text
