---
title: "Formazione Digitale — Architettura del Progetto"
author: "Cristiano De Pasquale"
date: "Maggio 2026"
geometry: "margin=2.5cm"
fontsize: 11pt
toc: true
toc-depth: 3
numbersections: true
colorlinks: true
linkcolor: "blue"
---

\newpage

# Panoramica del progetto

**Formazione Digitale** è un portale statico di alfabetizzazione digitale che eroga guide pratiche, strumenti interattivi e pillole di contenuto. Le risorse sono libere, gratuite e senza prerequisiti. Il portale è usato come riferimento didattico per studenti e docenti — portale di riferimento scolastico istituzionale (IIS Einaudi Chiari, BS).

| Campo | Valore |
|---|---|
| URL live | https://formazione-digitale.it |
| Repository | github.com/formazione-digitale/formazione-digitale.github.io |
| Visibilità repo | Pubblica |
| Deploy | Vercel Edge Network — pubblicazione automatica da branch main |
| Dominio | formazione-digitale.it — registrato su Aruba, maggio 2026 |
| Stack | HTML puro + CSS + JS vanilla — zero framework, zero build step |
| Autore | Cristiano De Pasquale — Docente di Informatica, IIS Einaudi Chiari (BS) |
| Licenza | Uso libero e non commerciale |

---

# Struttura del repository

La root contiene i file di configurazione e i JS condivisi. Ogni risorsa vive nella propria cartella autonoma.

```
formazione-digitale/
|--- index.html
|--- mappa.html
|--- mappa-framework.html
|--- 404.html
|--- privacy-policy.html
|--- cookie-policy.html
|--- manifest.json                   ← Catalogo risorse — unica fonte di verità
|--- site.webmanifest
|--- robots.txt
|--- sitemap.xml
|--- sw.js
|--- stats.js
|--- supabase.js
|--- auth.js
|--- .gitignore
|--- css/shared.css
|--- img/
|--- docs/
|--- scripts/
|   |--- genera_sitemap.py
|   |--- aggiorna_dominio.py
|   |--- aggiungi_footer_index.py
|   |--- aggiungi_link_footer.py
|   |--- replace_in_files.py
|   |--- inject_after.py
|   |--- icdl_to_json.py             ← Anonimizza export Excel ICDL → JSON per dashboard
|   |--- zip_risorse.py              ← Genera ZIP contesto per IA (esclude binari e .git)
|   \--- struttura.bat
|--- sicurezza/
|   |--- pillola-cybersicurezza/
|   \--- guida-cybersicurezza/
|--- competenze-digitali/
|   |--- pillola-wikipedia-speedrun/
|   |--- pillola-valutazione-fonti/
|   |--- pillola-aggiornamento-digitale/
|   |--- strumento-valutazione-fonti/
|   \--- strumento-autovalutazione-digcompedu/
|--- intelligenza-artificiale/
|   |--- guida-prompting/
|   |--- guida-peer-review-ia/
|   \--- prompt-builder/
|--- elaborazione-testi/
|   \--- guida-word/
|--- database/
|   \--- guida-libreoffice-base-query/   ← Pattern CSS proprietario — NON collegare a shared.css
|--- marketing/
|   |--- guida-marketing/
|   |--- pillola-seo/
|   |--- analizzatore-seo/
|   \--- break-even-point-tool/
|--- networking/
|   |--- subnet-calculator/
|   \--- hfs-server/
|--- sistemi/
|   \--- codifica-binaria/
\--- icdl/                               ← Pagine istituzionali — noindex, active:false
    |--- index.html
    \--- statistiche/
            index.html
```

---

# Architettura CSS

## shared.css

File CSS condiviso caricato da tutte le pagine tramite path assoluto.

Contiene:

