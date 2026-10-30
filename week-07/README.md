# Week 7 — Live engines and monitoring

> **Destination**
> You can turn three vendors' answers into one shape, price a measurement before you run
> it, keep every run and alert only on changes beyond noise, and read a server log for
> which AI crawlers really came and which answer engines sent people. Builders ship a
> monitor; Strategists ship the monitoring plan Tidewell will run.

Six weeks of measurement happened on engines we built. This week points the same method
at engines nobody outside their companies can read: Claude, ChatGPT and Perplexity with
search on. The tests stay offline, on answers shaped like theirs; with a key you can run
every lab live.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Parse three vendors' answers into one shape (B) · compare live-shaped answers with the panel (S) |
| Tue | `day-2/` | Price a run before running it (B) · a sampling plan with a cost (S) |
| Wed | `day-3/` | Store every run and detect drift (B) · read nine weeks of runs (S) |
| Thu | `day-4/` | Read a server log: verified bots, spoofed bots, AI referrals (B) · the log report (S) |
| Fri | `milestone/` | **B:** `monitor.py` · **S:** Tidewell's monitoring plan |

---

## The rule from this week on

**Price it before you run it, and say which numbers are verified.** A run on a live
engine costs money and cannot be taken back. Every price in this course says where it
came from and when, or says that it is missing.

---

## Before Monday

Optional: add a key to `.env` for one or more engines (see `SETUP.md`) and read the
docstring of `aeolab/live.py`. Without a key, every lab works on the fixtures.

---

## Outside-view question

> *A weather network has a thousand stations. How does it tell a broken station from a
> storm, and how long does it wait before it decides?*
