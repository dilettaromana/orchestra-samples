# orchestra-samples

Libreria di **campioni reali multicampionati** per l'app *orchestra distribuita*
(Tone.js). Sostituisce i suoni sintetici con strumenti registrati, organizzati per
**strati dinamici** e **round-robin**, caricati da un solo `manifest.json`.

**Versione 0.4.0** — 42 strumenti, 574 note campionate, ogni pacco **verificato per
misura**: intonazione, livello e ambito.

---

## Che cosa distingue questo deposito

Tre cose che non si vedono aprendo una cartella di campioni, e che qui sono state
misurate una per una.

**1. L'intonazione è verificata, non dichiarata.** Il nome di un file è
un'affermazione: nelle raccolte d'origine ci sono campioni che dicono una nota e ne
suonano un'altra (un trombone «do 4» che suona il do sotto). Ogni file è stato
misurato con **due metodi indipendenti** — serie armonica sui picchi e
autocorrelazione — e tenuto solo se i due concordano. Quarantatré candidati sono
stati scartati; dove nessun candidato passava, la nota è stata lasciata vuota:
*un buco nella scala si sente meno di una nota sbagliata*. Ogni campione accettato
è poi portato in intonazione esatta a 440 Hz.

**2. I livelli sono pari, e dichiarati.** Prima, fra lo strumento più forte e il
più debole del deposito c'erano **quasi 50 dB** (un contralto a −8,6 dBFS, un
triangolo a −56,5): ogni applicazione doveva ritarare a mano ogni strumento. Ora i
pacchi rifatti escono tutti a **−20 dBFS** sullo strato forte (±0,5 dB), e per
**tutti** gli strumenti il livello misurato è scritto nel manifesto:

```json
{ "livelloRif": -20.0,
  "instruments": { "violin": { "livelloDb": -31.0, "layers": [...] } } }
```

Chi carica il pacco sa quanto alzare o abbassare senza doverlo indovinare.

**3. L'ambito è coperto con strumenti reali, non con trasposizioni estreme.** Un
campione stirato di mezz'ottava perde la fondamentale e la sua altezza diventa
incerta. Dove un pacco non arrivava, il registro è stato esteso con **lo strumento
che nella realtà suona quelle note**:

| pacco | ambito | il registro grave viene da |
|---|---|---|
| `saxophone` | G#1 – D6 | sassofono **tenore** sotto il re3 |
| `trombone` | D1 – C5 | **tuba** sotto il mi2 |
| `clarinet` | D2 – F#6 | **clarinetto basso** sotto il re3 |
| `bassoon` | C1 – D5 | **controfagotto** sotto il la#1 |
| `oboe` | E3 – E6 | **corno inglese** sotto il la#3 |

Alla giunzione fra i due strumenti il livello è pareggiato per misura, entro
**0,2 dB**: un cambio di colore quasi non si nota, uno scalino di volume sempre.

---

## Inventario

`passo` = distanza massima in semitoni fra un campione e il successivo (quanto il
campionatore deve trasportare). Sotto i 4 semitoni il trasporto non si sente.

### Rifatti e verificati (v0.2–0.4)

| strumento | note | passo | ambito | strati |
|---|---:|---:|---|---:|
| saxophone | 28 | 2 | G#1–D6 | 2 |
| clarinet | 27 | 2 | D2–F#6 | 2 |
| bassoon | 26 | 2 | C1–D5 | 2 |
| trombone | 23 | 4 | D1–C5 | 2 |
| french-horn | 22 | 2 | B1–F5 | 2 |
| violin-solo | 21 | 2 | G3–B6 | 2 |
| flute | 19 | 2 | C4–C7 | 2 |
| oboe | 19 | 2 | E3–E6 | 2 |
| contrabass | 18 | 2 | C1–A#3 | 2 |
| trumpet | 16 | 2 | F3–B5 | 2 |
| timpani | 14 | 3 | E2–D4 | 2 |
| choir-male | 24 | **1** | G2–F#4 | 1 |
| choir-female | 18 | **1** | G4–C6 | 1 |

I **timpani** meritano una riga: erano *un solo campione* stirato su due ottave.
Le quattordici altezze attuali vengono da otto tamburi accordati diversamente, e la
nota di ciascuno è stata **misurata sul suono** — una membrana ha i modi a 1,5 e
1,98 volte la fondamentale, non a 2 e 3, quindi il metodo buono per un violino qui
sbaglia. Dove il colpo piano e il colpo forte non concordavano, il tamburo è stato
escluso.

