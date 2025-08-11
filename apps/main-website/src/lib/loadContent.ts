import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const CONTENT_DIR =
  process.env.CONTENT_DIR ||
  path.resolve(process.cwd(), '../../content/editorial-pipeline');

function safeReaddir(p: string) {
  try { return fs.readdirSync(p); } catch { return []; }
}

export function listArticles() {
  const topicsRoot = path.join(CONTENT_DIR, 'topics');
  const topics = safeReaddir(topicsRoot);
  const items: { slug: string; title: string; path: string }[] = [];
  for (const t of topics) {
    const artDir = path.join(topicsRoot, t, 'articles');
    for (const f of safeReaddir(artDir)) {
      if (!f.endsWith('.md')) continue;
      const p = path.join(artDir, f);
      const raw = fs.readFileSync(p, 'utf-8');
      const fm = matter(raw);
      items.push({
        slug: (fm.data as any).slug || f.replace(/\.md$/, ''),
        title: (fm.data as any).title || f.replace(/\.md$/, ''),
        path: p
      });
    }
  }
  return items;
}

export function getArticle(slug: string) {
  const topicsRoot = path.join(CONTENT_DIR, 'topics');
  const topics = safeReaddir(topicsRoot);
  for (const t of topics) {
    const artDir = path.join(topicsRoot, t, 'articles');
    for (const f of safeReaddir(artDir)) {
      const p = path.join(artDir, f);
      if (!p.endsWith('.md')) continue;
      const raw = fs.readFileSync(p, 'utf-8');
      const fm = matter(raw);
      const s = (fm.data as any).slug || f.replace(/\.md$/, '');
      if (s === slug) {
        return { frontmatter: fm.data as any, content: fm.content, topic: t };
      }
    }
  }
  return null;
}