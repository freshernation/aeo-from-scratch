# Day 4 - which searches does Tidewell have no answer for?
#
#   gaps(panel, model, prompts, domain="tidewell.example", k=5) -> list[dict]
#       For every prompt, ask model.fan_out(prompt["prompt"]) for its searches and
#       skip the first one (it is the prompt itself). For each remaining search q,
#       look at panel.search(q, k): if no passage there has .domain == domain, that
#       search is a gap. Return one dict per gap, in prompt order:
#           {"prompt_id": "P03", "subquery": "..."}
#
# Why: an engine fills its answer from all the searches it fans out to. A search you
# have no passage for is a place a competitor's sentence goes in your answer.
