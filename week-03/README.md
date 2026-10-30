# Week 3 — Can it read you?

> **Destination**
> For any page and any of the nine AI crawlers, you can say whether that crawler can
> read it and exactly why not: robots.txt under RFC 9309, the server's answer, a
> noindex in the page or its headers, content that only JavaScript draws. Builders ship
> the first version of an audit tool; Strategists fix a copy of Tidewell's site and
> show the lift is real.

Access fails before content does, and silently. In week 1 half of Tidewell's losses
happened before scoring; last week one robots.txt line was worth eleven points. This
week you find all of it, and two of the faults are invisible to anyone who only reads
robots.txt.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Read robots.txt the way RFC 9309 says (B) · write Tidewell's crawler policy (S) |
| Tue | `day-2/` | Fetch like a bot: status, redirects, noindex, JavaScript (B) · find the invisible pages (S) |
| Wed | `day-3/` | Audit the sitemap and generate llms.txt (B) · write llms.txt and say what it is worth (S) |
| Thu | `day-4/` | Every page against every crawler (B) · the access audit, with a fix order (S) |
| Fri | `milestone/` | **B:** `aeo_audit.py`, version 1 · **S:** a fixed copy of Tidewell's site, and the measured lift |

---

## The rule from this week on

**Check access before content.** Before you rewrite a page, prove a crawler can read
it. A rewrite of a page nobody can fetch measures nothing.

---

## Before Monday

Read the four vendors' crawler pages listed in `SOURCES.md`. Note which bots train,
which build a search index and which fetch for a user.

---

## Outside-view question

> *A building has a doorman who checks one list and a fire marshal who locks some doors
> whatever the list says. A visitor is turned away. How do you find out which of them
> did it?*
