import json, os, yaml, glob, sys
from jsonschema import validate
def _load_json(path): 
    with open(path, "r", encoding="utf-8") as f: 
        return json.load(f)
def validate_schemas(repo_root: str = "."):
    schemas = {
        "source": _load_json(os.path.join(repo_root, "schemas", "source.schema.json")),
        "claim": _load_json(os.path.join(repo_root, "schemas", "claim.schema.json")),
        "verification": _load_json(os.path.join(repo_root, "schemas", "verification.schema.json")),
    }
    for topic in glob.glob(os.path.join(repo_root, "content", "editorial-pipeline", "topics", "topic-*")):
        for p in glob.glob(os.path.join(topic, "sources", "*.yaml")):
            data = yaml.safe_load(open(p, "r", encoding="utf-8"))
            validate(instance=data, schema=schemas["source"])
        claims = os.path.join(topic, "claims", "claims.yaml")
        if os.path.exists(claims):
            data = yaml.safe_load(open(claims, "r", encoding="utf-8"))
            if isinstance(data, dict) and "items" in data:
                for item in data["items"]:
                    validate(instance=item, schema=schemas["claim"])
        ver = os.path.join(topic, "verification", "verification-log.json")
        if os.path.exists(ver):
            data = json.load(open(ver, "r", encoding="utf-8"))
            for item in data.get("items", []):
                validate(instance=item, schema=schemas["verification"])
if __name__ == "__main__":
    validate_schemas()