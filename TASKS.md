Priority tasks for AI Copilot
  - Implement newsroom_core/ingest.py functions to fetch metadata from Semantic Scholar and data.gov given URLs in sources/*.yaml. Add missing checksums (SHA-256 of fetched file) and retrieval timestamps.
  - Implement newsroom_core/extract.py to parse sources and emit atomic claims in claims/claims.yaml using prompts/extraction_prompt.md. Save model parameters into claims file header.
  - Implement newsroom_core/bias_lint.py with checks for loaded language, asymmetry, hedging. Output a report and suggested rewrites.
  - Implement website content loader (apps/main-website/src/lib/loadContent.ts) to read content/editorial-pipeline and render articles, sources, per-claim popovers.
  - Add tests for schemas (schemas/*.json) and validate content on CI.
  - Prepare social pack generator stub in newsroom_core/render.py that fills social/pack.json drafts from articles.
  - Do not publish or merge to main. Open PRs with labels per step.