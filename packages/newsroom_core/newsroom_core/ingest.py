import hashlib, requests, datetime, yaml, os, glob, json
from .models import Source
def sha256_of_url(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return hashlib.sha256(r.content).hexdigest()
def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
def save_yaml(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
def enrich_sources(topic_dir: str):
    src_dir = os.path.join(topic_dir, "sources")
    for y in glob.glob(os.path.join(src_dir, "*.yaml")):
        data = load_yaml(y)
        changed = False
        if not data.get("retrieved_at"):
            data["retrieved_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            changed = True
        if data.get("url") and not data.get("checksum_sha256"):
            try:
                data["checksum_sha256"] = sha256_of_url(data["url"])
                changed = True
            except Exception:
                pass
        if changed:
            save_yaml(y, data)