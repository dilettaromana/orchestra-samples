#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_manifest.py — genera manifest.json scandendo ./samples.

Convenzioni di cartella riconosciute:
    samples/<strumento>/<NOTA>.<ext>                  -> layer unico
    samples/<strumento>/<layer>/<NOTA>.<ext>          -> layer dinamico (p/mp/mf/f/ff)
    samples/<strumento>/<layer>/<NOTA>_<n>.<ext>      -> round-robin (n = 1,2,3...)

Le NOTE seguono la notazione scientifica con bemolle (Eb4, Gb3) o diesis (Ds4, Fs3):
Tone.Sampler accetta entrambe.

I layer dinamici vengono mappati a fasce di velocity in ordine dal piu' piano al
piu' forte. Se non ci sono sottocartelle di layer, lo strumento ha un layer unico.
"""

import json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "samples")

LAYER_ORDER = ["ppp","pp","p","mp","mf","f","ff","fff"]
NOTE_RE = re.compile(r"^([A-G](?:b|#|s)?-?\d)(?:_(\d+))?$")

def note_key(n):
    """Chiave della nota per Tone.js: accetta '#' e 'b', NON la 's'.
    Il file su disco usa 's' perche' '#' non e' valido in un URL: Fs3.ogg -> chiave F#3."""
    return re.sub(r"^([A-G])s", r"\1#", n)

def vel_ranges(n):
    if n <= 1: return [[0.0, 1.0]]
    step = 1.0 / n
    return [[round(i*step,3), round((i+1)*step,3)] for i in range(n)]

def scan_instrument(instr_dir, embed_ext=False):
    """Ritorna (layers, has_layers). layers = lista di dict nome->map."""
    entries = sorted(os.listdir(instr_dir))
    subdirs = [e for e in entries if os.path.isdir(os.path.join(instr_dir, e))]
    def collect(folder, prefix, embed_ext=False):
        rr = defaultdict(dict)   # nota -> {rr_index: relpath}
        for f in sorted(os.listdir(folder)):
            base, ext = os.path.splitext(f)
            if ext.lower() not in (".ogg",".mp3",".wav",".flac"): continue
            m = NOTE_RE.match(base)
            if not m: continue
            note, idx = m.group(1), int(m.group(2) or 1)
            rel = (prefix + "/" + (base + ext if embed_ext else base)).lstrip("/")
            rr[note][idx] = rel
        # compatta: se una nota ha piu' varianti -> lista, altrimenti stringa
        out = {}
        for note, variants in rr.items():
            files = [variants[k] for k in sorted(variants)]
            out[note_key(note)] = files if len(files) > 1 else files[0]
        return out

    instr_name = os.path.basename(instr_dir)
    layer_dirs = [d for d in subdirs if d in LAYER_ORDER]
    if layer_dirs:
        layer_dirs = sorted(layer_dirs, key=lambda d: LAYER_ORDER.index(d))
        vr = vel_ranges(len(layer_dirs))
        layers = []
        for i, ld in enumerate(layer_dirs):
            m = collect(os.path.join(instr_dir, ld), instr_name + "/" + ld, embed_ext)
            if m: layers.append({"velRange": vr[i], "map": m})
        return layers
    else:
        m = collect(instr_dir, instr_name, embed_ext)
        return [{"map": m}] if m else []

def instr_exts(d):
    """Estensioni audio presenti sotto la cartella di uno strumento."""
    out = set()
    for root, _, files in os.walk(d):
        for f in files:
            e = os.path.splitext(f)[1].lower()
            if e in (".ogg", ".mp3", ".wav", ".flac"): out.add(e)
    return out

def main():
    if not os.path.isdir(SAMPLES):
        print("nessuna cartella samples/"); sys.exit(1)
    instruments = {}
    for name in sorted(os.listdir(SAMPLES)):
        d = os.path.join(SAMPLES, name)
        if not os.path.isdir(d): continue
        exts = instr_exts(d)
        mixed = len(exts) > 1
        layers = scan_instrument(d, embed_ext=mixed)
        if not layers:
            print("  (vuoto, salto)", name); continue
        # estensione per strumento: cosi' .mp3 e .ogg possono convivere nella stessa libreria
        ext = "" if mixed else (list(exts)[0] if exts else "")
        instruments[name] = {"release": 1.0, "ext": ext, "layers": layers}
        pts = sum(len(L["map"]) for L in layers)
        print("  %-16s %d layer, %3d note  %s" % (name, len(layers), pts, ext or "(estensioni miste)"))

    manifest = {
        "name": "orchestra-samples",
        "version": "0.1.0",
        "baseUrl": "./samples/",
        "ext": ".ogg",
        "instruments": instruments
    }
    out = os.path.join(ROOT, "manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("scritto", os.path.relpath(out, ROOT), "-", len(instruments), "strumenti")

if __name__ == "__main__":
    main()
