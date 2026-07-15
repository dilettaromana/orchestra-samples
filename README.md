# orchestra-samples

Libreria di **campioni reali multicampionati** per l'app *orchestra multi-agente*
(Tone.js). Sostituisce i suoni sintetici / il soundfont GM con strumenti registrati,
organizzati per **layer dinamici** e con **round-robin**, caricati via un `manifest.json`.

## Perche'

I campioni "reali" attuali dell'app suonano ancora elettronici perche':
- il coro usa un soundfont General MIDI con pochi punti di campione;
- gli strumenti hanno spesso un solo layer dinamico e poche note campionate;
- non c'e' round-robin (note ripetute identiche = effetto "mitragliatrice").

Questo repo risolve questi punti fornendo una struttura pensata per multicampioni di
qualita', un loader che gestisce layer+round-robin, e strumenti per popolarlo con
librerie libere.

## Struttura

```
orchestra-samples/
├─ manifest.json          # manifest target (locale, da popolare)
├─ manifest.cdn.json      # manifest demo: funziona subito da CDN pubblici
├─ loader/
│  └─ orchestra-samples.js  # loader: window.OrchestraSamples (layer + round-robin)
├─ tools/
│  ├─ prepare_samples.py  # scarica/converte campioni liberi (da eseguire in locale)
│  └─ make_manifest.py    # rigenera manifest.json scandendo ./samples
├─ sw/
│  └─ orchestra-sw.js     # service worker: cache offline (kiosk)
├─ examples/
│  ├─ demo.html           # demo minimale (coro + xilofono da CDN)
│  └─ integration.md      # come collegarlo all'app
└─ samples/               # qui vanno i file audio (vuoto nel repo)
```

## Campioni gia' inclusi (VSCO 2 CE, CC0)

Questo pacchetto arriva **gia' popolato** con 16 strumenti reali estratti da
**VSCO 2 Community Edition** (Versilian Studios, CC0): archi di sezione, violino solo,
arpa, legni (incluso l'**oboe**, prima solo sintetico), ottoni e mallet
(glockenspiel, xilofono, marimba). In tutto ~300 campioni, ~39 MB in Ogg Vorbis,
con due livelli dinamici (p/f) dove la fonte li offre.

| Famiglia | Strumenti |
|---|---|
| Archi | violin, viola, cello, contrabass, violin-solo, harp |
| Legni | flute, oboe, clarinet, bassoon |
| Ottoni | french-horn, trumpet, trombone |
| Mallet | glockenspiel, xylophone, marimba |
| Coro | choir-aah (17 note) |
| Tastiere | piano (Salamander), organ (VCSL) |
| Moderni | guitar-acoustic, guitar-electric, bass-electric, saxophone |
| Percussioni | timpani, bass-drum, snare, tom, cymbals, hi-hat, gong, triangle, woodblock, tambourine, tubular-bells |

**Non devi scaricare nulla:** e' tutto incluso. In tutto **34 strumenti, ~490
campioni**, e nessuna sezione dell'app resta senza campione. Gli strumenti VSCO sono in `.ogg`; coro e
pianoforte restano `.mp3` originali (nessuna ricompressione): il manifest indica
l'estensione **per singolo strumento**, quindi convivono senza problemi.

## Avvio rapido (senza scaricare nulla)

Apri `examples/demo.html` con una rete attiva: carica il coro e lo xilofono dai CDN
pubblici e suona una scala. Serve a verificare il loader.

## Popolare con campioni di qualita' (in locale)

```bash
# coro (mp3, veloce) e pianoforte Salamander (multi-nota)
python3 tools/prepare_samples.py --choir --salamander

# converti in ogg (piu' leggero per il web; richiede ffmpeg)
python3 tools/prepare_samples.py --choir --salamander --to-ogg

# rigenera il manifest dalla struttura scaricata
python3 tools/make_manifest.py
```

Per archi/fiati/ottoni/percussioni di qualita' usa librerie **libere e CC-clean**
(vedi `LICENSES.md`): scaricale, copia i WAV in `samples/<strumento>/<layer>/<NOTA>.wav`
(es. `samples/violin/f/A3.wav`), converti in ogg e rilancia `make_manifest.py`.

## Convenzioni di cartella

```
samples/violin/A3.ogg                 # layer unico
samples/violin/p/A3.ogg               # layer dinamico "piano"
samples/violin/f/A3.ogg               # layer dinamico "forte"
samples/violin/f/A3_1.ogg  A3_2.ogg   # round-robin (varianti della stessa nota)
```

Layer riconosciuti (dal piu' piano al piu' forte): `ppp pp p mp mf f ff fff`.
Note in notazione scientifica con bemolle (`Eb4`) o diesis (`Ds4`).

## Fonti consigliate (libere)

- **VSCO 2 Community Edition** / **VCSL** — orchestra, CC0.
- **Salamander Grand Piano** — pianoforte, CC-BY, multi-velocity.
- **Philharmonia Orchestra** e **University of Iowa MIS** — note singole per strumento.
- **FluidR3_GM choir_aahs** — coro (soundfont GM), gia' usato nella demo.

Vedi `LICENSES.md` per i dettagli e verifica sempre i termini prima della pubblicazione.

## Integrazione con l'app

Vedi `examples/integration.md`.
