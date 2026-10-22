# Numbrik

Free online calculators — https://numbrik.com

## Folders

- `numbrik/` — the live website (static HTML, CSS and JS). Cloudflare deploys this folder.
- `numbrik-source/` — the source used to build the website.

## Rebuilding the site

From `numbrik-source/`:

1. `npm install` inside `fontsrc/` (downloads the self-hosted fonts).
2. `python3 build.py` — writes the finished site to `dist/`.
3. Copy the contents of `dist/` into the `numbrik/` folder and commit.

Page text lives in `content.py`, `content2.py`, `content3.py` and `more.py`. Calculator code is in `src/app.js`.
