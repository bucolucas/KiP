Verifiable Newsroom (Mono-repo)
Mission: Publish neutral, verifiable news with radical transparency. Every claim traceable to a primary source. Human approval required to publish.
Quickstart
1) Create a GitHub repository from this scaffold. Require 2FA for org members.
2) Copy .env.example to .env and set model API keys and settings (do not commit .env).
3) Python setup (from repo root):
   - python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
   - python -m pip install --upgrade pip setuptools wheel
   - python -m pip install -r requirements-dev.txt
   - Run: newsroom ingest --topic topic-0001
4) Website:
   - cd apps/main-website && npm install && npm run dev
5) Workflows:
   - Open an issue in research-requests or create content/editorial-pipeline/topics/topic-0002 and push a feature/topic-0002 branch.
Troubleshooting
- ModuleNotFoundError: No module named 'newsroom_cli' or 'newsroom_core'
  - Ensure the venv is active and pip uses the same interpreter as python:
    - python -c "import sys; print(sys.executable)"; python -m pip -V
  - Reinstall editable packages:
    - python -m pip install -e packages/newsroom_core -U
    - python -m pip install -e tools/newsroom_cli -U
  - Quick, no-install test (from repo root):
    - macOS/Linux: export PYTHONPATH="$PWD/packages/newsroom_core:$PWD/tools/newsroom_cli"; python -m newsroom_cli.cli --help
    - Windows PS: $env:PYTHONPATH="$PWD\packages\newsroom_core;$PWD\tools\newsroom_cli"; python -m newsroom_cli.cli --help
Transparency guarantees
- Every article includes links to sources, claims, verification log, and PRs.
- No content publishes without human approvals defined in CODEOWNERS.