- Reset universale
- Variabili `:root` — palette colori, font, token di layout
- Header con back-link, separatore, logo, sottotitolo
- Sidebar e overlay (hamburger menu)
- Layout `#main` con responsività
- Struttura sezioni guide (`section-header`, `cover-block`)
- Box callout: `.box-tip`, `.box-warn`, `.box-note`, `.box-info`, `.box-red`
- Footer — stile base per tag `<footer>` semantico
- Auth UI: bottone login, modal accesso, modal profilo, bottone segnalibro
- GUIDE LAYOUT — `.guide-header`, hamburger, layout griglia
- `.header-downloads` — barra download file allegati (desktop: inline header; mobile <600px: barra fissa sotto header)
- `.mode-toggle` — nascosto su mobile (<600px) perché non utile
- `.nav-menu-btn` + `.nav-dropdown` — hamburger a tendina per pagine con nav custom (subnet-calculator, hfs-server)
- Responsive mobile < 640px per sottopagine standard
- Dark mode — variabili e override componenti (pianificato)

```html
<link rel="stylesheet" href="/css/shared.css?v=N">
```

> **Nota:** incrementare `?v=N` ad ogni modifica significativa per invalidare la cache. Versione attuale: `?v=2` per subnet-calculator e hfs-server (aggiornati 13/05/2026).

## Pattern header-downloads (nuovo — 11/05/2026)

Per pagine con file allegati scaricabili, usare `.header-downloads` come wrapper dei `.btn-download` dentro `header-right`. Su desktop appaiono nell'header. Su mobile (<600px) diventano una barra fissa sotto l'header, scrollabile orizzontalmente. Usare `body.aula-mode` per nasconderli in modalità presentazione.

```html
<div class="header-right">
  <div class="header-downloads">
    <a class="btn-download" href="file.pptx" download>...</a>
  </div>
  <button class="mode-toggle">...</button>
</div>
```

## Pattern nav-dropdown (nuovo — 13/05/2026)

Per pagine con `<nav>` custom (non `.guide-header`) che necessitano di menu mobile. Usato da `subnet-calculator` e `hfs-server`.

```html
<!-- Bottone hamburger nella nav -->
<button class="nav-menu-btn" id="nav-menu-btn" onclick="toggleNavMenu()" aria-label="Menu">
  <span></span><span></span><span></span>
</button>

<!-- Dropdown sotto la nav -->
<div class="nav-dropdown" id="nav-dropdown">
  <div class="nav-dropdown-label">Sezioni</div>
  <a href="#sezione1" onclick="closeNavMenu()">Testo sezione</a>
  <div class="nav-dropdown-divider"></div>
  <div class="nav-dropdown-label">Download</div>
  <a href="file.zip" download onclick="closeNavMenu()">↓ File</a>
</div>
```

JS richiesto inline nella pagina: `toggleNavMenu()`, `closeNavMenu()`, listener click esterno.

## CSS specifico per pagina

Ogni pagina mantiene un proprio `<style>` inline per componenti non condivisi.

> **NOTA:** `database/guida-libreoffice-base-query` e le future guide LibreOffice usano un sistema CSS proprietario — palette dedicata, ~50 variabili custom. **Non collegare a shared.css.** Questo sarà il pattern base per tutte le guide LibreOffice future (1-2 in arrivo). Decidere poi se creare un secondo shared dedicato.

---

# JavaScript — file e responsabilità

| File | Responsabilità |
|---|---|
| `sw.js` | Service Worker PWA. Cache First per CSS/img, Network First per HTML/JSON. `CACHE_VERSION` da incrementare ad ogni deploy significativo. |
| `stats.js` | Carica statistiche da GoatCounter API. Inietta Schema.org ItemList dinamico da `manifest.json`. Non modificare per aggiungere risorse — aggiornare solo `manifest.json`. |
| `supabase.js` | Client Supabase condiviso. Esporta `supabase` per import ES module. **ATTENZIONE:** contiene anon key — pianificata migrazione a variabile d'ambiente Vercel (settembre 2026). |
| `auth.js` | Gestisce login magic link, logout, stato sessione, segnalibri. Importa `supabase.js`. |
| `scripts/ui.js` | Inietta back-to-top button in tutte le pagine. Gestisce localStorage tema. Includere con `<script src="/scripts/ui.js" defer></script>` prima di `</body>` in ogni pagina HTML. |
| `scripts/icdl_to_json.py` | Anonimizza export Excel ICDL → JSON per la dashboard statistiche. |
| `scripts/zip_risorse.py` | Genera ZIP del progetto escludendo binari, immagini e `.git`. Output nella root con timestamp. Usare per passare contesto alle IA. |

