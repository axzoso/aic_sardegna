# Landing page — Educazione, Supporto e Cucina Senza Barriere

Prototipo statico della pagina one page del progetto interregionale AIC Sardegna (capofila),
AIC Piemonte, AIC Sicilia e AIC Calabria, realizzato con il contributo della Fondazione di Sardegna.
Specifiche complete in [CLAUDE.md](CLAUDE.md).

## Struttura

```
docs/                 ← sito pubblicato da GitHub Pages
  index.html
  404.html
  .nojekyll           ← disattiva Jekyll (serve i file così come sono)
  assets/
    css/style.css
    js/main.js
    fonts/            ← Asap self-hosted (OFL), stesso font di sardegna.celiachia.it
    logos/            ← loghi web (SVG convertiti dai PDF, PNG AIC Sardegna)
    img/
```

Tutti i percorsi sono relativi: il sito funziona sia su `https://<utente>.github.io/<repo>/`
sia in locale.

## Anteprima locale

```sh
cd docs
python -m http.server 8000
# http://localhost:8000
```

## Pubblicazione su GitHub Pages

1. Creare il repository su GitHub e fare push del branch `main`.
2. *Settings → Pages → Build and deployment*: Source **Deploy from a branch**,
   Branch **main**, cartella **/docs**.
3. Dopo circa un minuto la pagina è online su `https://<utente>.github.io/<repo>/`.

> **Attenzione**: il `.gitignore` esclude i PDF con dati personali/bancari
> (`Fondazione/20251205-ModuloRichiesta-*.pdf`) e le note operative interne. Se il repository
> è pubblico, verificare con `git status` prima del primo commit che non vengano inclusi.
> Il prototipo ha `noindex, nofollow`: rimuoverlo solo nella versione definitiva.
