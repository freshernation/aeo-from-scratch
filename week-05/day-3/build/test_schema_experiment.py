import tempfile

from aeolab import load_prompts, web2
from aeolab.engine_b import EngineB
from aeolab.panel import Panel

HTML = '<html><head><title>t</title>\n<script type="application/ld+json">{"@type": "FAQPage", "mainEntity": [' \
       '{"@type": "Question", "name": "How often?", "acceptedAnswer": {"@type": "Answer", "text": "Every 150 litres."}}]}' \
       '</script>\n</head><body><p>x</p></body></html>'


def mod(load):
    load("jsonld.py")
    return load("schema_experiment.py")


def test_strip(load):
    assert mod(load).strip_jsonld(HTML) == "<html><head><title>t</title>\n</head><body><p>x</p></body></html>"


def test_changed(load):
    a = [{"prompt_id": "A", "sample": 0, "cited_urls": ["x"]}, {"prompt_id": "A", "sample": 1, "cited_urls": ["x"]}]
    b = [{"prompt_id": "A", "sample": 1, "cited_urls": ["y"]}, {"prompt_id": "A", "sample": 0, "cited_urls": ["x"]}]
    assert mod(load).changed(a, b) == 1


def test_faq_passages(load):
    assert mod(load).faq_passages("u", HTML) == [
        {"id": "u#faq0", "url": "u", "heading": "How often?", "text": "Every 150 litres."}]


def test_finding_no_engine_here_reads_it(load):
    s = mod(load)
    folder = tempfile.mkdtemp()
    written = s.without_jsonld(web2(), folder)
    assert len(written) == 9
    prompts = load_prompts()
    for engine in (Panel, EngineB):
        before = engine(web2()).run(prompts, 20, 0.3, seed=4)
        after = engine(web2(folder)).run(prompts, 20, 0.3, seed=4)
        assert s.changed(before, after) == 0, \
            f"{engine.__name__}: removing every piece of structured data on the web changes 0 of 600 answers"
