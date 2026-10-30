from aeolab import load_pages, web2

PAGE = """<html><head><title>x</title>
<script type="application/ld+json">{"@context": "https://schema.org", "@graph": [
 {"@type": "Product", "name": "P", "offers": {"@type": "Offer", "price": "29.00", "priceCurrency": "USD"}},
 {"@type": ["Organization", "Brand"], "name": "T"}]}</script>
<script type="application/ld+json">{"@type": "Product", "name": "Q",}</script>
<script type="application/ld+json">[{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Why?", "acceptedAnswer": {"text": ""}}]}]</script>
</head><body><p>The pitcher costs $34. Big one: $1,299.</p></body></html>"""


def mod(load):
    return load("jsonld.py")


def test_extract(load):
    nodes, errors = mod(load).extract(PAGE)
    assert [n.get("name") for n in nodes] == ["P", "T", None] and errors == ["invalid JSON"]


def test_types(load):
    assert mod(load).types({"@type": "Product"}) == ["Product"] and mod(load).types({}) == []


def test_validate(load):
    j = mod(load)
    nodes, _ = j.extract(PAGE)
    assert j.validate(nodes[0]) == []
    assert j.validate(nodes[1]) == ["Organization: missing url"]
    assert j.validate(nodes[2]) == ["Answer: missing text"], "recurse: FAQPage -> Question -> Answer"
    assert j.validate({"@type": "Product", "name": "x", "offers": [{"price": "1"}]}) == ["Offer: missing priceCurrency"]


def test_mismatch(load):
    j = mod(load)
    nodes, _ = j.extract(PAGE)
    assert j.mismatches(PAGE, nodes) == ["price 29.00 in markup is not on the page"]
    assert j.mismatches(PAGE, [{"offers": {"price": "1299.00"}}]) == []


def test_audit_page(load):
    a = mod(load).audit_page("u", PAGE)
    assert a["types"] == ["Product", "Organization", "Brand", "FAQPage"]
    assert a["problems"][0] == "invalid JSON" and len(a["problems"]) == 3


def test_finding_valid_is_not_true(load):
    j = mod(load)
    results = {u: j.audit_page(u, h) for u, h in load_pages(web2()).items()}
    assert sum(bool(r["types"] or r["problems"]) for r in results.values()) == 9
    assert {u: r["problems"] for u, r in results.items() if r["problems"]} == {
        "https://aquaminder.example/shower-filter": ["Product: missing offers"],
        "https://purepath.example/reverse-osmosis": ["invalid JSON"]}
    pitcher = results["https://tidewell.example/filters/pitcher"]
    assert pitcher["problems"] == [] and pitcher["mismatches"] == ["price 29.00 in markup is not on the page"], \
        "Tidewell's pitcher markup is valid - and says $29 on a $34 page"
