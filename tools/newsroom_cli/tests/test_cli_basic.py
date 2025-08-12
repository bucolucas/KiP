import os, json
from typer.testing import CliRunner
from newsroom_cli.cli import app

runner = CliRunner()

def test_init_topic_scaffold(tmp_path, monkeypatch):
    # Run in tmp repo root
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init-topic", "--id", "topic-1", "--title", "Hello"])
    assert result.exit_code == 0
    base = tmp_path / "content" / "editorial-pipeline" / "topics" / "topic-1"
    # core dirs
    for d in ["sources", "claims", "verification", "drafts", "articles", "social", "assets-manifests"]:
        assert (base / d).exists()
    # topic.json seeded
    meta = json.loads((base / "topic.json").read_text())
    assert meta["id"] == "topic-1"


def test_cli_commands_exist():
    # Ensure core commands are registered
    commands = {c.name for c in app.registered_commands}
    assert {"init-topic", "ingest", "extract", "draft", "verify-assist", "render-social", "debias"}.issubset(commands)
