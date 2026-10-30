from aeolab import load_pages, web2


def mod(load):
    for f in ("robots.py", "fetchcheck.py", "jsonld.py", "entities.py"):
        load(f)
    return load("schema.py")


def test_only_readable_pages(load):
    r = mod(load).schema_audit(web2(), "tidewell.example")
    assert len(r) == 18 and "https://tidewell.example/filters/pitcher-blue" not in r


def test_summary(load):
    s = mod(load)
    out = s.schema_summary({"a": {"types": ["Product"], "problems": [], "mismatches": ["m"]},
                            "b": {"types": [], "problems": ["p"], "mismatches": []}})
    assert out == {"pages": 2, "with_markup": 1, "types": ["Product"], "problems": {"b": ["p"]}, "mismatches": {"a": ["m"]}}


def test_finding_tidewell(load):
    s = mod(load)
    out = s.schema_summary(s.schema_audit(web2(), "tidewell.example"))
    assert (out["with_markup"], out["types"]) == (3, ["FAQPage", "Organization", "Product"])
    assert out["mismatches"] == {"https://tidewell.example/filters/pitcher": ["price 29.00 in markup is not on the page"]}
    e = s.entity_report(load_pages(web2()), "Tidewell")
    assert set(e["conflicts"]) == {"founded", "city"}