Il **coro** era un pacco solo per tutte e cinque le voci: i bassi lo cantavano due
ottave sotto i soprani, e due ottave di trasporto su una voce non danno un basso.
Ora sono due, cromatici, ciascuno nel proprio ambito.

### Ereditati (VSCO 2 CE e altri, invariati)

Archi di sezione (`violin`, `viola`, `cello`), `piano`, `organ`, `harp`,
`accordion`, chitarre e basso elettrico, mallet (`glockenspiel`, `xylophone`,
`marimba`, `tubular-bells`), `choir-aah`, le cinque voci soliste, e le percussioni
a rumore (`snare`, `cymbals`, `hi-hat`, `bass-drum`, `tom`, `tambourine`,
`triangle`, `woodblock`, `gong`). Per questi il livello misurato è comunque
dichiarato nel manifesto.

> **Nota onesta su due di essi:** `baritone-solo` e `bass-solo` sono gli **stessi
> file** con due nomi (correlazione 1,000 su tutte le note in comune). Le voci
> soliste reali sono quattro, non cinque. E un mezzosoprano non c'è.

---

## Struttura

```
orchestra-samples/
├─ manifest.json            # la mappa: strumento -> strati -> nota -> file
├─ loader/
│  └─ orchestra-samples.js  # loader: window.OrchestraSamples (strati + round-robin)
├─ tools/                   # utilita' per popolare e rigenerare il manifest
├─ examples/                # demo minimale e note d'integrazione
└─ samples/
   ├─ saxophone/p/Gs1.ogg   # strato piano
   ├─ saxophone/f/Gs1.ogg   # strato forte
   └─ timpani/f/C3_1.ogg    # round-robin (varianti della stessa nota)
```

Note in notazione scientifica; il diesis nel **nome del file** si scrive `s`
(`Fs3`), nella **chiave del manifesto** con `#` (`F#3`). Il manifesto indica
l'estensione **per singolo strumento**, quindi `.ogg` e `.mp3` convivono.

Un file rotto non deve costare uno strumento: il loader tollera i campioni che non
si decodificano, li dichiara in `inst.caduti` e suona con quelli che ha. (Serviva:
in questo deposito c'era un file di 671 byte che non è audio, e portava via l'intera
voce di contralto.)

---

## Verificare il pacco

Dall'app *orchestra distribuita*:

```bash
node prove/campioni.mjs            # conta: note, passo, ambito, chi e' magro
node prove/campioni.mjs --verifica # controlla anche che ogni file esista davvero
node prove/pacco.mjs               # SUONA il pacco e misura l'altezza di ogni nota
```

La seconda prova è quella che conta: un controllo sui file di partenza non vede i
guasti della lavorazione. Un esempio vero — i campioni del sassofono tenore sono a
48 kHz, e una conversione che forzava 44,1 nel punto sbagliato li faceva scendere di
**un semitono e mezzo**. Tutte le verifiche sull'ingresso dicevano «perfetto».

---

## Fonti e licenze

| fonte | che cosa | licenza |
|---|---|---|
| [Philharmonia Orchestra](https://philharmonia.co.uk/resources/sound-samples/) | fiati, ottoni, violino solista, contrabbasso, tuba, clarinetto basso, controfagotto, corno inglese | libere per uso musicale |
| [VCSL — Versilian Community Sample Library](https://github.com/sgossner/VCSL) | timpani, sassofono tenore | CC0 |
| [Sonatina Symphonic Orchestra](https://github.com/peastman/sso) | cori femminile e maschile | CC Sampling Plus 1.0 |
| [VSCO 2 Community Edition](https://github.com/sgossner/VSCO-2-CE) | archi di sezione, mallet, percussioni | CC0 |
| Salamander Grand Piano | pianoforte | CC-BY |

Vedi `LICENSES.md` per i dettagli. Verifica sempre i termini prima di ripubblicare.

---

## Integrazione

Vedi `examples/integration.md`. In breve: si carica il manifesto una volta,
si chiedono solo gli strumenti che servono, e si legge `livelloDb` per sapere a che
livello sono stati registrati.

```js
const banks = await OrchestraSamples.load(MANIFEST_URL,
  { only: ["saxophone"], baseUrl: BASE + "samples/" });
banks.saxophone.connect(destinazione);
banks.saxophone.triggerAttackRelease("F#2", 1.2, quando, 0.8);
```
