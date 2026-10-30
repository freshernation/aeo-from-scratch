"""Day-zero environment check.

Run this with:  python3 check_setup.py

Every line should say OK. If one says FAIL, it tells you what to do about it.
Add one check per package or account the course needs, in the order SETUP.md
introduces them. The last check is always the baseline.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
GREEN, RED, DIM, OFF = "\033[32m", "\033[31m", "\033[2m", "\033[0m"
results = []


def check(name, ok, fix=""):
    results.append((name, ok))
    print(f"  {GREEN + 'OK  ' if ok else RED + 'FAIL'}{OFF}  {name}")
    if not ok and fix:
        print(f"        {DIM}-> {fix}{OFF}")


def can_import(module):
    try:
        __import__(module)
        return True
    except ImportError:
        return False


def main():
    print("\nChecking your setup\n" + "-" * 46)
    v = sys.version_info
    check(f"Python {v.major}.{v.minor}.{v.micro}", (v.major, v.minor) >= (3, 12),
          "Install Python 3.12 or newer - see SETUP.md step 1.")
    in_venv = sys.prefix != sys.base_prefix
    check("Virtual environment is active", in_venv, "Run:  source .venv/bin/activate")
    check("pytest is installed", can_import("pytest"), "Run:  pip install -r requirements.txt")
    for module in ["bs4", "aeolab"]:
        check(f"{module} is installed", can_import(module), "Run:  pip install -r requirements.txt  and  pip install -e .")
    check("git is installed", shutil.which("git") is not None, "Install git - see SETUP.md.")
    if shutil.which("git"):
        tracked = subprocess.run(["git", "ls-files", ".env"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        check(".env is not tracked by git", not tracked,
              "Your key file is in git. Run:  git rm --cached .env   then rotate the key.")
    baseline = ROOT / "logs" / "baseline.md"
    check("Your baseline is written (logs/baseline.md)", baseline.exists() and "_(" not in baseline.read_text(),
          "Run the advisor (ai/advisor.md) and paste its summary into logs/baseline.md.")
    print("-" * 46)
    failed = [name for name, ok in results if not ok]
    if failed:
        print(f"\n{RED}{len(failed)} check(s) failed.{OFF} Fix them, then run this again.\n")
        return 1
    print(f"\n{GREEN}All checks passed.{OFF} Next: open week-01/README.md\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
