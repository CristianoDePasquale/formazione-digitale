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

**Formazione Digitale** è un portale statico di alfabetizzazione digitale che eroga guide pratiche, strumenti interattivi e pillole di contenuto. Le risorse sono libere, gratuite e senza prerequisiti.

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
|--- 404.html
|--- privacy-policy.html
|--- cookie-policy.html
|--- manifest.json           ← Catalogo risorse (fonte di verità)
|--- manifest_digcomp.json   ← Catalogo con campi DigComp/DigCompEdu
|--- site.webmanifest
|--- robots.txt
|--- sitemap.xml
|--- vercel.json
|--- sw.js
|--- stats.js
|--- supabase.js
|--- auth.js
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
|   \--- struttura.bat
|--- sicurezza/
|   |--- pillola-cybersicurezza/
|   \--- guida-cybersicurezza/
|--- competenze-digitali/
|   |--- pillola-wikipedia-speedrun/
|   |--- pillola-valutazione-fonti/
|   \--- strumento-valutazione-fonti/
|--- intelligenza-artificiale/
|--- elaborazione-testi/
|--- database/
|--- marketing/
|--- networking/
\--- sistemi/
```

---

# Architettura CSS

## shared.css

File CSS condiviso caricato da tutte le pagine tramite path assoluto. Contiene:

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
- Responsive mobile < 640px per sottopagine standard
- Dark mode — variabili e override componenti (pianificato)

```html
<link rel="stylesheet" href="/css/shared.css?v=N">
```

> **Nota:** incrementare `?v=N` ad ogni modifica significativa per invalidare la cache.

## CSS specifico per pagina

Ogni pagina mantiene un proprio `<style>` inline per componenti non condivisi. Le pagine con design system proprietario (LibreOffice Base, Word) non usano `shared.css`.

---

# JavaScript — file e responsabilità

| File | Responsabilità |
|---|---|
| `sw.js` | Service Worker PWA. Cache First per CSS/img, Network First per HTML/JSON. `CACHE_VERSION` da incrementare ad ogni deploy significativo. |
| `stats.js` | Carica statistiche da GoatCounter API. Inietta Schema.org ItemList dinamico da `manifest.json`. Non modificare per aggiungere risorse — aggiornare solo `manifest.json`. |
| `supabase.js` | Client Supabase condiviso. Esporta `supabase` per import ES module. **ATTENZIONE:** contiene anon key — pianificata migrazione a variabile d'ambiente Vercel (settembre 2026). |
| `auth.js` | Gestisce login magic link, logout, stato sessione, segnalibri. Importa `supabase.js`. |
| `scripts/ui.js` | Gestisce `initThemeToggle()`, localStorage tema, sincronizzazione sistema operativo. |

---

# manifest.json — catalogo risorse

File JSON fonte di verità per tutte le risorse del portale.

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
| `active` | Boolean — `false` esclude dalla risorsa da stats e schema |
| `digcomp` | Array competenze DigComp (es. `["DC 4.1", "DC 4.2"]`) |
| `digcomp_level` | Livello DigComp: `foundation` / `intermediate` / `advanced` |
| `digcompedu` | Array competenze DigCompEdu (es. `["DCEdu 6.4"]`) |
| `digcomp_areas` | Array aree tematiche DigComp |

Consumato da: `stats.js` (GoatCounter + Schema.org), `mappa.html` (grafo), `sitemap.xml` tramite `genera_sitemap.py`.

> **Regola:** quando aggiungi una risorsa, aggiorna **manifest.json** + **manifest_digcomp.json** + **index.html** (card) + rilancia `genera_sitemap.py`.

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
| Configurazione | `vercel.json` — redirect 301, header di sicurezza |
| Serverless Functions | Pianificate per settembre 2026 (proxy Supabase sicuro) |

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
| Keep-alive | GitHub Actions (`supabase-keep-alive.yml`) |
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
| Proprietà precedente | formazione-digitale.github.io (cambio indirizzo pendente) |
| Sitemap inviata | https://www.formazione-digitale.it/sitemap.xml |

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
| `struttura.bat` | Genera `struttura.txt` con albero cartelle. |

---

# Workflow — aggiungere una nuova risorsa

1. Crea la cartella: `/categoria/nome-risorsa/`
2. Crea `index.html` con link a `shared.css` e CSS specifico inline
3. Aggiungi la voce a `manifest.json` con tutti i campi inclusi `digcomp`/`digcompedu`
4. Aggiungi la stessa voce a `manifest_digcomp.json`
5. Aggiungi la card in `index.html` nella sezione corretta
6. Lancia `scripts/genera_sitemap.py` per aggiornare `sitemap.xml`
7. Push su GitHub — Vercel pubblica in 1-2 minuti automaticamente
8. Verifica: card visibile, filtro funzionante, ricerca per tag, link corretto

---

# Copertura DigComp / DigCompEdu / INDIRE

## DigComp 2.2 — copertura attuale

| Area | Competenze coperte | Risorse principali |
|---|---|---|
| **1 — Informazione** | DC 1.1, DC 1.2 | Wikipedia Speedrun, Pillola Valutazione Fonti, Strumento Verifica Fonti |
| **2 — Comunicazione** | DC 2.1, DC 2.6 | Wikipedia Speedrun, Cybersicurezza |
| **3 — Creazione** | DC 3.1, DC 3.2 | Word, Prompting, Peer-review IA |
| **4 — Sicurezza** | DC 4.1, DC 4.2 | Pillola/Guida Cybersicurezza |
| **5 — Problem solving** | DC 5.1, DC 5.2 | LibreOffice Base, BEP Tool, Subnet Calculator |

**Area 1 — Informazione** è la più coperta del portale, con tre risorse dedicate a navigazione e valutazione critica.

**Gap:** DC 2.2 (condivisione), DC 2.3 (collaborazione), DC 2.4 (netiquette) non ancora coperti.

## DigCompEdu — copertura attuale

| Area | Competenze attivate | Note |
|---|---|---|
| **1 — Coinvolgimento professionale** | 1.4 | Prompting IA |
| **2 — Risorse digitali** | 2.2, 2.3 | Più guide |
| **3 — Pratiche di insegnamento** | 3.1, 3.2 | Strumenti interattivi, pillole |
| **4 — Valutazione** | 4.1 | BEP Tool, Strumento Verifica Fonti |
| **5 — Valorizzazione studenti** | 5.3 | Gamification Wikipedia |
| **6 — Competenze digitali studenti** | 6.1, 6.2, 6.3, 6.4, 6.5 | Copertura quasi completa |

**DCEdu 6.1 (Information literacy)** è la competenza più presidiata — coperta da tre risorse distinte.

## INDIRE — standard attivabili

| Standard | Attivato da |
|---|---|
| **A1 — Progettazione** | Quasi tutte le risorse |
| **A2 — Gestione aula** | Pillole con dual-mode docente, attività Caccia alla fonte |
| **A3 — Valutazione** | Strumento Verifica Fonti, BEP Tool, checklist interattive |
| **A4 — Inclusione** | Dual-mode studente/docente nelle pillole |
| **C1 — Sviluppo professionale** | Guida Prompting, Peer-review IA |
| **C2 — Identità professionale** | PDF bilingue, documentazione metodologica |

**Gap:** B1 (collaborazione tra colleghi) e B2 (coinvolgimento famiglie) — nessuna risorsa li presidia.

## Priorità di sviluppo contenuti (ottica INDIRE/DigComp)

| Priorità | Risorsa suggerita | Standard attivati |
|---|---|---|
| [!] 1 | Pillola netiquette / cittadinanza digitale | DC 2.2–2.4 · DCEdu 6.4 · INDIRE A4 |
| [~] 2 | Guida/strumento collaborazione scolastica | INDIRE B1·B2 · DCEdu 1.2·2.3 |
| [?] 3 | Risorsa valutazione digitale (rubric builder) | DCEdu 4.1·4.2·4.3 · INDIRE A3 |

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

## Classificazione header per tipo

| Tipo | Classi CSS | Pagine |
|---|---|---|
| Homepage | `header` + `.header-brand` inline | `index.html` |
| Sottopagine standard | `.guide-header` (ora in `shared.css`) | Guide, pillole, strumenti con sidebar |
| Pagine custom | `nav.sticky-bar` o `#header` | Subnet, Marketing, Prompting, SEO, Wiki |

