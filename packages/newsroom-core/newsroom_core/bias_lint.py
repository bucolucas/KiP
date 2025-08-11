import sys, re, os, glob
LOADED_WORDS = ["significant", "dramatic", "alarming", "shocking", "critical", "stunning"]
def score_text(text: str) -> dict:
    flags = []
    for w in LOADED_WORDS:
        for m in re.finditer(rf"\\b{re.escape(w)}\\b", text, flags=re.IGNORECASE):
            flags.append({"type": "loaded_word", "word": w, "index": m.start()})
    return {"flags": flags, "count": len(flags)}
def main(repo="."):
    for draft in glob.glob(os.path.join(repo, "content", "editorial-pipeline", "topics", "topic-*", "drafts", "*.md")):
        txt = open(draft, "r", encoding="utf-8").read()
        report = score_text(txt)
        print(f"{draft}: {report['count']} issues")
if __name__ == "__main__":
    main()