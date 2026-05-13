#!/usr/bin/env python3
"""
icdl_to_json.py — Converte i report Excel ICDL in data.json anonimizzato.

Uso:
    python scripts/icdl_to_json.py

Cerca automaticamente tutti i file export_*.xlsx in data-src/,
li unisce e scrive icdl/statistiche/data.json.

La cartella data-src/ è in .gitignore — gli Excel non vanno mai sul repo.
I dati personali (Candidato, Codice Fiscale, Codice Skillscard) vengono rimossi.

Certificazioni calcolate per candidato (basate su Codice Skillscard):
- ICDL Essentials:    Computer Essentials + Online Essentials superati
- ICDL Base:          Computer Essentials + Online Essentials + Word Processing + Spreadsheets superati
- ICDL Cyber Security: Cyber Security superato
- ICDL Full Standard: tutti e 7 i moduli ICDL superati
"""

import json
import os
import glob
from datetime import datetime, date

try:
    import pandas as pd
except ImportError:
    print("Errore: pandas non installato. Esegui: pip install pandas openpyxl")
    raise SystemExit(1)

# Root del repo = cartella padre di scripts/
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORGENTE = os.path.join(ROOT, "data-src", "export_*.xlsx")
OUTPUT   = os.path.join(ROOT, "icdl", "statistiche", "data.json")

COLONNE = {
    "Certificazione":   "certificazione",
    "Modulo":           "modulo",
    "Punteggio":        "punteggio",
    "Punteggio minimo": "punteggio_minimo",
    "Esito":            "esito",
    "Completato il":    "data",
}

# Requisiti per ogni certificazione ICDL
CERT_REQUISITI = {
    "ICDL Essentials":     {"Computer Essentials", "Online Essentials"},
    "ICDL Base":           {"Computer Essentials", "Online Essentials",
                            "Word Processing", "Spreadsheets"},
    "ICDL Cyber Security": {"Cyber Security"},
    "ICDL Full Standard":  {"Computer Essentials", "Online Essentials",
                            "Word Processing", "Spreadsheets",
                            "Presentation", "Online Collaboration", "Cyber Security"},
}


def parse_data(valore):
    if isinstance(valore, (datetime, date)):
        return valore.strftime("%Y-%m-%d")
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(valore).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return str(valore).strip()


def leggi_excel(percorso):
    df = pd.read_excel(percorso)
    mancanti = [c for c in COLONNE if c not in df.columns]
    if mancanti:
        print(f"  ⚠ Colonne mancanti in {percorso}: {mancanti} — file ignorato")
        return None, None
    # DataFrame completo (con Codice Skillscard) per il calcolo certificazioni
    df_raw = df.copy()
    # DataFrame anonimizzato per l'export
    df_anon = df[list(COLONNE.keys())].rename(columns=COLONNE)
    df_anon["data"] = df_anon["data"].apply(parse_data)
    return df_anon, df_raw


def calcola_certificazioni(frames_raw):
    """
    Calcola quanti candidati hanno ottenuto ciascuna certificazione ICDL.
    Usa Codice Skillscard come identificatore anonimo — non compare nel JSON.
    Un candidato può ottenere da 0 a 4 certificazioni.
    """
    # Unisci tutti i DataFrame raw
    tutto_raw = pd.concat(frames_raw, ignore_index=True)

    # Filtra solo moduli ICDL superati
    icdl_ok = tutto_raw[
        (tutto_raw["Certificazione"] == "ICDL") &
        (tutto_raw["Esito"] == "Superato")
    ]

    # Per ogni candidato, costruiamo l'insieme dei moduli superati
    per_candidato = icdl_ok.groupby("Codice Skillscard")["Modulo"].apply(set)

    risultati = {}
    for nome_cert, requisiti in CERT_REQUISITI.items():
        count = sum(1 for moduli in per_candidato if requisiti.issubset(moduli))
        risultati[nome_cert] = count

    return risultati


def main():
    file_trovati = sorted(glob.glob(SORGENTE))

    if not file_trovati:
        print(f"Nessun file trovato in {SORGENTE}")
        print("Assicurati che la cartella data-src/ esista e contenga i file export_*.xlsx")
        raise SystemExit(1)

    print(f"File trovati: {len(file_trovati)}")
    frames_anon = []
    frames_raw  = []

    for f in file_trovati:
        print(f"  Lettura: {f}")
        df_anon, df_raw = leggi_excel(f)
        if df_anon is not None:
            frames_anon.append(df_anon)
            frames_raw.append(df_raw)

    if not frames_anon:
        print("Nessun file valido da processare.")
        raise SystemExit(1)

    tutto = pd.concat(frames_anon, ignore_index=True)
    tutto = tutto.sort_values("data").reset_index(drop=True)

    certificazioni = calcola_certificazioni(frames_raw)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    output = {
        "generato_il":   datetime.today().strftime("%Y-%m-%d"),
        "certificazioni": certificazioni,
        "esami":          tutto.to_dict(orient="records"),
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nOK: {len(tutto)} esami scritti in {OUTPUT}")
    print(f"    Periodo: {tutto['data'].min()} → {tutto['data'].max()}")
    print(f"\nCertificazioni calcolate:")
    for nome, count in certificazioni.items():
        print(f"    {nome}: {count}")


if __name__ == "__main__":
    main()
