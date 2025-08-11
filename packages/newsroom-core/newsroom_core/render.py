import os, yaml, json
def build_social_pack(article_md_path: str, out_path: str):
    pack = {
        "platforms": {
            "mastodon": {"text": "TODO", "alt_text": "TODO"},
            "linkedin": {"text": "TODO"},
        },
        "article_url": "TODO",
        "scheduled_at": None
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pack, f, indent=2)