import typer, os, json, glob, subprocess
from newsroom_core import ingest as ingest_mod, extract as extract_mod, bias_lint
app = typer.Typer()
@app.command()
def init_topic(id: str, title: str = "Untitled"):
    base = os.path.join("content", "editorial-pipeline", "topics", id)
    os.makedirs(os.path.join(base, "sources"), exist_ok=True)
    os.makedirs(os.path.join(base, "claims"), exist_ok=True)
    os.makedirs(os.path.join(base, "verification"), exist_ok=True)
    os.makedirs(os.path.join(base, "drafts"), exist_ok=True)
@app.command()
def ingest(topic: str = None, auto: bool = False):
    topics = [topic] if topic else [os.path.basename(p) for p in glob.glob("content/editorial-pipeline/topics/topic-*")]
    for t in topics:
        ingest_mod.enrich_sources(os.path.join("content", "editorial-pipeline", "topics", t))
@app.command()
def extract(topic: str = None, auto: bool = False):
    topics = [topic] if topic else [os.path.basename(p) for p in glob.glob("content/editorial-pipeline/topics/topic-*")]
    for t in topics:
        extract_mod.extract_claims(os.path.join("content", "editorial-pipeline", "topics", t), "prompts/extraction_prompt.md", {"model": "TODO"})
        ingest.enrich_sources(os.path.join("content", "editorial-pipeline", "topics", t))
@app.command()
def extract(topic: str = None, auto: bool = False):
    topics = [topic] if topic else [os.path.basename(p) for p in glob.glob("content/editorial-pipeline/topics/topic-*")]
    for t in topics:
        extract.extract_claims(os.path.join("content", "editorial-pipeline", "topics", t), "prompts/extraction_prompt.md", {"model": "TODO"})
@app.command()
def draft(topic: str = None, auto: bool = False):
    print("TODO: Implement drafting using prompts/drafting_prompt.md and Verified claims.")
@app.command()
def debias(topic: str = None, auto: bool = False):
    bias_lint.main(".")