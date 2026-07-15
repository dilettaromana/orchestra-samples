# Licenze delle fonti

Questo repository **non** ridistribuisce campioni: la cartella `samples/` e' vuota e
va popolata in locale. Ogni fonte ha la propria licenza — verificala prima di
pubblicare l'app o il repository popolato.

| Fonte | Contenuto | Licenza (verificare) |
|---|---|---|
| VSCO 2 Community Edition / VCSL (Versilian) | orchestra (archi, fiati, ottoni, percussioni) | CC0 (dominio pubblico) |
| Salamander Grand Piano (Alexander Holm) | pianoforte, multi-velocity | CC-BY 3.0 (attribuzione) |
| Philharmonia Orchestra samples | note singole per strumento | uso libero/educativo — vedi termini del sito |
| University of Iowa MIS | note singole per strumento | uso libero — vedi termini |
| FluidR3_GM (Frank Wen) choir_aahs | coro "aah" (soundfont GM) | MIT (wrapper midi-js-soundfonts) / licenza soundfont FluidR3 |
| nbrosowsky/tonejs-instruments | vari (derivati VSCO2) | CC-BY |

## Note

- **CC0**: nessuna attribuzione richiesta, uso libero anche commerciale.
- **CC-BY**: attribuzione obbligatoria (cita autore/fonte nei crediti dell'app).
- Le fonti "uso educativo/libero" possono avere restrizioni sulla redistribuzione dei
  file grezzi: spesso e' ok usarle in un'app, meno ridistribuire il set completo.
- **Suno e altri generatori AI**: gli *stems* sono esecuzioni di un brano, non strumenti
  suonabili nota-per-nota, e i termini/il contenzioso in corso li rendono inadatti come
  fonte di una libreria di campioni. Non usarli qui.

## Attribuzioni — campioni inclusi in questo pacchetto

I campioni presenti in `samples/` provengono da:

- **VSCO 2 Community Edition** — Versilian Studios LLC
  https://github.com/sgossner/VSCO-2-CE — licenza **CC0** (pubblico dominio).
  Nessuna attribuzione e' obbligatoria, nessuna royalty, uso anche commerciale.
  L'attribuzione qui sopra e' un ringraziamento, non un obbligo.

Trattamento applicato: selezione delle articolazioni tenute (sus/susVib/susLong/Arco Vib),
conversione da WAV 44.1 kHz a Ogg Vorbis (q4), riorganizzazione in livelli dinamici
p/f secondo le convenzioni di questo repository. Nessuna altra elaborazione.

- **Salamander Grand Piano** (cartella `samples/piano/`) — **Alexander Holm**
  licenza **CC-BY 3.0**. Distribuito qui nella versione a note singole del mirror
  Tone.js (https://github.com/Tonejs/audio). File .mp3 originali, non ricompressi.
  **L'attribuzione e' OBBLIGATORIA**: se pubblichi l'app, cita autore, licenza e
  fonte nei crediti. Testo pronto:
  «Pianoforte: Salamander Grand Piano di Alexander Holm, licenza CC-BY 3.0.»

- **FluidR3_GM — choir_aahs** (cartella `samples/choir-aah/`) — Frank Wen,
  tramite la raccolta midi-js-soundfonts (https://github.com/gleitz/midi-js-soundfonts).
  Wrapper MIT; si applicano i termini del soundfont FluidR3.

- **tonejs-instruments** (cartelle `guitar-acoustic/`, `guitar-electric/`, `bass-electric/`)
  — Nicholas Brosowsky, https://github.com/nbrosowsky/tonejs-instruments
  licenza **CC-BY**. File .ogg originali, non ricompressi. **Attribuzione obbligatoria.**
  Testo pronto: «Chitarre e basso elettrico: tonejs-instruments (N. Brosowsky), CC-BY.»

- **VCSL — Versilian Community Sample Library** (organo, sassofono, percussioni,
  campane tubolari) — Versilian Studios LLC, https://github.com/sgossner/VCSL
  licenza **CC0**. Nessun obbligo.

## Obblighi in sintesi

| Cartella | Fonte | Licenza | Attribuzione |
|---|---|---|---|
| tutti gli strumenti VSCO | VSCO 2 CE — Versilian Studios | CC0 | non richiesta |
| `piano/` | Salamander — Alexander Holm | CC-BY 3.0 | **obbligatoria** |
| `choir-aah/` | FluidR3_GM — Frank Wen | soundfont FluidR3 | consigliata |
| organo, sax, percussioni, campane | VCSL — Versilian Studios | CC0 | non richiesta |
| `guitar-*`, `bass-electric` | tonejs-instruments — N. Brosowsky | CC-BY | **obbligatoria** |

Nota sul pianoforte: questo mirror contiene **un solo livello dinamico** per nota
(l'originale di Holm ne ha 16). Il suono resta ottimo, ma non cambia timbro con
l'intensita' come farebbe la libreria completa.
