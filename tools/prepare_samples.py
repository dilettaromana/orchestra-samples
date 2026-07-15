#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepare_samples.py — scarica campioni liberi nella struttura ./samples e (opzionale)
li converte in .ogg. DA ESEGUIRE IN LOCALE, dove la rete verso le sorgenti e'
raggiungibile. Rispetta e verifica sempre le licenze (vedi LICENSES.md).

Uso:
    python3 tools/prepare_samples.py --choir            # coro FluidR3 (mp3, veloce)
    python3 tools/prepare_samples.py --salamander       # pianoforte Salamander (mp3)
    python3 tools/prepare_samples.py --all
    python3 tools/prepare_samples.py --choir --to-ogg   # converte in ogg via ffmpeg

Sorgenti orchestrali di qualita' (archi/fiati/ottoni/percussioni) come VSCO2 CE /
VCSL sono grandi (centinaia di MB) e distribuite come pacchetti: la sezione
ORCHESTRAL qui sotto va configurata a mano con i percorsi corretti dopo averle
scaricate. Vedi README.md per i link.
"""

import argparse, os, sys, subprocess, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "samples")

# --- sorgenti a nota-per-file, affidabili (naturali + bemolle) ---
CHOIR_BASE = "https://cdn.jsdelivr.net/gh/gleitz/midi-js-soundfonts/FluidR3_GM/choir_aahs-mp3/"
CHOIR_NOTES = ["C2","Eb2","Gb2","A2","C3","Eb3","Gb3","A3","C4","Eb4","Gb4","A4","C5","Eb5","Gb5","A5","C6"]

# Salamander Grand Piano (mirror Tone.js). Note campionate ogni terza minore, layer unico "mp3".
SALAMANDER_BASE = "https://tonejs.github.io/audio/salamander/"
SALAMANDER_NOTES = ["A0","C1","Ds1","Fs1","A1","C2","Ds2","Fs2","A2","C3","Ds3","Fs3",
                    "A3","C4","Ds4","Fs4","A4","C5","Ds5","Fs5","A5","C6","Ds6","Fs6","A6","C7","Ds7","Fs7","A7","C8"]

def fetch(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "orchestra-samples/0.1"})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
            f.write(r.read())
        print("  ok  ", os.path.relpath(dest, ROOT))
        return True
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print("  MISS", url, "->", e)
        return False

def to_ogg(path):
    """Converte in .ogg via ffmpeg (se presente) e rimuove l'originale."""
    if not path.lower().endswith((".mp3", ".wav", ".flac")):
        return
    out = os.path.splitext(path)[0] + ".ogg"
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path,
                        "-c:a", "libvorbis", "-q:a", "5", out], check=True)
        os.remove(path)
        print("  ogg ", os.path.relpath(out, ROOT))
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  (ffmpeg non disponibile: salto conversione di", os.path.basename(path), ")")

def grab(base, notes, subdir, ext, to_ogg_flag):
    print("scarico", subdir, "...")
    got = 0
    for n in notes:
        dest = os.path.join(SAMPLES, subdir, n + ext)
        if fetch(base + n + ext, dest):
            got += 1
            if to_ogg_flag:
                to_ogg(dest)
    print("  totale:", got, "/", len(notes))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--choir", action="store_true")
    ap.add_argument("--salamander", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--to-ogg", action="store_true", help="converte in ogg (richiede ffmpeg)")
    a = ap.parse_args()
    if not (a.choir or a.salamander or a.all):
        ap.print_help(); sys.exit(0)

    if a.choir or a.all:
        grab(CHOIR_BASE, CHOIR_NOTES, "choir-aah", ".mp3", a.to_ogg)
    if a.salamander or a.all:
        grab(SALAMANDER_BASE, SALAMANDER_NOTES, "piano", ".mp3", a.to_ogg)

    # --- ORCHESTRAL (da configurare a mano dopo il download dei pacchetti) ---
    # Esempio: dopo aver scaricato VSCO2 CE / VCSL, copiare i WAV in
    #   samples/violin/p/A3.wav, samples/violin/f/A3_1.wav, ...
    # e poi lanciare:  python3 tools/prepare_samples.py --to-ogg  (solo conversione)
    # oppure convertire con: for f in samples/**/*.wav; do ffmpeg -i "$f" -q:a 5 "${f%.wav}.ogg"; done

    print("\nfatto. Ora rigenera il manifest:  python3 tools/make_manifest.py")

if __name__ == "__main__":
    main()
