# Versione per Elementor (widget HTML)

La landing page del prototipo (`docs/`) rifattorizzata per essere incollata in **widget HTML di Elementor**,
una sezione per widget. Gli stili sono in un unico file, da incollare nel CSS personalizzato della pagina.
I sorgenti (sezioni HTML, CSS, JS) sono condivisi con la versione PHP e stanno in `../src/`.

```
elementor/
  urls.json              URL delle immagini caricate nella Libreria media (unico punto da aggiornare)
  build.py               genera dist/ sostituendo gli URL nei segnaposto {{chiave}}
  dist/                  ← file pronti da incollare (generati, non modificare a mano)
    aicfds.css
    widgets/01-hero.html … 10-footer-loghi.html, 99-script.html
    preview.html         anteprima locale con i CSS reali del sito (solo test)
```

## Come montare la pagina in Elementor

1. **Nuova pagina** con il layout predefinito del sito (sidebar a sinistra, header e footer del tema).
   Il titolo della pagina lo stampa già il tema come `<h1>`: per questo, nella versione Elementor, il titolo
   dell'hero è un `<h2>` (lo imposta `build.py`).
2. Inserire i widget nella **colonna principale del contenuto** del tema (nel sito è `#aic-main-content`, larga al
   massimo **822px**). Il contenitore deve essere **verticale** (Direction = Column) e a larghezza piena, con *Gap* = **0**:
   i widget vengono impilati e ognuno occupa tutta la larghezza. Un contenitore in riga o con larghezza "in base al
   contenuto" farebbe collassare il widget.
3. Dentro il container, **11 widget "HTML"** in quest'ordine, incollando il contenuto del file corrispondente
   di `dist/widgets/`:

   | # | File | Sezione |
   | --- | --- | --- |
   | 1 | `01-hero.html` | Hero con loghi |
   | 2 | `02-progetto.html` | Il progetto, obiettivi, numeri |
   | 3 | `03-indice-attivita.html` | Indice delle 4 attività |
   | 4 | `04-in-fuga-dal-glutine.html` | Progetto 01 |
   | 5 | `05-qa.html` | Progetto 02 |
   | 6 | `06-corsi-di-cucina.html` | Progetto 03 |
   | 7 | `07-dirette.html` | Progetto 04 |
   | 8 | `08-evento-finale.html` | Evento finale |
   | 9 | `09-associazioni.html` | Le 4 associazioni |
   | 10 | `10-footer-loghi.html` | Loghi e dicitura del bando |
   | 11 | `99-script.html` | Badge "Svolto / In programma" (va per ultimo) |

4. **Pagina → Impostazioni → Avanzate → CSS personalizzato** (Elementor Pro): incollare tutto
   `dist/aicfds.css`.
5. Meta description, titolo SEO e `noindex` (finché è in bozza) si impostano dal plugin SEO, non nell'HTML.

## Aggiornare i contenuti

- **Testi, date, link**: modificare il file in `../src/sections/`, poi `python build.py` e incollare di nuovo
  solo il widget cambiato. In alternativa si può modificare direttamente nel widget in Elementor.
- **Nuova immagine o logo**: caricarla nella Libreria media, aggiungere l'URL in `urls.json`, usare
  `{{nome-chiave}}` nel widget, rieseguire `python build.py`.
- **Stili**: `../src/css/aicfds.css`, poi `python build.py` e incollare `dist/aicfds.css` nel CSS della pagina.
- **Anteprima locale con gli stili reali del sito**: `python build.py --preview`, poi servire la cartella
  principale del repository (`python -m http.server`) e aprire `/elementor/dist/preview.html`.

## Note e attenzioni

- **Il layout segue la larghezza della colonna, non della finestra** (container query: `@container aicfds`). Con la
  sidebar del tema la colonna è al massimo 822px e si restringe da sola su tablet e smartphone; il CSS ha tre
  assetti: ≥ 640px (hero con loghi in orizzontale, pannelli su due colonne), < 640px (smartphone), < 300px.
- **Puntini del tema**: il tema aggiunge un puntino a ogni `<li>` in `#aic-main-content` (regola con ID). Il CSS lo
  azzera (`content: none !important`); non rimuovere quelle righe.
- **Prefisso `aicfds-`** su tutte le classi e contenitore `.aicfds` in ogni widget: servono a isolare gli stili
  da quelli del tema `AIC-territoriale-master` e di Elementor. Non rimuoverli.
- **Link ai menu del sito**: le sezioni hanno gli id `progetto`, `progetti`, `in-fuga-dal-glutine`, `qa`,
  `corsi-cucina`, `dirette`, `associazioni`, quindi nel menu del sito si può puntare a `/slug-pagina/#progetti`.
- **Header sticky del sito**: se coprisse l'inizio delle sezioni dopo un clic su un'ancora, regolare
  `scroll-padding-top` (ora 90px) in cima a `aicfds.css`.
- **SVG**: i loghi sono SVG e richiedono l'upload SVG abilitato (già fatto, gli URL rispondono).
- **WP Rocket**: se il badge "Svolto / In programma" non compare, escludere lo script dal ritardo/minificazione
  del JavaScript. Senza JavaScript la pagina è comunque completa.
- **Contenuti provvisori**: le etichette gialle "da confermare" (`aicfds-tbc`) vanno rimosse a contenuti definitivi.
- **Immagine del calendario**: è il PNG originale (1,2 MB). Se la pagina risulta pesante conviene
  ricaricarlo come WebP (124 KB, disponibile in `docs/assets/img/`) e aggiornare l'URL in `urls.json`.
