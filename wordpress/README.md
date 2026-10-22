# Versione WordPress: template di pagina in PHP (plugin)

La landing page come **modello di pagina WordPress** scritto in PHP. Usa `get_header()` e `get_footer()`,
quindi mostra **l'header e il footer del sito** (nel tema `AIC-territoriale-master` sono i modelli di
Elementor Pro / Theme Builder) e, in mezzo, le sezioni del progetto.

Il modello è consegnato come **plugin**: non si modifica il tema condiviso (che un aggiornamento
sovrascriverebbe) e basta attivarlo per avere il modello «Progetto Fondazione di Sardegna» tra quelli delle pagine.

```
wordpress/
  build.py                      genera dist/ a partire da ../src
  plugin/                       parte fissa del plugin (modificabile)
    aicfds-landing.php            registra il modello, carica CSS e JS solo sulla pagina
    templates/page-progetto-fondazione.php   get_header() + sezioni + get_footer()
  dist/                         ← generato
    aicfds-landing/               cartella del plugin completa
    aicfds-landing.zip            da caricare in WordPress
```

Contenuti, CSS e JS sono gli stessi della versione Elementor e vengono dai sorgenti comuni in `../src/`
(`sections/*.html`, `css/aicfds.css`, `js/aicfds.js`): `build.py` li trasforma in `template-parts/*.php` e
copia nel plugin anche loghi e immagini, senza passare dalla Libreria media.

## Installazione

1. `python build.py` (solo se hai modificato qualcosa; `dist/aicfds-landing.zip` è già pronto).
2. WordPress → **Plugin → Aggiungi nuovo → Carica plugin** → scegliere `aicfds-landing.zip` → **Attiva**.
   In alternativa copiare la cartella `dist/aicfds-landing/` in `assets/plugins/` (nel sito la cartella
   `wp-content` si chiama `assets`).
3. **Pagine → Aggiungi nuova**, titolo ad es. «Progetto Fondazione di Sardegna», slug a piacere.
   Nel riquadro **Attributi pagina → Modello** scegliere **Progetto Fondazione di Sardegna**.
   L'editor può restare vuoto: il contenuto non viene usato.
4. Salvare come **bozza**, aprire l'anteprima, controllare, poi pubblicare.
5. Svuotare la cache (WP Rocket) dopo ogni aggiornamento del plugin.

Per titolo SEO, meta description e `noindex` (finché è in bozza) usare il plugin SEO del sito.

## Cose da controllare alla prima installazione

- **Elementor Pro / Theme Builder.** Il sito ha un modello «Single» (id 74) che può applicarsi a tutte le pagine.
  Il plugin carica il proprio template con priorità alta, quindi dovrebbe prevalere. Se la pagina mostrasse
  comunque il modello Single di Elementor, escludere questa pagina dalle sue condizioni
  (Elementor → Theme Builder → Single → Condizioni).
- **Header sticky.** Se l'header del sito è fisso e copre l'inizio delle sezioni quando si clicca un'ancora,
  regolare `scroll-padding-top` (ora 90px) in cima a `src/css/aicfds.css`.
- **WP Rocket.** Se i badge «Svolto / In programma» non compaiono, escludere `aicfds.js` dal ritardo/minificazione
  del JavaScript. Senza JavaScript la pagina è comunque completa.
- **Link nel menu del sito**: le sezioni hanno gli id `progetto`, `progetti`, `in-fuga-dal-glutine`, `qa`,
  `corsi-cucina`, `dirette`, `associazioni` → `/slug-pagina/#progetti`.

## Aggiornare i contenuti

Modificare i file in `../src/sections/` (testi, date, link), poi `python build.py` e ricaricare lo ZIP
(WordPress chiede di sostituire il plugin esistente) oppure sovrascrivere i file in `assets/plugins/aicfds-landing/`.
Lo stesso `build.py` della cartella `../elementor/` aggiorna la versione a widget HTML.

## Come è stato provato

PHP lintato (`php -l`) e template eseguito con un simulatore minimo delle funzioni di WordPress, usando
header e footer reali di sardegna.celiachia.it e i suoi CSS: il modello viene risolto, CSS/JS vengono accodati e
la pagina si incastra tra header e footer. **Non è stato provato su un'installazione WordPress vera**: il primo
test va fatto su una pagina in bozza.