> **Regola ui.js:** ogni file HTML del portale deve includere `<script src="/scripts/ui.js" defer></script>`. Per verificare le pagine senza ui.js: `ls -r *.html | ?{ !(sls "ui.js" $_.FullName -Quiet) } | % FullName` (PowerShell dalla root).

---

# manifest.json — catalogo risorse

File JSON unica fonte di verità per tutte le risorse del portale. I campi framework DigComp e DigCompEdu sono integrati direttamente in questo file — `manifest_digcomp.json` è stato eliminato (maggio 2026).

| Campo | Descrizione |
|---|---|
| `path` | Path assoluto della risorsa |
| `label` | Titolo completo |
| `short` | Titolo breve per statistiche e mappa |
| `cat` | Categoria: `guide` / `strumento` / `pillola` |
| `emoji` | Emoji identificativa |
| `tags` | Array di keyword per la ricerca interna |
| `meta` | Testo secondario nella card |
| `description` | Descrizione breve usata da Schema.org ItemList |
| `featured` | Boolean — card in evidenza (max 1 per sezione) |
| `active` | Boolean — `false` esclude la risorsa da stats, mappa e schema |
| `digcomp` | Array competenze DigComp (es. `["DC 4.1", "DC 4.2"]`) |
| `digcomp_level` | Livello DigComp: `foundation` / `intermediate` / `advanced` |
| `digcompedu` | Array competenze DigCompEdu (es. `["DCEdu 6.4"]`) |
| `digcomp_areas` | Array aree tematiche DigComp |

Consumato da: `stats.js` (GoatCounter + Schema.org), `mappa.html` (grafo), `mappa-framework.html` (navigazione per competenza), `sitemap.xml` tramite `genera_sitemap.py`.

> **Regola:** quando aggiungi una risorsa, aggiorna **manifest.json** + **index.html** (card) + aggiorna `stats.js` (`gcPagine`) + rilancia `genera_sitemap.py`.

> **Pagine istituzionali invisibili:** `/icdl/` e `/icdl/statistiche/` hanno `"active": false` — escluse da mappa, statistiche e Schema.org. Meta robots impostato a `noindex, nofollow`. Accessibili solo via path diretto.

---

# Integrazioni esterne

## Vercel (hosting principale)

| Campo | Valore |
|---|---|
| Scopo | Hosting statico + Serverless Functions + Preview Deployments |
| Piano | Hobby (gratuito) |
| URL produzione | https://formazione-digitale.it |
| Deploy | Automatico da push su branch main GitHub |
| Preview | Ogni branch genera URL preview univoco |
| Configurazione domini | formazione-digitale.it → Production · www → 301 redirect a non-www |

> **NOTA:** Non esiste `vercel.json` nel progetto. I redirect www→non-www sono configurati direttamente nel dashboard Vercel (Settings → Domains). HTTP→HTTPS gestito automaticamente da Vercel.

## Aruba (registrar dominio)

| Campo | Valore |
|---|---|
| Dominio | formazione-digitale.it |
| Registrato | Maggio 2026 |
| Scadenza | Maggio 2027 |
| Rinnovo automatico | Attivo |
| Email attiva | info@formazione-digitale.it |
| DNS | Record A: `@` → 216.198.79.1 · CNAME: `www` → Vercel |

## Supabase

