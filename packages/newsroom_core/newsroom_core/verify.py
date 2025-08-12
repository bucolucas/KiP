import json, os, yaml, glob, sys, datetime
from jsonschema import validate

def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _to_json_types(obj):
    # Recursively convert datetime/date to ISO strings; leave others unchanged
    if isinstance(obj, datetime.datetime):
        # If UTC, prefer Z suffix for readability
        if obj.tzinfo is not None and obj.tzinfo.utcoffset(obj) == datetime.timedelta(0):
            return obj.replace(tzinfo=None).isoformat() + "Z"
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _to_json_types(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_json_types(v) for v in obj]
    return obj


def validate_schemas(repo_root: str = "."):
    schemas = {
        "source": _load_json(os.path.join(repo_root, "schemas", "source.schema.json")),
        "claim": _load_json(os.path.join(repo_root, "schemas", "claim.schema.json")),
        "verification": _load_json(os.path.join(repo_root, "schemas", "verification.schema.json")),
    }
    for topic in glob.glob(os.path.join(repo_root, "content", "editorial-pipeline", "topics", "topic-*")):
        for p in glob.glob(os.path.join(topic, "sources", "*.yaml")):
            with open(p, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            data = _to_json_types(data)
            validate(instance=data, schema=schemas["source"])
        claims = os.path.join(topic, "claims", "claims.yaml")
        if os.path.exists(claims):
            with open(claims, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            data = _to_json_types(data)
            if isinstance(data, dict) and "items" in data:
                for item in data["items"]:
                    validate(instance=item, schema=schemas["claim"])
        ver = os.path.join(topic, "verification", "verification-log.json")
        if os.path.exists(ver):
            with open(ver, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            # Verification is JSON; still normalize just in case
            data = _to_json_types(data)
            for item in data.get("items", []):
                validate(instance=item, schema=schemas["verification"])


if __name__ == "__main__":
    validate_schemas()
