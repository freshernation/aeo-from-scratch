from aeolab import HERE

LOG = HERE / "data" / "logs" / "tidewell-2026-09.log"
RANGES = HERE / "data" / "ip_ranges"
L1 = ('192.0.2.5 - - [03/Sep/2026:10:00:00 +0000] "GET /faq HTTP/1.1" 200 512 "-" '
      '"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.3; +https://openai.com/gptbot"')
L2 = '10.0.0.1 - - [04/Sep/2026:11:00:00 +0000] "GET /faq?utm_source=chatgpt.com HTTP/1.1" 200 900 "-" "Mozilla/5.0 Safari"'


def test_parse(load):
    h = load("logs.py").parse_line(L1)
    assert (h["ip"], h["day"], h["path"], h["status"]) == ("192.0.2.5", "03/Sep/2026", "/faq", 200)
    assert load("logs.py").parse_line("garbage") is None


def test_bots_and_verification(load):
    lg = load("logs.py")
    ranges = lg.load_ranges(RANGES)
    assert lg.bot_of(lg.parse_line(L1)["ua"]) == "GPTBot"
    assert lg.verified("192.0.2.5", "GPTBot", ranges) and not lg.verified("45.33.1.1", "GPTBot", ranges)
    assert not lg.verified("192.0.2.20", "GPTBot", ranges), "inside OpenAI's search bot range, not GPTBot's"


def test_referral(load):
    lg = load("logs.py")
    assert lg.referral(lg.parse_line(L2)) == "ChatGPT"
    assert lg.referral({"referer": "https://www.perplexity.ai/", "path": "/"}) == "Perplexity"
    assert lg.referral({"referer": "https://www.google.com/", "path": "/"}) is None


def test_finding_who_really_came(load):
    lg = load("logs.py")
    lines = LOG.read_text().splitlines()
    ranges = lg.load_ranges(RANGES)
    s = lg.summarize(lines, ranges)
    assert s["bots"]["GPTBot"] == {"verified": 180, "spoofed": 400, "status-200": 180}, \
        "400 of 580 hits claiming to be GPTBot came from outside OpenAI's ranges"
    assert s["bots"]["Claude-SearchBot"] == {"verified": 210, "status-403": 98, "status-200": 112}
    assert lg.first_success(lines, ranges, "Claude-SearchBot") == "15/Sep/2026", "the day the CDN rule was fixed"
    assert s["referrals"] == {"ChatGPT": 73, "Gemini": 39, "Claude": 21, "Perplexity": 15}