| Campo | Valore |
|---|---|
| Scopo | Database PostgreSQL + Auth + API REST |
| Piano | Free (pausa dopo 7gg inattività) |
| Auth attiva | Magic link (OTP via email) |
| Auth in arrivo | OAuth Google |
| Tabelle | `profiles` · `bookmarks` |
| RLS | Attiva — ogni utente vede solo i propri dati |
| Keep-alive | GitHub Actions (`supabase-keep-alive.yml`) — ogni giorno alle 08:00 UTC |
| **Sicurezza** | **ATTENZIONE:** anon key in `supabase.js` (file pubblico). Migrazione a Vercel env variables — settembre 2026. |

## Resend (email transazionale)

| Campo | Valore |
|---|---|
| Scopo | SMTP per magic link Supabase |
| Piano | Free (3.000 email/mese) |
| Mittente attuale | onboarding@resend.dev (temporaneo — email in spam) |
| Mittente futuro | info@formazione-digitale.it (dominio da verificare) |

## GoatCounter (analytics)

| Campo | Valore |
|---|---|
| Scopo | Analytics privacy-friendly, senza cookie, GDPR compliant |
| Account | formazionedigitale.goatcounter.com |
| Integrazione | Script asincrono in `<head>` di ogni pagina |
| API | Usata da `stats.js` per pageview e top 3 pagine |

## Google Search Console

| Campo | Valore |
|---|---|
| Proprietà attiva | formazione-digitale.it |
| Cambio indirizzo | Completato il 09/05/2026: github.io → formazione-digitale.it |
| Sitemap inviata | https://formazione-digitale.it/sitemap.xml |
| Stato indicizzazione | In corso — crawl completo atteso entro 2-6 settimane |

## Google Fonts

| Campo | Valore |
|---|---|
| Font usati | DM Serif Display (titoli) · DM Sans (corpo testo) |
| Caricamento | Da `shared.css` |
| Note | Principale causa del LCP mobile (4.8s). `font-display: swap` non ancora implementato. |

---

# GDPR e Privacy

| Documento | URL | Note |
|---|---|---|
| Privacy Policy | `/privacy-policy.html` | Copre GoatCounter, Formspree, Google Fonts, Vercel |
| Cookie Policy | `/cookie-policy.html` | Nessun cookie di profilazione — banner non necessario |

Il sito non utilizza cookie di profilazione. GoatCounter è privacy-first e non richiede consenso. Quando sarà attiva l'autenticazione Supabase, sarà necessario aggiornare entrambi i documenti e aggiungere il banner cookie per i cookie di sessione.

---

# Progressive Web App (PWA)

| Componente | Dettaglio |
|---|---|
| `site.webmanifest` | Nome, icone, colori, display standalone, lingua it |
| `sw.js` | Cache First per assets, Network First per HTML/JSON |
| `CACHE_VERSION` | Da incrementare ad ogni deploy significativo |
| Offline | Pagine già visitate disponibili offline. Fallback alla homepage. |

---

# SEO

| Metrica | Valore |
|---|---|
| PageSpeed SEO (desktop) | 100 / 100 |
| PageSpeed Prestazioni (desktop) | 99 / 100 |
| PageSpeed Accessibilità | 94 / 100 |
| PageSpeed Best Practice | 96 / 100 |
| PageSpeed Prestazioni (mobile) | 79 / 100 — LCP 4.8s (Google Fonts) |

**Elementi SEO implementati:**

- Title tag, meta description, canonical, robots, author in ogni pagina
- Open Graph completo + Twitter/X Card
- Schema.org WebSite con SearchAction in `index.html`
- Schema.org ItemList dinamico — generato da `stats.js` via `manifest.json`
- Schema.org LearningResource nelle sottopagine guide
- `sitemap.xml` inviata a GSC
- `lang="it"` su tutti gli HTML
- `<h1>` semantico in ogni pagina (incluse pagine con layout canvas: H1 nascosto via CSS)

---

# Debito CSS — da affrontare prima del dark mode

- Variabili colori semantici ricorrenti (`#4caf80`, `#c0392b`, `#f39c12`) da variabilizzare come `--green-success`, `--red-error` in `shared.css`
- `marketing/analizzatore-seo` — 49 proprietà hardcoded con palette Google Search Console (by design, ma da isolare)
- `strumento-autovalutazione-digcompedu` — salta da H1 a H3, nessun H2 (struttura heading rotta)

