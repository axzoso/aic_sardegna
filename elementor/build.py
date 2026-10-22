#!/usr/bin/env python3
"""Genera i file da incollare in Elementor a partire da src/ e urls.json.

    python build.py            -> dist/widgets/*.html, dist/aicfds.css
    python build.py --preview  -> in più dist/preview.html (pagina di prova con gli stili reali del sito,
                                   scarica la home di sardegna.celiachia.it per leggere i CSS del tema)

Solo libreria standard di Python.
"""
import json
import pathlib
import re
import shutil
import sys
import urllib.request

HERE = pathlib.Path(__file__).parent
SRC, DIST = HERE.parent / "src", HERE / "dist"
SITE = "https://sardegna.celiachia.it/"


def load_urls():
    urls = json.loads((HERE / "urls.json").read_text(encoding="utf8"))
    missing = [k for k, v in urls.items() if not v.startswith("https://")]
    if missing:
        sys.exit(f"urls.json: URL mancante o non valido per: {', '.join(missing)}")
    return urls


def adapt(name, html):
    """Adattamenti specifici della versione Elementor.

    Il tema stampa già il titolo della pagina come <h1> (Post Title del Theme Builder): il titolo dell'hero
    diventa <h2>, per non avere due <h1>. Nella versione PHP (pagina senza titolo del tema) resta <h1>.
    """
    if name.startswith("01-"):
        html = html.replace('<h1 id="hero-title"', '<h2 id="hero-title"').replace("</h1>", "</h2>")
    return html


def build_widgets(urls):
    out = DIST / "widgets"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    names = []
    for src in sorted((SRC / "sections").glob("*.html")):
        html = src.read_text(encoding="utf8")
        unknown = set(re.findall(r"\{\{([\w-]+)\}\}", html)) - set(urls)
        if unknown:
            sys.exit(f"{src.name}: segnaposto senza URL in urls.json: {', '.join(sorted(unknown))}")
        html = re.sub(r"\{\{([\w-]+)\}\}", lambda m: urls[m.group(1)], adapt(src.name, html))
        (out / src.name).write_text(html, encoding="utf8")
        names.append(src.name)

    js = (SRC / "js" / "aicfds.js").read_text(encoding="utf8")
    (out / "99-script.html").write_text(f"<script>\n{js}</script>\n", encoding="utf8")
    names.append("99-script.html")

    shutil.copy(SRC / "css" / "aicfds.css", DIST / "aicfds.css")
    return names


def build_preview(names):
    """Pagina locale che imita la pagina Elementor: CSS reali del sito + i widget in sequenza."""
    req = urllib.request.Request(SITE, headers={"User-Agent": "Mozilla/5.0"})
    home = urllib.request.urlopen(req, timeout=30).read().decode("utf8", "replace")
    sheets = re.findall(r"<link[^>]+rel=['\"]stylesheet['\"][^>]*href=['\"]([^'\"]+)['\"]", home)
    sheets = [s for s in sheets if "complianz" not in s]
    body_class = re.search(r"<body[^>]*class=['\"]([^'\"]*)['\"]", home)
    body_class = body_class.group(1) if body_class else ""

    parts = []
    for n in names:
        content = (DIST / "widgets" / n).read_text(encoding="utf8")
        parts.append(
            '<div class="elementor-element elementor-widget elementor-widget-html">'
            f'<div class="elementor-widget-container">\n{content}</div></div>'
        )
    links = "\n".join(f'<link rel="stylesheet" href="{s}">' for s in sheets)
    page = f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anteprima widget Elementor (solo test locale)</title>
{links}
<style>
@font-face {{ font-family:"Asap"; font-weight:400; src:url("../../docs/assets/fonts/asap-latin-400-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Asap"; font-weight:400; font-style:italic; src:url("../../docs/assets/fonts/asap-latin-400-italic.woff2") format("woff2"); }}
@font-face {{ font-family:"Asap"; font-weight:500; src:url("../../docs/assets/fonts/asap-latin-500-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Asap"; font-weight:600; src:url("../../docs/assets/fonts/asap-latin-600-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Asap"; font-weight:700; src:url("../../docs/assets/fonts/asap-latin-700-normal.woff2") format("woff2"); }}
</style>
<link rel="stylesheet" href="aicfds.css">
</head>
<body class="{body_class}">
<!-- Colonna del tema: #aic-main-content ha padding 30px e il contenuto utile arriva a 822px -->
<section id="aic-main-content" style="max-width:882px;margin:0 auto;padding:30px;box-sizing:border-box;background:#fff">
<div class="elementor-widget-wrap" style="display:flex;flex-direction:column">
{chr(10).join(parts)}
</div></section>
</body></html>
"""
    (DIST / "preview.html").write_text(page, encoding="utf8")


if __name__ == "__main__":
    names = build_widgets(load_urls())
    print(f"dist/aicfds.css + {len(names)} widget:")
    for n in names:
        print("  ", n)
    if "--preview" in sys.argv:
        build_preview(names)
        print("dist/preview.html")
