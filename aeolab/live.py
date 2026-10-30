"""Given. Ask live answer engines a question, with their web search on. Week 7 onward.

NOTHING IN THE TESTS CALLS THIS FILE. It needs API keys and costs money. The course
author has not run it (no keys); every request shape below follows the vendors' own
documentation, read on 2026-10-30. Run it yourself, once, before trusting it.

    from aeolab import live
    raw = live.ask("claude", "Do water filters remove lead?")   # the vendor's raw JSON, as a dict

Keys come from the environment (put them in .env, never in git):
    ANTHROPIC_API_KEY   claude      (or an `ant auth login` profile)
    OPENAI_API_KEY      openai      also set OPENAI_MODEL to a current model with web search
    PERPLEXITY_API_KEY  perplexity  model "sonar" unless PERPLEXITY_MODEL says otherwise

What each returns, and where its citations are:
    claude      a Messages response. Text blocks carry "citations" of type
                "web_search_result_location" (url, title, cited_text).
    openai      a Responses response. "output" holds a "web_search_call" item and a
                "message" item whose output_text has "annotations" of type "url_citation".
    perplexity  a chat completion with "citations" (a list of URLs) and "search_results"
                (title, url, date, snippet).
Week 7 day 1 writes the parsers that turn all three into one shape.
"""

import os

CLAUDE_MODEL = "claude-opus-5-5"
CLAUDE_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": 5}


def ask_claude(prompt, max_continuations=3):
    import anthropic

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": prompt}]
    for _ in range(max_continuations + 1):
        # fallbacks="default": if the model declines on safety grounds, the API reruns the
        # request on a fallback model inside the same call (beta, Claude API only).
        response = client.beta.messages.create(
            model=CLAUDE_MODEL, max_tokens=16000, tools=[CLAUDE_TOOL], messages=messages,
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
        )
        if response.stop_reason != "pause_turn":
            return response.to_dict()
        # The server's search loop paused: send the turn back and it resumes on its own.
        messages = [{"role": "user", "content": prompt}, {"role": "assistant", "content": response.content}]
    return response.to_dict()


def ask_openai(prompt):
    import openai

    model = os.environ.get("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Set OPENAI_MODEL to a current model that supports the web_search tool.")
    client = openai.OpenAI()
    return client.responses.create(model=model, tools=[{"type": "web_search"}], input=prompt).to_dict()


def ask_perplexity(prompt):
    import httpx

    key = os.environ["PERPLEXITY_API_KEY"]
    r = httpx.post("https://api.perplexity.ai/chat/completions", timeout=120,
                   headers={"Authorization": f"Bearer {key}"},
                   json={"model": os.environ.get("PERPLEXITY_MODEL", "sonar"),
                         "messages": [{"role": "user", "content": prompt}]})
    r.raise_for_status()
    return r.json()


ENGINES = {"claude": ask_claude, "openai": ask_openai, "perplexity": ask_perplexity}


def ask(engine, prompt):
    return ENGINES[engine](prompt)
