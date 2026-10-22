#!/usr/bin/env python3
"""Genera il plugin WordPress (template di pagina PHP) a partire dai sorgenti comuni in ../src.

    python build.py

Produce:
    dist/aicfds-landing/        cartella del plugin (per copia diretta in wp-content/plugins/)
    dist/aicfds-landing.zip     lo stesso, pronto per Plugin → Aggiungi nuovo → Carica plugin

Le sezioni HTML di src/sections/ vengono trasformate in template-parts/*.php: il contenitore
<div class="aicfds"> di ogni widget è rimosso (nel template c'è un solo <main class="aicfds">) e i segnaposto
{{chiave}} diventano chiamate a aicfds_asset(). Loghi e immagini sono inclusi nel plugin.

Solo libreria standard di Python.
"""
import pathlib
import re
import shutil
import sys
import textwrap
import zipfile

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
SRC = ROOT / "src"
PLUGIN_SRC = HERE / "plugin"
SLUG = "aicfds-landing"
OUT = HERE / "dist" / SLUG

# chiave del segnaposto -> (file di origine nel repository, percorso dentro assets/ del plugin)
ASSETS = {
    "aic-sardegna": ("docs/assets/logos/aic-sardegna.png", "logos/aic-sardegna.png"),
    "aic-piemonte": ("docs/assets/logos/aic-piemonte.svg", "logos/aic-piemonte.svg"),
    "aic-sicilia": ("docs/assets/logos/aic-sicilia.svg", "logos/aic-sicilia.svg"),
    "aic-calabria": ("docs/assets/logos/aic-calabria.svg", "logos/aic-calabria.svg"),
    "fondazione-sardegna": ("docs/assets/logos/fondazione-sardegna.svg", "logos/fondazione-sardegna.svg"),
    "calendario": (
        "docs/assets/img/calendario-corsi-cucina-sardegna-2026.webp",
        "img/calendario-corsi-cucina-sardegna-2026.webp",
    ),
}

PART_HEADER = """<?php
/**
 * Sezione: {title}
 * Generato da src/sections/{name} con wordpress/build.py.
 *
 * @package aicfds-landing
 */

defined( 'ABSPATH' ) || exit;
?>
"""


def section_to_php(name, html):
    m = re.match(r'<!-- AICFDS · (.*?) -->\n<div class="aicfds">\n(.*)\n</div>\n?$', html, re.S)
    if not m:
        sys.exit(f"{name}: formato inatteso (commento iniziale + <div class=\"aicfds\"> ... </div>)")
    title, body = m.group(1), textwrap.dedent(m.group(2))

    unknown = set(re.findall(r"\{\{([\w-]+)\}\}", body)) - set(ASSETS)
    if unknown:
        sys.exit(f"{name}: segnaposto non mappato in ASSETS: {', '.join(sorted(unknown))}")
    if "<?" in body:
        sys.exit(f"{name}: l'HTML sorgente contiene già codice PHP")

    body = re.sub(
        r"\{\{([\w-]+)\}\}",
        lambda k: f"<?php echo esc_url( aicfds_asset( '{ASSETS[k.group(1)][1]}' ) ); ?>",
        body,
    )
    return PART_HEADER.format(title=title, name=name) + body.rstrip() + "\n"


def build():
    if OUT.parent.exists():
        shutil.rmtree(OUT.parent)
    shutil.copytree(PLUGIN_SRC, OUT)

    parts = OUT / "template-parts"
    parts.mkdir()
    sections = sorted((SRC / "sections").glob("*.html"))
    for f in sections:
        (parts / (f.stem + ".php")).write_text(section_to_php(f.name, f.read_text(encoding="utf8")), encoding="utf8")

    for sub, name in (("css", "aicfds.css"), ("js", "aicfds.js")):
        (OUT / "assets" / sub).mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / sub / name, OUT / "assets" / sub / name)

    for origin, dest in ASSETS.values():
        target = OUT / "assets" / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / origin, target)

    zip_path = OUT.parent / f"{SLUG}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.rglob("*")):
            if f.is_file():
                z.write(f, f"{SLUG}/{f.relative_to(OUT).as_posix()}")

    print(f"{len(sections)} sezioni -> template-parts/")
    print(f"plugin:  {OUT.relative_to(HERE)}")
    print(f"zip:     {zip_path.relative_to(HERE)} ({zip_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
