/*!
 * orchestra-samples — loader per librerie multicampione con Tone.js
 * Espone window.OrchestraSamples. Richiede Tone.js gia' caricato.
 *
 * Concetti:
 *  - ogni strumento = 1+ "layer" dinamici (velocity layers), ciascuno un Tone.Sampler
 *  - trigger instradato al layer in base alla velocity (piano/mezzoforte/forte...)
 *  - round-robin opzionale: se una nota ha piu' file, si alternano ad ogni colpo
 *    (elimina l'effetto "mitragliatrice" sulle note ripetute)
 *
 * Formato del manifest: vedi README.md e manifest.json.
 */
(function (global) {
  "use strict";

  function firstDefined() {
    for (var i = 0; i < arguments.length; i++) if (arguments[i] != null) return arguments[i];
    return undefined;
  }

  // Wrapper che espone la stessa interfaccia di un Tone.Sampler (.connect / .triggerAttackRelease)
  function SampledInstrument(name) {
    this.name = name;
    this.layers = [];        // [{lo, hi, samplers:[Tone.Sampler,...]}]
    this._rr = {};           // contatori round-robin per nota
    this.loaded = false;
    this.release = 1;
    this._out = null;
  }
  SampledInstrument.prototype.connect = function (node) {
    this._out = node;
    this.layers.forEach(function (L) { L.samplers.forEach(function (s) { s.connect(node); }); });
    return this;
  };
  SampledInstrument.prototype._pickLayer = function (vel) {
    for (var i = 0; i < this.layers.length; i++) {
      var L = this.layers[i];
      if (vel >= L.lo && vel <= L.hi) return L;
    }
    return this.layers[this.layers.length - 1] || null;
  };
  SampledInstrument.prototype.triggerAttackRelease = function (note, dur, time, vel) {
    if (vel == null) vel = 0.8;
    var L = this._pickLayer(vel);
    if (!L) return;
    var s;
    if (L.samplers.length > 1) {
      var k = String(note);
      var i = (this._rr[k] || 0) % L.samplers.length;
      this._rr[k] = i + 1;
      s = L.samplers[i];
    } else {
      s = L.samplers[0];
    }
    s.triggerAttackRelease(note, dur, time, vel);
  };
  SampledInstrument.prototype.dispose = function () {
    this.layers.forEach(function (L) {
      L.samplers.forEach(function (s) { try { s.dispose(); } catch (e) {} });
    });
    this.layers = [];
    this.loaded = false;
  };

  function buildInstrument(name, def, globalBase, globalExt) {
    var inst = new SampledInstrument(name);
    inst.release = firstDefined(def.release, 1);
    var base = firstDefined(def.baseUrl, globalBase, "");
    var ext = firstDefined(def.ext, globalExt, "");            // es. ".ogg"; vuoto se i file sono gia' completi nel map
    var layers = def.layers || [{ map: def.map || {} }];

    layers.forEach(function (layer) {
      var lo = layer.velRange ? layer.velRange[0] : 0;
      var hi = layer.velRange ? layer.velRange[1] : 1;
      // quante varianti round-robin al massimo su questo layer?
      var rr = 1;
      Object.keys(layer.map).forEach(function (nt) {
        var v = layer.map[nt];
        if (Array.isArray(v) && v.length > rr) rr = v.length;
      });
      var samplers = [];
      for (var r = 0; r < rr; r++) {
        var urls = {};
        Object.keys(layer.map).forEach(function (nt) {
          var v = layer.map[nt];
          var file = Array.isArray(v) ? v[Math.min(r, v.length - 1)] : v;
          urls[nt] = file + ext;
        });
        samplers.push(new Tone.Sampler({ urls: urls, baseUrl: base, release: inst.release }));
      }
      inst.layers.push({ lo: lo, hi: hi, samplers: samplers });
    });
    return inst;
  }

  var OrchestraSamples = {
    /**
     * Carica un manifest e restituisce { instrumentName: SampledInstrument, ... }.
     * opts.baseUrl / opts.format sovrascrivono i valori del manifest.
     * opts.only = ["violin","cello"] per caricare solo alcuni strumenti (lazy).
     */
    load: function (manifestUrl, opts) {
      opts = opts || {};
      return fetch(manifestUrl)
        .then(function (r) { if (!r.ok) throw new Error("manifest " + r.status); return r.json(); })
        .then(function (man) {
          var base = firstDefined(opts.baseUrl, man.baseUrl, "");
          var ext = firstDefined(opts.format ? "." + opts.format.replace(/^\./, "") : null, man.ext, "");
          var only = opts.only ? new Set(opts.only) : null;
          var out = {};
          Object.keys(man.instruments).forEach(function (name) {
            if (only && !only.has(name)) return;
            out[name] = buildInstrument(name, man.instruments[name], base, ext);
          });
          return Tone.loaded().then(function () {
            Object.keys(out).forEach(function (n) { out[n].loaded = true; });
            return out;
          });
        });
    },
    SampledInstrument: SampledInstrument
  };

  global.OrchestraSamples = OrchestraSamples;
})(typeof window !== "undefined" ? window : this);
