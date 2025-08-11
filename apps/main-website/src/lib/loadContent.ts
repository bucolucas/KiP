import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
const root = path.resolve(process.cwd(), '../../content/editorial-pipeline');
export function listArticles() {
const topics = fs.readdirSync(path.join(root, 'topics'));
const items = [];
for (const t of topics) {
    const artDir = path.join(root, 'topics', t, 'articles');
    if (fs.existsSync(artDir)) {
    for (const f of fs.readdirSync(artDir)) {
        const p = path.join(artDir, f);
        const raw = fs.readFileSync(p, 'utf-8');
        const fm = matter(raw);
        items.push({ slug: fm.data.slug || f.replace('.md',''), title: fm.data.title, path: p });
    }
    }
}
return items;
}
export function getArticle(slug: string) {
const topics = fs.readdirSync(path.join(root, 'topics'));
for (const t of topics) {
    const artDir = path.join(root, 'topics', t, 'articles');
    if (!fs.existsSync(artDir)) continue;
    for (const f of fs.readdirSync(artDir)) {
    const p = path.join(artDir, f);
    const raw = fs.readFileSync(p, 'utf-8');
    const fm = matter(raw);
    if ((fm.data.slug || f.replace('.md','')) === slug) {
        return { frontmatter: fm.data, content: fm.content, topic: t };
    }
    }
}
return null;
}