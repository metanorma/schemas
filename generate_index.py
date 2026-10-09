#!/usr/bin/env python3
"""Generate the schemas.metanorma.org index page from manifest.yml.

The raw JSON of each entry stays at its canonical $id path; the
documentation SPA is generated alongside it by lutaml-jsonschema. This
page is the catalog linking both.
"""
import html
import pathlib

import yaml

STYLE = """
:root {
  --bg: #ffffff; --bg-soft: #f8fafc; --card: #ffffff;
  --text: #0f172a; --muted: #64748b; --border: #e2e8f0;
  --accent: #4f46e5; --accent-soft: #eef2ff;
  --chip: #f1f5f9; --code-bg: #f8fafc;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0b1120; --bg-soft: #0f172a; --card: #101a2e;
    --text: #e2e8f0; --muted: #94a3b8; --border: #1e293b;
    --accent: #818cf8; --accent-soft: #1e1b4b;
    --chip: #1e293b; --code-bg: #0f172a;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, monospace; }
.wrap { max-width: 52rem; margin: 0 auto; padding: 0 1.5rem; }
header { border-bottom: 1px solid var(--border); background: var(--bg-soft); }
header .wrap { padding: 3.5rem 1.5rem 2.5rem; }
h1 { margin: 0 0 .5rem; font-size: 1.9rem; letter-spacing: -.02em; }
.tagline { margin: 0; color: var(--muted); font-size: 1.05rem; }
main .wrap { padding: 2.5rem 1.5rem 4rem; }
h2 { font-size: 1.15rem; letter-spacing: -.01em; margin: 0 0 1.25rem; }
.card {
  border: 1px solid var(--border); border-radius: .75rem; background: var(--card);
  padding: 1.4rem 1.5rem; margin-bottom: 1rem;
  transition: border-color .15s ease;
}
.card:hover { border-color: var(--accent); }
.card-title { margin: 0 0 .35rem; font-size: 1.1rem; }
.card-title a { color: var(--text); }
.card-title a:hover { color: var(--accent); text-decoration: none; }
.card-path {
  margin: 0 0 .9rem; color: var(--muted); font-size: .85rem;
  word-break: break-all;
}
.card-path code {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: .375rem; padding: .15rem .45rem;
}
.chips { display: flex; flex-wrap: wrap; gap: .5rem; }
.chip {
  display: inline-flex; align-items: center; gap: .35rem;
  background: var(--chip); color: var(--text);
  border-radius: 999px; padding: .3rem .85rem; font-size: .85rem;
}
.chip:hover { background: var(--accent-soft); text-decoration: none; }
.chip-primary { background: var(--accent); color: #fff; }
.chip-primary:hover { background: var(--accent); opacity: .88; text-decoration: none; }
footer { border-top: 1px solid var(--border); color: var(--muted); font-size: .85rem; }
footer .wrap { padding: 1.5rem; }
footer code { color: var(--text); }
"""

CARD = """
<article class="card">
  <h3 class="card-title"><a href="{docs}">{title}</a></h3>
  <p class="card-path"><code>https://schemas.metanorma.org{path}</code></p>
  <div class="chips">
    <a class="chip chip-primary" href="{docs}">Documentation</a>
    <a class="chip" href="{path}">Raw JSON</a>
    <a class="chip" href="{source}">Source repository</a>
  </div>
</article>
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>schemas.metanorma.org</title>
<meta name="description" content="Canonical, versioned schema contracts of the Metanorma ecosystem.">
<style>{style}</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>schemas.metanorma.org</h1>
    <p class="tagline">Canonical, versioned schema contracts of the Metanorma
    ecosystem. Schemas are owned by their product repositories and served
    here at their permanent <code>$id</code> paths.</p>
  </div>
</header>
<main>
  <div class="wrap">
    <h2>Published schemas</h2>
    {cards}
  </div>
</main>
<footer>
  <div class="wrap">
    Regenerated from <code>manifest.yml</code> on every change — to publish a
    schema, add one manifest entry. Documentation pages are generated with
    <a href="https://github.com/lutaml/lutaml-jsonschema">lutaml-jsonschema</a>.
  </div>
</footer>
</body>
</html>
"""


def main():
    manifest = yaml.safe_load(open("manifest.yml"))["schemas"]
    cards = "".join(
        CARD.format(
            title=html.escape(e["title"]),
            path=html.escape(e["path"]),
            docs=html.escape(e["path"].removesuffix(".json") + "/"),
            source=html.escape(e["source"]),
        )
        for e in manifest
    )
    out = pathlib.Path("site/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.format(style=STYLE, cards=cards))
    print(f"index written: {out} ({len(manifest)} schemas)")


if __name__ == "__main__":
    main()
