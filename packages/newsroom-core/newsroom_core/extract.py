import yaml, os, glob
from .models import Claim
# TODO: Implement model adapters; for now, leave placeholders for AI to fill.
def extract_claims(topic_dir: str, prompt_path: str, model_info: dict):
    claims_dir = os.path.join(topic_dir, "claims")
    os.makedirs(claims_dir, exist_ok=True)
    claims_path = os.path.join(claims_dir, "claims.yaml")
    if not os.path.exists(claims_path):
        with open(claims_path, "w", encoding="utf-8") as f:
            f.write("# claims.yaml\n# TODO: AI populate using prompts/extraction_prompt.md\nitems: []\n")
