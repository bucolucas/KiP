Verifiable Newsroom (Mono-repo)
  Mission: Publish neutral, verifiable news with radical transparency. Every claim traceable to a primary source. Human approval required to publish.
  Quickstart
  1) Create a GitHub repository from this scaffold. Require 2FA for org members.
  2) Copy .env.example to .env and set model API keys and settings (do not commit .env).
  3) Python setup:
     - cd packages/newsroom-core && pip install -e .
     - cd tools/newsroom-cli && pip install -e .
     - Run: newsroom ingest --topic topic-0001
  4) Website:
     - cd apps/main-website && npm install && npm run dev
  5) Workflows:
     - Open an issue in research-requests or create content/editorial-pipeline/topics/topic-0002 and push a feature/topic-0002 branch.
  Transparency guarantees
  - Every article includes links to sources, claims, verification log, and PRs.
  - No content publishes without human approvals defined in CODEOWNERS.