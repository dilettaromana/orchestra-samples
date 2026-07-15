# SAMPLE_MAP — gia' inclusa nell'app

**Non devi piu' modificare la `SAMPLE_MAP`**: la versione aggiornata dell'app
(`orchestra_multiagente_completa.html`) la contiene gia', con tutte le sezioni
collegate ai campioni di questo pacchetto. Questo file resta solo come riferimento.


Con i campioni inclusi in questo pacchetto puoi sostituire la `SAMPLE_MAP`
dell'app (`orchestra_multiagente_completa.html`) con questa versione, che sfrutta
i nuovi strumenti: **oboe**, **viola** e **violin-solo** dedicati, più i mallet.

```js
const SAMPLE_MAP={ flauti:"flute", oboi:"oboe", clarinetti:"clarinet", fagotti:"bassoon",
  corni:"french-horn", trombe:"trumpet", tromboni:"trombone",
  violiniI:"violin", violiniII:"violin", viole:"viola", celli:"cello", bassi:"contrabass",
  piano:"piano", arpa:"harp", organo:"organ",
  chitarra:"guitar-acoustic", chitarraE:"guitar-electric", bassoE:"bass-electric", sax:"saxophone",
  xilofono:"xylophone", glockenspiel:"glockenspiel", marimba:"marimba",
  violinoSolo:"violin-solo", celloSolo:"cello", flautoSolo:"flute", trombaSolo:"trumpet" };
```

Novità rispetto alla versione precedente:

| Sezione | Prima | Ora |
|---|---|---|
| Oboi | solo sintesi | campioni reali (`oboe`) |
| Viole | campione di violino | campioni di viola (`viola`) |
| Violino solista | campione di violino di sezione | vero violino solo (`violin-solo`) |
| Glockenspiel, Marimba | solo sintesi | campioni reali |

`piano` e il coro (`choir-aah`) **sono inclusi** e funzionano gia' con la mappa qui
sopra: il pianoforte tramite `piano:"piano"`, il coro tramite il blocco delle cinque
voci dentro `loadSamples()`.

Restano fuori dal pacchetto `organo`, `guitar-acoustic`, `guitar-electric`,
`bass-electric`, `saxophone` e i timpani: quelle sezioni continueranno a usare la
sintesi (nessun errore, semplicemente non trovano il campione).
