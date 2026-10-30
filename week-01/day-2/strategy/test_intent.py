from aeolab import load_prompts

HELD_OUT = [
    ("Is the ClearFlow Under-Sink better than the UX3?", "comparison"),
    ("Does Tidewell ship to Canada?", "brand"),
    ("How to replace a shower filter cartridge", "howto"),
    ("Best filter for a rental flat", "commercial"),
    ("What is reverse osmosis?", "informational"),
    ("Tidewell RO-5 vs PurePath RO Max", "comparison"),
]


class TestClassify:
    def test_intents(self, load):
        assert set(load("intent.py").INTENTS) == {"brand", "howto", "comparison", "commercial", "informational"}

    def test_examples(self, load):
        c = load("intent.py").classify
        assert c("Is a shower filter worth it?") == "commercial"
        assert c("Tidewell Pitcher vs ClearFlow Pitcher") == "comparison", "a comparison that names Tidewell is still a comparison"

    def test_course_prompts(self, load):
        acc = load("intent.py").accuracy(load_prompts())
        assert acc >= 0.9, f"{acc:.2f} of the course prompts classified right; aim for 0.9"

    def test_held_out(self, load):
        c = load("intent.py").classify
        right = sum(c(p) == want for p, want in HELD_OUT)
        assert right >= 5, f"{right}/6 prompts you have never seen were right - rules that only fit the 30 are memorised, not rules"


class TestNewPrompts:
    def rows(self, source):
        text = source("NEW_PROMPTS.md")
        rows = [r for r in text.splitlines() if r.startswith("|") and not r.startswith(("| Prompt", "|---"))]
        return [[c.strip() for c in r.strip("|").split("|")] for r in rows]

    def test_instructions_removed(self, source):
        assert "<!--" not in source("NEW_PROMPTS.md"), "Delete the instructions comment."

    def test_ten_new_prompts(self, source):
        rows = self.rows(source)
        assert len(rows) == 10, f"{len(rows)} rows; write ten"
        existing = {p["prompt"].lower() for p in load_prompts()}
        assert not {r[0].lower() for r in rows} & existing, "these must be new, not from prompts.csv"
        intents = {r[1] for r in rows}
        assert intents <= {"brand", "howto", "comparison", "commercial", "informational"}, intents
        assert len(intents) >= 3, "use at least three intents"

    def test_your_classifier_agrees_with_you(self, source, load):
        c = load("intent.py").classify
        rows = self.rows(source)
        agree = sum(c(r[0]) == r[1] for r in rows)
        assert agree >= 8, f"your classifier agrees with your own labels on {agree}/10 - fix one of them"

    def test_where_they_came_from(self, source):
        part = source("NEW_PROMPTS.md").split("## Where they came from", 1)[1]
        assert len(part.split()) >= 60
