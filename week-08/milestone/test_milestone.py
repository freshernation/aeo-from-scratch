from site_checks import check_sections, part


def test_two_rehearsals(source):
    text = source("INTERVIEW.md")
    check_sections(text, (("Rehearsal 1", 60), ("Rehearsal 2", 60), ("What I will say differently on Friday", 40)))
    for n in (1, 2):
        block = part(text, f"Rehearsal {n}")
        assert "SIGNAL" in block and "role: interviewer" in block, f"paste rehearsal {n}'s SIGNAL block"