---

# Broken links — run 11/05/2026

Usare `blc https://formazione-digitale.it -ro | findstr "BROKEN"` per il check settimanale.

## Link risolti — 13/05/2026

Tutti i broken link interni ed esterni rilevati al 11/05/2026 sono stati corretti.

## Falsi positivi (lasciare così)

- `platform.openai.com` — HTTP 403, sito blocca crawler
- `mediabiasfactcheck.com` — BLC_UNKNOWN, sito blocca crawler
- `weverify.eu` — BLC_UNKNOWN, sito blocca crawler
- `datareportal.com` — BLC_UNKNOWN, sito blocca crawler
- `support.google.com/chrome/answer/95647` — HTTP 404 da crawler, pagina funzionante
- `education.ec.europa.eu/selfie-for-teachers` — BLC_UNKNOWN, sito EU funzionante

---

# Script di manutenzione locale

| Script | Funzione |
|---|---|
| `genera_sitemap.py` | Genera `sitemap.xml` da `manifest.json`. Lanciare dopo ogni nuova risorsa. |
| `aggiorna_dominio.py` | Sostituisce un dominio in tutti i file HTML e XML. |
| `aggiungi_footer_index.py` | Aggiunge `<footer>` con link legali ai file della root. |
| `aggiungi_link_footer.py` | Aggiunge link Privacy/Cookie ai footer di tutte le sottocartelle. |
| `replace_in_files.py` | Trova e sostituisce una stringa in tutti gli HTML. |
| `inject_after.py` | Inietta una stringa dopo un'occorrenza in tutti gli HTML. Idempotente. |
| `icdl_to_json.py` | Anonimizza export Excel ICDL → JSON per la dashboard statistiche. |
| `struttura.bat` | Genera `struttura.txt` con albero cartelle. |
| `zip_risorse.py` | Genera ZIP del progetto (~374KB) escludendo binari, immagini, `.git`. Output nella root con timestamp. Configurabile via `BLACKLIST_ESTENSIONI` e `BLACKLIST_CARTELLE`. Usare con `--dry-run` per anteprima. |

---

# Responsive Mobile — sessione 08/05/2026

## Workflow branch e preview Vercel

1. Creare branch dedicato in GitHub Desktop
2. Pubblicare il branch — Vercel genera automaticamente un preview URL
3. Testare il preview URL da mobile prima del merge
4. Merge su main → deploy automatico su formazione-digitale.it

Usare main direttamente solo per modifiche piccole e sicure.

## Migrazione .guide-header in shared.css

Il CSS di `.guide-header`, hamburger, sidebar e layout griglia era duplicato inline in ogni sottopagina standard. Migrato in `shared.css` come blocco condiviso.

## Bug mobile risolti

| Bug | Data | Stato |
|---|---|---|
| Guida Marketing — bottoni download non funzionanti su mobile | 11/05/2026 | RISOLTO — pattern `.header-downloads` |
| Guida Marketing — mode-toggle visibile su mobile (inutile) | 11/05/2026 | RISOLTO — nascosto via media query |
| LibreOffice Base Query — navbar sparisce + manca back-to-top | 11/05/2026 | RISOLTO |
| Subnet Calculator — hamburger mancante, sidebar non accessibile su mobile | 13/05/2026 | RISOLTO — pattern `.nav-menu-btn` + `.nav-dropdown` in `shared.css` |
| HFS Server — nessun menu di navigazione mobile | 13/05/2026 | RISOLTO — pattern `.nav-menu-btn` + `.nav-dropdown` in `shared.css` |

---

# Dark Mode — Analisi Architetturale

Analisi prodotta in maggio 2026. Implementazione non ancora avviata.

## Valutazione

