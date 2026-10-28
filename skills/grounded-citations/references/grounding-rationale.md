# Why Numbered Ledger IDs

Why each SKILL.md rule matters for output quality:

- **Numbered id trick** — hallucinated citations come from a model
  reconstructing a URL from memory. If it only ever emits a small integer
  handed to it at retrieval time, there's nothing to reconstruct: a wrong id
  is detectable (not in the ledger), a wrong URL is impossible (the model
  never types one — `render` does). Rule: register at retrieval, render
  mechanically; letting the model type a URL breaks the guarantee.

- **Cite while writing, not after** — research (ALCE, arXiv:2305.14627)
  shows citing during composition, from numbered retrieved snippets, beats
  adding citations after writing. Post-hoc citing invites finding a source
  that plausibly matches a sentence already written — which is how a
  citation ends up supporting something the page doesn't say. Rule: cite per
  sentence, inline, as you write — never dump citations at the end.

- **Verbatim quotes prevent drift** — research (WebGPT, arXiv:2112.09332)
  shows collecting exact quotes at browse time, then composing from them,
  beats paraphrasing. Each summarization hop risks a number drifting. Rule:
  copy-paste the source's own words for any figure/date/name/quantity.

- **Formatting rules** — matches what users expect from citation-heavy
  products: marker right after punctuation, no space (`water.[1]`); each id
  its own brackets (`[1][2]`, not `[1, 2]`); max 3 ids/sentence (beyond that,
  unclear which source backs which claim); never cite an unconsulted source;
  skip citations for translation/creative writing/casual chat.

Code Beta renders the id → URL list explicitly since it has no UI layer to
show source cards automatically.
