# Integrazione con l'app orchestra multi-agente

L'app (`orchestra_multiagente_completa.html`) oggi carica i campioni in `loadSamples()`
usando la libreria `tonejs-instruments` per gli strumenti e un soundfont GM per il coro.
Per farla attingere a **questo repository** basta sostituire quella funzione con il
loader qui incluso.

## 1. Aggiungi il loader

Nell'`<head>` (dopo lo script di Tone.js) aggiungi:

```html
<script src="https://cdn.jsdelivr.net/gh/TUO-UTENTE/orchestra-samples/loader/orchestra-samples.js"></script>
```

(oppure il percorso locale se distribuisci il repo insieme all'app).

## 2. Sostituisci `loadSamples()`

Idea: costruisci il banco dal manifest e mappa `samplers[sezione] = banco[strumento]`,
riusando la stessa tabella `SAMPLE_MAP` gia' presente nell'app.

```js
const SAMPLES_MANIFEST =
  "https://cdn.jsdelivr.net/gh/TUO-UTENTE/orchestra-samples/manifest.json";

async function loadSamples(){
  if(samplesReady) return true; if(samplesLoading) return false;
  if(typeof OrchestraSamples==="undefined"){ sampStatus("loader non disponibile"); return false; }
  samplesLoading=true; sampStatus("caricamento campioni\u2026");
  try{
    await ensureStarted();
    // strumenti orchestrali dal manifest
    const bank = await OrchestraSamples.load(SAMPLES_MANIFEST);
    for(const [id,instr] of Object.entries(SAMPLE_MAP)){
      const inst = bank[instr];
      if(!inst) continue;
      const fam=(SECTIONS.find(s=>s.id===id)||{}).family;
      inst.connect(chans[id]||buses[fam]||master);
      samplers[id]=inst;                 // stessa interfaccia .triggerAttackRelease
    }
    // coro: le 5 voci puntano allo stesso strumento "choir-aah" del manifest
    ["soprani","contralti","tenori","baritoni","bassicoro"].forEach(id=>{
      const inst = bank["choir-aah"];
      if(inst){ inst.connect(chans[id]||buses.coro); samplers[id]=inst; }
    });
    samplesReady=true; samplesLoading=false;
    Object.keys(samplers).forEach(id=>applyMix(id));
    sampStatus("campioni pronti"); return true;
  }catch(e){ samplesLoading=false; samplers={};
    sampStatus("caricamento non riuscito \u2014 uso la sintesi"); return false; }
}
```

> Nota sul coro: nel `SAMPLE_MAP` aggiungi (o lascia gestire al blocco coro qui sopra)
> il fatto che le 5 voci condividono `choir-aah`. Se vuoi timbri distinti per voce,
> crea nel manifest `choir-soprano`, `choir-alto`, ecc. e mappa di conseguenza.

## 3. Round-robin e layer dinamici

Sono trasparenti per l'app: `samplers[id].triggerAttackRelease(note, dur, time, vel)`
sceglie da solo il layer in base alla `vel` e alterna le varianti round-robin. Il
codice di `playEnsemble` / `playNoiseEnsemble` non cambia.

## 4. Offline / kiosk

Registra il service worker una volta sola nella pagina dell'app:

```js
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register(
    "https://cdn.jsdelivr.net/gh/TUO-UTENTE/orchestra-samples/sw/orchestra-sw.js",
    { scope: "./" }
  );
}
```

Al primo avvio con rete la cache si popola; agli avvii successivi i campioni sono
serviti offline. Per i kiosk, esegui una volta un "giro" che tocchi tutti gli
strumenti cosi' da scaricare tutto in anticipo.

## 5. Caricamento selettivo (lazy)

Per non scaricare tutto subito:

```js
const bank = await OrchestraSamples.load(SAMPLES_MANIFEST, { only: ["violin","cello","choir-aah"] });
```

Carica gli altri strumenti quando servono (es. alla prima riproduzione che li usa).