Il dark mode è raccomandato. Il costo reale non è tecnico — è di manutenzione CSS: ogni nuovo componente deve prevedere la variante dark. Tutto centralizzato in `shared.css`, nessuna modifica ai singoli file delle guide.

## Prerequisiti prima dell'implementazione

1. Variabilizzare colori semantici ricorrenti (`--green-success`, `--red-error`, ecc.) in `shared.css`
2. Risolvere i colori hardcoded nei Tier 2

## Classificazione pagine (Tier)

| Tier | Pagine | Strategia |
|---|---|---|
| **Tier 1 — Risposta automatica** | index.html, mappa.html, guide IA, Subnet, BEP | Variabili dark in `shared.css` |
| **Tier 2 — Intervento mirato** | guida-marketing, hfs-server, codifica-binaria | Revisione colori hardcoded inline |
| **Tier 3 — Valutare caso per caso** | guida-libreoffice-base-query, guida-word | Escludere con `data-theme-lock="true"` |

## Pattern scelto

`prefers-color-scheme` (sistema) + attributo manuale `data-theme` su `<html>` + `localStorage`.

1. Default → rispetta la preferenza del sistema operativo
2. Toggle manuale → aggiunge `data-theme="dark"|"light"` su `<html>`
3. Persistenza → `localStorage` (chiave: `fd-theme`)
4. Anti-flash → script sincrono in `<head>` prima di qualsiasi CSS

## Stima lavoro

| Attività | Tempo stimato |
|---|---|
| Variabili dark in `shared.css` + override componenti | 1–2 ore |
| `ui.js` + bottone header index e mappa | 30 min |
| Anti-flash in tutte le pagine (`replace_in_files.py`) | 15 min |
| Test Tier 1 | 1–2 ore |
| Revisione Tier 2 | 2–4 ore |
| Decisione e lock Tier 3 | 30 min |

---

# Architettura CSS LibreOffice — shared-libreoffice.css

## Decisione (11/05/2026)

Le guide LibreOffice (attuale: `guida-libreoffice-base-query`, in arrivo: 1-2 guide aggiuntive) usano un sistema CSS proprietario con palette scura e toni caldi, completamente diversa da `shared.css`. Il pattern scelto è un **import a cascata**:

```html
<link rel="stylesheet" href="/css/shared.css">
<link rel="stylesheet" href="/css/shared-libreoffice.css">
```

## Cosa eredita da shared.css

- Reset universale
- Footer semantico
- Auth UI (login modal, segnalibri)
- Box callout (`.box-tip`, `.box-warn`, ecc.)
- Sidebar e overlay
- Back-to-top (`ui.js`)
- Dark mode override (quando implementato)

## Cosa sovrascrive shared-libreoffice.css

- Variabili `:root` — palette (sfondo scuro, toni caldi, accent LibreOffice)
- Header — colore e identità visiva
- Font se diverso dal sistema
- Componenti specifici del DB (tabelle query, syntax highlight SQL)

## Beneficio

Quando `shared.css` si aggiorna (dark mode, auth UI, back-to-top), le guide LibreOffice si aggiornano automaticamente senza interventi manuali.

> **PROSSIMO PASSO:** prima della seconda guida LibreOffice, estrarre il CSS proprietario da `guida-libreoffice-base-query/index.html` in `/css/shared-libreoffice.css` e collegare entrambi i file.

---

# Roadmap

## Completato

