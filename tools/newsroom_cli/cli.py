import typer, os, json, glob, subprocess, datetime
from typing import List, Dict
import yaml
from newsroom_core import ingest as ingest_mod, extract as extract_mod, bias_lint
from newsroom_core import render as render_mod

app = typer.Typer()


def _topic_dirs(topic: str | None) -> List[str]:
    if topic:
        return [os.path.basename(topic)] if os.path.sep not in topic else [os.path.basename(topic)]
    return [os.path.basename(p) for p in glob.glob("content/editorial-pipeline/topics/topic-*")]


@app.command("init-topic")
def init_topic(id: str, title: str = "Untitled"):
    base = os.path.join("content", "editorial-pipeline", "topics", id)
    # core scaffold
    os.makedirs(os.path.join(base, "sources"), exist_ok=True)
    os.makedirs(os.path.join(base, "claims"), exist_ok=True)
    os.makedirs(os.path.join(base, "verification"), exist_ok=True)
    os.makedirs(os.path.join(base, "drafts"), exist_ok=True)
    # extended scaffold per spec
    os.makedirs(os.path.join(base, "articles"), exist_ok=True)
    os.makedirs(os.path.join(base, "social"), exist_ok=True)
    os.makedirs(os.path.join(base, "assets-manifests"), exist_ok=True)
    # seed minimal files
    meta_path = os.path.join(base, "topic.json")
    if not os.path.exists(meta_path):
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({"id": id, "title": title, "created_at": datetime.datetime.utcnow().isoformat() + "Z"}, f, indent=2)


@app.command()
def ingest(topic: str = None, auto: bool = False):
    topics = _topic_dirs(topic)
    for t in topics:
        ingest_mod.enrich_sources(os.path.join("content", "editorial-pipeline", "topics", t))


@app.command()
def extract(topic: str = None, auto: bool = False):
    topics = _topic_dirs(topic)
    for t in topics:
        extract_mod.extract_claims(
            os.path.join("content", "editorial-pipeline", "topics", t),
            "prompts/extraction_prompt.md",
            {"model": "TODO"},
        )


@app.command()
def draft(topic: str = None, auto: bool = False):
    """Create a draft using only Verified claims.
    Fails if any claims in verification log are not Verified.
    """
    topics = _topic_dirs(topic)
    failed_any = False
    for t in topics:
        base = os.path.join("content", "editorial-pipeline", "topics", t)
        ver_path = os.path.join(base, "verification", "verification-log.json")
        claims_path = os.path.join(base, "claims", "claims.yaml")
        if not os.path.exists(ver_path) or not os.path.exists(claims_path):
            typer.echo(f"[draft] Skipping {t}: missing verification or claims.")
            continue
        with open(ver_path, "r", encoding="utf-8") as f:
            ver = json.load(f)
        with open(claims_path, "r", encoding="utf-8") as f:
            claims_doc = yaml.safe_load(f) or {}
        claims_items = claims_doc.get("items", [])
        status_map: Dict[str, str] = {i.get("claim_id"): i.get("status") for i in ver.get("items", [])}
        unverified = [cid for cid, st in status_map.items() if st != "Verified"]
        if unverified:
            failed_any = True
            typer.echo(f"[draft] {t}: found non-Verified claims: {', '.join(unverified)}", err=True)
            continue
        verified_claims = [c for c in claims_items if status_map.get(c.get("claim_id")) == "Verified"]
        # Render a minimal markdown draft embedding [C:nnn]
        lines = [f"# Draft: {t}", "", "## Claims", ""]
        for idx, c in enumerate(verified_claims, start=1):
            cid = c.get("claim_id") or f"C{idx:03d}"
            lines.append(f"- [C:{idx:03d}] {c.get('text','')}")
        lines.extend(["", "## Body", "", "TODO: Expand based on prompts/drafting_prompt.md using Verified claims only."])
        drafts_dir = os.path.join(base, "drafts")
        os.makedirs(drafts_dir, exist_ok=True)
        out_md = os.path.join(drafts_dir, f"{datetime.date.today().isoformat()}-draft.md")
        with open(out_md, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        typer.echo(f"[draft] Wrote {out_md}")
    if failed_any:
        raise typer.Exit(code=1)


@app.command("verify-assist")
def verify_assist(topic: str = None):
    """Generate a verification assistance checklist for claims lacking verification."""
    topics = _topic_dirs(topic)
    for t in topics:
        base = os.path.join("content", "editorial-pipeline", "topics", t)
        claims_path = os.path.join(base, "claims", "claims.yaml")
        ver_path = os.path.join(base, "verification", "verification-log.json")
        if not os.path.exists(claims_path):
            typer.echo(f"[verify-assist] Skipping {t}: no claims.yaml")
            continue
        with open(claims_path, "r", encoding="utf-8") as f:
            claims_doc = yaml.safe_load(f) or {}
        claims_items = claims_doc.get("items", [])
        ver_map: Dict[str, str] = {}
        if os.path.exists(ver_path):
            with open(ver_path, "r", encoding="utf-8") as f:
                ver = json.load(f)
            ver_map = {i.get("claim_id"): i.get("status") for i in ver.get("items", [])}
        todo = []
        for c in claims_items:
            cid = c.get("claim_id")
            st = ver_map.get(cid)
            if st != "Verified":
                todo.append({
                    "claim_id": cid,
                    "text": c.get("text"),
                    "status": st or "Unverified",
                })
        assist_dir = os.path.join(base, "verification")
        os.makedirs(assist_dir, exist_ok=True)
        out_path = os.path.join(assist_dir, "assist.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"items": todo}, f, indent=2)
        typer.echo(f"[verify-assist] Wrote {out_path} ({len(todo)} items)")


@app.command("render-social")
def render_social(topic: str, article_md: str = None):
    """Render social pack JSON for a given topic/article."""
    base = os.path.join("content", "editorial-pipeline", "topics", topic)
    if article_md is None:
        # pick latest draft
        drafts = sorted(glob.glob(os.path.join(base, "drafts", "*.md")))
        if not drafts:
            typer.echo(f"[render-social] No drafts found for {topic}", err=True)
            raise typer.Exit(code=1)
        article_md = drafts[-1]
    out = os.path.join(base, "social", os.path.splitext(os.path.basename(article_md))[0] + "-social.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_mod.build_social_pack(article_md, out)
    typer.echo(f"[render-social] Wrote {out}")


@app.command()
def debias(topic: str = None, auto: bool = False):
    bias_lint.main(".")
