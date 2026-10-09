#!/usr/bin/env python3
"""Generate the schemas.metanorma.org index page from manifest.yml.

Visual language follows www.metanorma.org (brand palette, Bricolage
Grotesque / Hanken Grotesk / Space Mono, paper background, sticky
blurred header, soft footer) so the registry reads as part of the same
site family. The raw JSON of each entry stays at its canonical $id
path; the documentation SPA is generated alongside it by
lutaml-jsonschema.
"""
import html
import pathlib

import yaml

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:"
         "opsz,wght@12..96,400;12..96,600;12..96,700"
         "&family=Hanken+Grotesk:wght@400;500;600;700"
         "&family=Space+Mono&display=swap")

STYLE = """
:root {
  --brand-1: #575ABE; --brand-ink: #1F3D7A;
  --bg: #FAF8F3; --bg-soft: #F4F1EA; --bg-mute: #ECE7DC; --bg-elv: #FFFFFF;
  --nav-bg: rgba(253, 252, 250, 0.92);
  --text-1: #14223D; --text-2: #3F4A63; --text-3: #6F7689;
  --divider: #DCD6C7;
  --shadow: 0 1px 2px rgba(20, 34, 61, 0.05);
}
.dark {
  --brand-1: #A5A8E5; --brand-ink: #A5A8E5;
  --bg: #0B0F1C; --bg-soft: #11172A; --bg-mute: #1A2138; --bg-elv: #161D33;
  --nav-bg: rgba(11, 15, 28, 0.92);
  --text-1: #ECEFF8; --text-2: #A6ADBF; --text-3: #7C8296;
  --divider: #232B45;
  --shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
}
* { box-sizing: border-box; }
html { color-scheme: light; }
html.dark { color-scheme: dark; }
.not-dark { }
html.dark .not-dark { display: none; }
.only-dark { display: none; }
html.dark .only-dark { display: block; }
body {
  margin: 0; background: var(--bg); color: var(--text-1);
  font: 16px/1.65 'Hanken Grotesk', ui-sans-serif, system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--brand-1); text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: 'Space Mono', ui-monospace, SFMono-Regular, monospace; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 1.5rem; }
header.site {
  position: sticky; top: 0; z-index: 50;
  border-bottom: 1px solid var(--divider);
  background: var(--nav-bg); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}
header.site .wrap {
  display: flex; align-items: center; justify-content: space-between;
  height: 64px; gap: 1.5rem;
}
.brand { display: flex; align-items: center; gap: 0.9rem; }
.brand img { height: 32px; width: auto; }
.brand .wordmark {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 600;
  font-size: 1.05rem; color: var(--text-1); letter-spacing: -0.01em;
}
.brand .wordmark .dim { color: var(--text-3); font-weight: 400; }
.topnav { display: flex; align-items: center; gap: 1.25rem; }
.topnav a.navlink {
  font-size: 0.875rem; font-weight: 500; color: var(--text-2);
}
.topnav a.navlink:hover { color: var(--brand-1); text-decoration: none; }
.theme-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 8px; cursor: pointer;
  border: 1px solid var(--divider); background: var(--bg-elv); color: var(--text-2);
}
.theme-btn:hover { color: var(--brand-1); border-color: var(--brand-1); }
.theme-btn .sun { display: none; }
html.dark .theme-btn .sun { display: block; }
html.dark .theme-btn .moon { display: none; }
.hero .wrap { padding: 4.5rem 1.5rem 3rem; max-width: 820px; }
.hero .eyebrow {
  margin: 0 0 0.75rem; font-size: 0.75rem; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-3);
}
.hero h1 {
  margin: 0 0 0.9rem; font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 700; font-size: clamp(1.9rem, 4vw, 2.6rem);
  line-height: 1.15; letter-spacing: -0.02em; color: var(--text-1);
}
.hero p.lead { margin: 0; font-size: 1.1rem; color: var(--text-2); max-width: 62ch; }
main.listing .wrap { padding: 0 1.5rem 4rem; }
.listing h2 {
  margin: 0 0 1.25rem; font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-3);
}
.card {
  border: 1px solid var(--divider); border-radius: 12px;
  background: var(--bg-elv); box-shadow: var(--shadow);
  padding: 1.5rem 1.6rem; margin-bottom: 1rem;
  transition: border-color .15s ease, box-shadow .15s ease;
}
.card:hover {
  border-color: rgba(87, 90, 190, 0.45);
  box-shadow: 0 4px 16px rgba(20, 34, 61, 0.08);
}
.dark .card:hover { box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5); }
.card h3 { margin: 0 0 0.45rem; font-family: 'Bricolage Grotesque', sans-serif; font-weight: 600; font-size: 1.12rem; }
.card h3 a { color: var(--text-1); }
.card h3 a:hover { color: var(--brand-1); text-decoration: none; }
.card .idpath {
  margin: 0 0 1rem; font-size: 0.82rem; color: var(--text-3);
}
.card .idpath code {
  background: var(--bg-soft); border: 1px solid var(--divider);
  border-radius: 6px; padding: 0.2rem 0.5rem; word-break: break-all;
}
.chips { display: flex; flex-wrap: wrap; gap: 0.55rem; }
.chip {
  display: inline-flex; align-items: center; border-radius: 999px;
  padding: 0.34rem 0.95rem; font-size: 0.85rem; font-weight: 500;
  border: 1px solid var(--divider); color: var(--text-2);
}
.chip:hover { color: var(--brand-1); border-color: var(--brand-1); text-decoration: none; }
.chip.primary { background: var(--brand-1); border-color: var(--brand-1); color: #fff; }
html.dark .chip.primary { color: #0B0F1C; }
.chip.primary:hover { opacity: 0.88; text-decoration: none; }
footer.site { border-top: 1px solid var(--divider); background: var(--bg-soft); }
footer.site .wrap { padding: 2.75rem 1.5rem 2rem; }
.foot-grid {
  display: flex; flex-wrap: wrap; gap: 2.5rem; justify-content: space-between;
  padding-bottom: 2rem;
}
.foot-brand img { height: 28px; margin-bottom: 0.6rem; }
.foot-brand .tag { margin: 0; font-size: 0.875rem; color: var(--text-3); }
.foot-cols { display: flex; gap: 3.5rem; flex-wrap: wrap; }
.foot-cols h4 {
  margin: 0 0 0.75rem; font-size: 0.7rem; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-3);
}
.foot-cols ul { list-style: none; margin: 0; padding: 0; }
.foot-cols li { margin-bottom: 0.5rem; }
.foot-cols a { font-size: 0.875rem; color: var(--text-2); }
.foot-cols a:hover { color: var(--brand-1); }
.foot-legal {
  display: flex; flex-wrap: wrap; gap: 1rem; justify-content: space-between;
  border-top: 1px solid var(--divider); padding-top: 1.5rem;
  font-size: 0.85rem; color: var(--text-3);
}
.foot-legal a { color: var(--text-3); }
.foot-legal a:hover { color: var(--brand-1); }
.foot-legal .legal-links { display: flex; gap: 1.25rem; }
"""

