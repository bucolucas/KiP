import { defineConfig } from 'astro/config';
import path from 'node:path';

const repoRoot = path.resolve(process.cwd(), '..', '..'); // from apps/main-website to repo root
const contentDir = path.join(repoRoot, 'content');        // allow all content/*

export default defineConfig({
  output: 'static',
  vite: {
    server: {
      fs: {
        allow: [repoRoot, contentDir]
      }
    }
  }
});