- [OK] Migrazione Vercel (maggio 2026)
- [OK] Dominio formazione-digitale.it registrato su Aruba
- [OK] GSC cambio indirizzo completato (09/05/2026): github.io → formazione-digitale.it
- [OK] Sessione responsive mobile (08/05/2026)
- [OK] Pillola Valutazione Fonti + Strumento Verifica Fonti (maggio 2026)
- [OK] Unificazione manifest.json — eliminato manifest_digcomp.json (maggio 2026)
- [OK] Pattern `.header-downloads` per file allegati (11/05/2026)
- [OK] `.gitignore` creato (11/05/2026)
- [OK] `zip_risorse.py` — tool contesto per IA (11/05/2026)
- [OK] Redirect www→non-www configurato su Vercel dashboard (11/05/2026)
- [OK] Guida ICDL + Dashboard statistiche ICDL — aggiunte al portale (maggio 2026)
- [OK] Script `icdl_to_json.py` per anonimizzazione export Excel ICDL (maggio 2026)
- [OK] Audit SEO completo (13/05/2026): `<br>` in H1 (4 file), `cover-title` → `<h1>` (5 file), `404.html` meta/OG, `mappa.html` footer + H1, `strumento-valutazione-fonti` footer + H1 + `ui.js`, `mappa-framework.html` `ui.js`
- [OK] Broken links risolti — tutti i link interni ed esterni (13/05/2026)
- [OK] Hamburger mobile Subnet Calculator e HFS Server — pattern `.nav-menu-btn` + `.nav-dropdown` in `shared.css` (13/05/2026)
- [OK] `mappa.html` — footer visibile fisso in basso, H1 nascosto per SEO (13/05/2026)
- [OK] Pagine ICDL — `noindex, nofollow` + `active: false` in manifest (invisibili, solo accesso diretto) (13/05/2026)
- [OK] `mappa.html` — doppio `ui.js` fuori da `</body>` corretto (13/05/2026)

## Miglioramenti strutturali — luglio/agosto 2026

- `role="heading" aria-level="1"` sui `cover-title` con `replace_in_files.py` (passata unica su tutto il portale — risolve futuri audit automatici)
- Variabilizzare colori semantici ricorrenti in `shared.css`: `--color-success`, `--color-error`, `--color-warning` — prerequisito pulito per dark mode
- Creare `shared-libreoffice.css` prima della seconda guida LibreOffice
- `font-display: swap` per migliorare LCP mobile (attuale 4.8s)
- Conversione PNG → WebP
- Migrazione JS in `/js/`

## Bassa urgenza — quando disponibile

- Disabilitazione GitHub Pages (dopo settembre 2026 — branch redirect necessario fino ad allora)
- Nuovi contenuti: Pillola PageSpeed · Pillola Triade CIA

## Prima di aprire l'auth agli utenti reali

Completare **in questo ordine**:

1. Aggiornare Redirect URL Supabase → formazione-digitale.it
2. Configurare dominio verificato su Resend (email magic link in spam)
3. Login Google OAuth
4. Aggiornare Privacy Policy con sezione autenticazione + cookie sessione
5. Aggiungere banner cookie
6. Auth in tutte le sottopagine
7. Segnalibri sulle card
8. Checklist persistenti via Supabase

## Nuovi contenuti — priorità DigComp/INDIRE

| Priorità | Risorsa | Standard attivati |
|---|---|---|
| [!] 1 | Pillola netiquette / cittadinanza digitale | DC 2.2–2.4 · DCEdu 6.4 · INDIRE A4 |
| [~] 2 | Guida/strumento collaborazione scolastica | INDIRE B1·B2 · DCEdu 1.2·2.3 |
| [?] 3 | Risorsa valutazione digitale (rubric builder) | DCEdu 4.1·4.2·4.3 · INDIRE A3 |

## Settembre 2026 — badge DigComp (ordine obbligatorio)

> **ATTENZIONE:** eseguire tassativamente in questo ordine. La protezione del token Supabase è prerequisito per tutto il resto.

1. Migrazione Vercel come unico hosting (GitHub Pages dismesso)
2. Configurazione variabili d'ambiente Vercel (`SUPABASE_URL`, `SUPABASE_KEY`)
3. Creazione Serverless Function `/api/competenze.js` (proxy sicuro Supabase)
4. Creazione tabella Supabase `risorse_competenze` (`slug`, `digcomp[]`, `digcompedu[]`, `indire[]`)
5. Sviluppo `competenze.js` client — chiama `/api/` non Supabase direttamente
6. Badge competenze nelle card-footer
7. Profilo competenze utente
8. Vercel Cron Job keep-alive (sostituisce GitHub Actions)