## Bug in coda — refactor struttura

| Priorità | Bug |
|---|---|
| [!] | Guida Marketing — header con bottoni download su mobile troppo largo |
| [!] | Subnet Calculator — hamburger mancante, sidebar non accessibile su mobile |
| [!] | HFS Server — nessun menu di navigazione |
| [!] | LibreOffice Base Query — barra navigazione sparisce durante scroll, manca back-to-top |
| [?] | Hamburger a sinistra su Pillola SEO e Wiki Speedrun — inconsistente con pagine `.guide-header` |
| [?] | Modalità Aula Guida Prompting — verificare fix post-deploy |

---

# Dark Mode — Analisi Architetturale

Analisi prodotta in maggio 2026. Implementazione non ancora avviata.

## Valutazione

Il dark mode è raccomandato. Il costo reale non è tecnico — è di manutenzione CSS: ogni nuovo componente deve prevedere la variante dark. Tutto centralizzato in `shared.css`, nessuna modifica ai singoli file delle guide.

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

# Roadmap

## Completato

- [OK] Migrazione Vercel (maggio 2026)
- [OK] Dominio formazione-digitale.it registrato su Aruba
- [OK] Sessione responsive mobile (08/05/2026)
- [OK] Pillola Valutazione Fonti + Strumento Verifica Fonti (maggio 2026)

## Bassa urgenza — quando disponibile

- Redirect 301 da github.io + disabilitazione GitHub Pages
- Cambio indirizzo Google Search Console

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

## Miglioramenti continui

- `font-display: swap` per migliorare LCP mobile (attuale 4.8s)
- Conversione PNG → WebP
- Migrazione JS in `/js/`
- Nuovi contenuti: Pillola netiquette · Pillola PageSpeed · Pillola Triade CIA

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