TOGGLE = """
<script>
(function () {
  var key = 'mn-theme';
  var root = document.documentElement;
  document.querySelector('.theme-btn').addEventListener('click', function () {
    root.classList.toggle('dark');
    try { localStorage.setItem(key, root.classList.contains('dark') ? 'dark' : 'light'); } catch (e) {}
  });
})();
</script>
"""

ANTIFOUC = ("<script>(function(){try{var t=localStorage.getItem('mn-theme');"
            "if(t==='dark'||(!t&&matchMedia('(prefers-color-scheme: dark)').matches))"
            "document.documentElement.classList.add('dark');}catch(e){}})();</script>")

CARD = """
<article class="card">
  <h3><a href="{docs}">{title}</a></h3>
  <p class="idpath"><code>https://schemas.metanorma.org{path}</code></p>
  <div class="chips">
    <a class="chip primary" href="{docs}">Documentation</a>
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
<title>Schema Registry — Metanorma</title>
<meta name="description" content="Canonical, versioned schema contracts of the Metanorma ecosystem, served at their permanent $id paths.">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
{antifouc}
<style>{style}</style>
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Metanorma schema registry home">
      <img src="/assets/metanorma-logo_full-light.svg" alt="Metanorma" class="not-dark">
      <img src="/assets/metanorma-logo_full-dark.svg" alt="Metanorma" class="only-dark">
      <span class="wordmark">/ <span class="dim">schemas</span></span>
    </a>
    <nav class="topnav" aria-label="Primary">
      <a class="navlink" href="https://www.metanorma.org/">metanorma.org</a>
      <a class="navlink" href="https://github.com/metanorma">GitHub</a>
      <button class="theme-btn" aria-label="Toggle dark mode" type="button">
        <svg class="moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="sun" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Metanorma</p>
    <h1>Schema Registry</h1>
    <p class="lead">Canonical, versioned schema contracts of the Metanorma
    ecosystem. Schemas are owned by their product repositories and served
    here at their permanent <code>$id</code> paths.</p>
  </div>
</section>

<main class="listing">
  <div class="wrap">
    <h2>Published schemas</h2>
    {cards}
  </div>
</main>

<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="/assets/metanorma-logo_full-light.svg" alt="Metanorma" class="not-dark">
        <img src="/assets/metanorma-logo_full-dark.svg" alt="Metanorma" class="only-dark">
        <p class="tag">The standard of standards</p>
      </div>
      <div class="foot-cols">
        <div>
          <h4>Registry</h4>
          <ul>
            <li><a href="https://github.com/metanorma/schemas">metanorma/schemas</a></li>
            <li><a href="https://github.com/metanorma/standards-registry">standards-registry</a></li>
            <li><a href="https://github.com/lutaml/lutaml-jsonschema">lutaml-jsonschema</a></li>
          </ul>
        </div>
        <div>
          <h4>Metanorma</h4>
          <ul>
            <li><a href="https://www.metanorma.org/">www.metanorma.org</a></li>
            <li><a href="https://github.com/metanorma">GitHub</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="foot-legal">
      <p>&copy; {year} Ribose Group Inc. All rights reserved.</p>
      <div class="legal-links">
        <a href="https://www.ribose.com/tos">Terms of Service</a>
        <a href="https://www.ribose.com/privacy">Privacy Policy</a>
      </div>
    </div>
  </div>
</footer>
{toggle}
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
    out.write_text(
        PAGE.format(
            fonts=FONTS,
            antifouc=ANTIFOUC,
            style=STYLE,
            cards=cards,
            year=__import__("datetime").date.today().year,
            toggle=TOGGLE,
        )
    )
    print(f"index written: {out} ({len(manifest)} schemas)")


if __name__ == "__main__":
    main()
