import yaml
from newsroom_core import extract as extract_mod

def test_extract_creates_claims_yaml(tmp_path):
    topic_dir = tmp_path / "content" / "editorial-pipeline" / "topics" / "topic-123"
    # extract_claims will create the claims dir/file as needed
    extract_mod.extract_claims(str(topic_dir), "prompts/extraction_prompt.md", {"model": "TODO"})
    claims_path = topic_dir / "claims" / "claims.yaml"
    assert claims_path.exists()
    data = yaml.safe_load(claims_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)
