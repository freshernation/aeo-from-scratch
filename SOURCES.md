# Sources

Chosen by the librarian rule: an official source for how the thing works, an
engineering account from people who build with it for why, and nothing that is a
vendor selling the answer without saying so. Three or four a week, not ten.

Every link was checked on 2026-10-29. Need something that is not here? `ai/librarian.md`.

---

## The ones worth reading twice

| Read | Why |
|---|---|
| [GEO: Generative Engine Optimization (Aggarwal et al.)](https://arxiv.org/abs/2311.09735) | The first measured study of what changes citation in generative engines. Read the method before the results |
| [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) | What the largest engine says it does, including "no additional requirements". Treat it as a claim you can test |
| [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html) | The standard every crawler claims to follow |

---

## Week 1 — How an answer engine answers

| Read | Why |
|---|---|
| [GEO paper, sections 1 to 3](https://arxiv.org/abs/2311.09735) | How a generative engine is modelled: retrieve, synthesise, cite |
| [Google: AI Mode and query fan-out](https://blog.google/products/search/google-search-ai-mode-update/) | The engine's own description of fan-out |
| [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) | The formula, for Builders writing it by hand |
| [Reciprocal rank fusion (Cormack et al.)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | Two pages; how fan-out results are merged |
| [Claude web search tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool) | What a real engine's citations look like in an API |

**Ignore for now:** articles ranking "AEO factors". None of them shows a measurement you could repeat.

## Week 2 — Measure before you change

| Read | Why |
|---|---|
| [Adding error bars to evals (Anthropic)](https://www.anthropic.com/research/statistical-approach-to-model-evals) | The same problem, for model evaluations: noisy results need intervals and paired comparisons |
| [How not to sort by average rating (Evan Miller)](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html) | The Wilson interval, explained by someone who used it in production |
| [Binomial proportion confidence interval](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval) | The formula you implement |
| [Sign test](https://en.wikipedia.org/wiki/Sign_test) | The simplest paired test, and the one you implement |

**Ignore for now:** Bayesian methods, regression on visibility. Intervals and a paired test cover this course.

## Week 3 — Can it read you?

| Read | Why |
|---|---|
| [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) | Section 2.2.2: longest match wins |
| [OpenAI's crawlers](https://platform.openai.com/docs/bots) · [Anthropic's crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) · [Perplexity's crawlers](https://docs.perplexity.ai/guides/bots) · [Google's crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) | Each vendor's own list: which bot trains, which searches, which fetches for a user |
| [The rise of the AI crawler (Vercel)](https://vercel.com/blog/the-rise-of-the-ai-crawler) | Measured from real traffic: the major AI crawlers did not render JavaScript |
| [Block indexing with noindex (Google)](https://developers.google.com/search/docs/crawling-indexing/block-indexing) | Meta tag and header, and why robots.txt must not block a noindex page |
| [Sitemaps protocol](https://www.sitemaps.org/protocol.html) · [llms.txt proposal](https://llmstxt.org/) | The first is a standard; the second is a proposal. Know which is which |

**Ignore for now:** "AI-ready" plugins that write your robots.txt for you. You will write and test one.

---

## Week 4 — Content an engine can lift

| Read | Why |
|---|---|
| [Contextual retrieval (Anthropic)](https://www.anthropic.com/engineering/contextual-retrieval) | Why a chunk that loses its context retrieves badly: the case for self-contained passages, from the retrieval side |
| [GEO paper, sections 3.3 and 4](https://arxiv.org/abs/2311.09735) | The rewriting methods it tested, and which raised visibility |
| [Inverted pyramid](https://en.wikipedia.org/wiki/Inverted_pyramid_(journalism)) | The old newsroom rule behind answer-first |
| [Google: spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Keyword stuffing, defined by an engine |

**Ignore for now:** "AI content optimizer" tools that score pages. Week 4's lift test is the score.

## Week 5 — Structured data and entities

| Read | Why |
|---|---|
| [Google: introduction to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | What markup is for, from the engine that rewards it most |
| [Google: structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) | Markup must describe what is on the page |
| [schema.org: Product](https://schema.org/Product) · [Organization](https://schema.org/Organization) · [sameAs](https://schema.org/sameAs) | The vocabulary, for reference |
| [Google: Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization) | How one company states its identity once |
| [Google: changes to HowTo and FAQ rich results (2023)](https://developers.google.com/search/blog/2023/08/howto-faq-changes) | Markup's rewards change; build for truth, not for a feature |

**Ignore for now:** microdata and RDFa; schema generator plugins.

## Week 6 — Off-site: authority, consistency, freshness

| Read | Why |
|---|---|
| [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) | What an engine says it values in sources |
| [Google: spam policies, cloaking and hidden text](https://developers.google.com/search/docs/essentials/spam-policies) | The two tactics found on this web, defined |
| [Indirect prompt injection (Greshake et al.)](https://arxiv.org/abs/2302.12173) | Instructions planted in content an AI reads: the research behind week 6's detector |
| [GEO paper, section 6](https://arxiv.org/abs/2311.09735) | The methods tried on a deployed engine |

**Ignore for now:** link-building services and "citation building" packages.

---

## Week 7 — Live engines and monitoring

| Read | Why |
|---|---|
| [Claude web search tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool) | Citations, `pause_turn`, and $10 per 1,000 searches |
| [OpenAI web search](https://platform.openai.com/docs/guides/tools-web-search) · [OpenAI pricing](https://platform.openai.com/docs/pricing) | `url_citation` annotations; $10 per 1,000 calls plus tokens |
| [Perplexity quickstart](https://docs.perplexity.ai/getting-started/quickstart) · [Perplexity pricing](https://docs.perplexity.ai/getting-started/pricing) | `citations` and `search_results`; prices by search context |
| [OpenAI's crawlers](https://platform.openai.com/docs/bots) · [Perplexity's crawlers](https://docs.perplexity.ai/guides/bots) | The published IP lists that tell a real crawler from a costume |
| [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) | The run store |

**Ignore for now:** AEO tracking dashboards. Build the thing first, then judge what they sell.

## Week 8 — Your own site

| Read | Why |
|---|---|
| Your own weeks 1 to 7 | Every tool and every report you made is the reading this week |
| [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) | Before you snapshot anyone else's site |
| [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) | Read it again, and compare with what you measured |

**Ignore for now:** anyone promising results inside thirty days.
