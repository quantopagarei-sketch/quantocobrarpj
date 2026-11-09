/* Arquivo de Clientes — interface. Guarda tudo no próprio aparelho (IndexedDB). */
(function () {
  'use strict';
  var C = window.ArqCore, P = C.Phone;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  function h(tag, attrs) {
    var el = document.createElement(tag), kids = Array.prototype.slice.call(arguments, 2);
    if (attrs) for (var k in attrs) {
      var v = attrs[k];
      if (v == null || v === false) continue;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k.slice(0, 2) === 'on' && typeof v === 'function') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : v);
    }
    (function add(list) {
      list.forEach(function (c) {
        if (c == null || c === false) return;
        if (Array.isArray(c)) return add(c);
        el.appendChild(c.nodeType ? c : document.createTextNode(String(c)));
      });
    })(kids);
    return el;
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  var MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  function fDate(ts) { var d = new Date(ts); return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear(); }
  function fShort(ts) {
    if (!ts) return '';
    var d = new Date(ts), now = new Date();
    if (d.toDateString() === now.toDateString()) return pad(d.getHours()) + ':' + pad(d.getMinutes());
    if (d.getFullYear() === now.getFullYear()) return pad(d.getDate()) + ' ' + MESES[d.getMonth()];
    return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + String(d.getFullYear()).slice(2);
  }
  function fTime(ts) { var d = new Date(ts); return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function fDay(ts) {
    var d = new Date(ts);
    var dias = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
    return dias[d.getDay()] + ', ' + d.getDate() + ' ' + MESES[d.getMonth()] + ' ' + d.getFullYear();
  }
  function fSize(b) {
    if (!b) return '';
    if (b < 1024) return b + ' B';
    if (b < 1048576) return (b / 1024).toFixed(0) + ' KB';
    if (b < 1073741824) return (b / 1048576).toFixed(1).replace('.', ',') + ' MB';
    return (b / 1073741824).toFixed(2).replace('.', ',') + ' GB';
  }
  function num(n) { return (n || 0).toLocaleString('pt-BR'); }
  function pl(n, one, many) { return num(n) + ' ' + (n === 1 ? one : many); }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function tick() { return new Promise(function (r) { setTimeout(r, 0); }); }

  var toastTimer;
  function toast(msg, ms) {
    var t = $('#toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.hidden = true; }, ms || 3200);
  }

  // ------------------------------------------------------------------ banco local
  var DB = {
    db: null,
    open: function () {
      return new Promise(function (res, rej) {
        var r;
        try { r = indexedDB.open('arquivo-clientes', 2); } catch (e) { return rej(e); }
        r.onupgradeneeded = function (ev) {
          var d = r.result, old = ev.oldVersion || 0, ms;
          if (old < 1) {
            d.createObjectStore('contacts', { keyPath: 'id' });
            ms = d.createObjectStore('messages', { keyPath: 'k' });
            ms.createIndex('cid', ['cid', 'ts', 'seq']);
            d.createObjectStore('blobs', { keyPath: 'id' });
            var ds = d.createObjectStore('docs', { keyPath: 'id' });
            ds.createIndex('cid', 'cid'); ds.createIndex('ts', 'ts');
            d.createObjectStore('meta', { keyPath: 'key' });
          } else ms = r.transaction.objectStore('messages');
          // bk = chave pelo conteúdo (minuto + quem + texto), para achar a mesma mensagem vinda de outra fonte
          if (old < 2) ms.createIndex('bk', 'bk');
        };
        r.onsuccess = function () { DB.db = r.result; res(); };
        r.onerror = function () { rej(r.error); };
        r.onblocked = function () { rej(new Error('Feche outras abas deste app e recarregue.')); };
      });
    },
    req: function (r) { return new Promise(function (res, rej) { r.onsuccess = function () { res(r.result); }; r.onerror = function () { rej(r.error); }; }); },
    done: function (t) { return new Promise(function (res, rej) { t.oncomplete = function () { res(); }; t.onerror = function () { rej(t.error); }; t.onabort = function () { rej(t.error || new Error('Gravação cancelada (espaço cheio?)')); }; }); },
    tx: function (s, m) { return DB.db.transaction(s, m || 'readonly'); },
    get: function (s, k) { return DB.req(DB.tx(s).objectStore(s).get(k)); },
    getAll: function (s) { return DB.req(DB.tx(s).objectStore(s).getAll()); },
    put: function (s, v) { var t = DB.tx(s, 'readwrite'); t.objectStore(s).put(v); return DB.done(t); },
    del: function (s, k) { var t = DB.tx(s, 'readwrite'); t.objectStore(s).delete(k); return DB.done(t); },
    count: function (s) { return DB.req(DB.tx(s).objectStore(s).count()); },
    range: function (cid) { return IDBKeyRange.bound([cid, -Infinity, -Infinity], [cid, Infinity, Infinity]); },
    messagesOf: function (cid) { return DB.req(DB.tx('messages').objectStore('messages').index('cid').getAll(DB.range(cid))); },
    docsOf: function (cid) { return DB.req(DB.tx('docs').objectStore('docs').index('cid').getAll(cid)); },
    countOf: function (cid) { return DB.req(DB.tx('messages').objectStore('messages').index('cid').count(DB.range(cid))); },
    edge: function (cid, dir) {
      return new Promise(function (res, rej) {
        var r = DB.tx('messages').objectStore('messages').index('cid').openCursor(DB.range(cid), dir);
        r.onsuccess = function () { res(r.result ? r.result.value : null); }; r.onerror = function () { rej(r.error); };
      });
    },
    lastReal: function (cid) {
      return new Promise(function (res, rej) {
        var r = DB.tx('messages').objectStore('messages').index('cid').openCursor(DB.range(cid), 'prev'), first = null;
        r.onsuccess = function () {
          var c = r.result; if (!c) return res(first);
          if (!first) first = c.value;
          if (!c.value.sys) return res(c.value);
          c.continue();
        };
        r.onerror = function () { rej(r.error); };
      });
    },
    // grava mensagens sem duplicar e sem perder um arquivo já ligado
    upsert: function (list) {
      if (!list.length) return Promise.resolve();
      var t = DB.tx(['messages', 'docs'], 'readwrite'), ms = t.objectStore('messages'), ds = t.objectStore('docs');
      function write(v, oldK) {
        if (oldK && oldK !== v.k) { ms.delete(oldK); ds.delete(oldK); }
        ms.put(v);
        if (v.m && (v.ty === 'doc' || v.ty === 'image')) ds.put(docOf(v));
      }
      list.forEach(function (m) {
        var r = ms.get(m.k);
        r.onsuccess = function () {
          if (r.result) return write(mergeMsg(r.result, m));
          if (!m.bk) return write(m);
          var r2 = ms.index('bk').get(m.bk);
          r2.onsuccess = function () {
            var ex = r2.result;
            if (!ex || (stableKey(ex.k) && stableKey(m.k))) return write(m);
            var v = mergeMsg(ex, m);
            if (stableKey(m.k) && !stableKey(ex.k)) { v.k = m.k; return write(v, ex.k); }
            write(v);
          };
        };
      });
      return DB.done(t);
    },
    each: function (store, fn) {
      return new Promise(function (res, rej) {
        var r = DB.tx(store).objectStore(store).openCursor();
        r.onsuccess = function () { var c = r.result; if (!c) return res(); if (fn(c.value) === false) return res(); c.continue(); };
        r.onerror = function () { rej(r.error); };
      });
    },
    clear: function () {
      var names = ['contacts', 'messages', 'blobs', 'docs', 'meta'], t = DB.tx(names, 'readwrite');
      names.forEach(function (n) { t.objectStore(n).clear(); });
      return DB.done(t);
    }
  };
  function stableKey(k) { return String(k).indexOf('|w:') > 0; }
  function mergeMsg(ex, m) {
    var v = Object.assign({}, ex);
    // backup novo da mesma mensagem: vale o texto editado e o caminho novo do arquivo (sem perder o arquivo já guardado)
    var newer = (ex.src || []).indexOf('bkp') >= 0 && (m.src || []).indexOf('bkp') >= 0 && m.ty !== 'deleted';
    if (newer) {
      if (m.t) v.t = m.t;
      if (m.ty) v.ty = m.ty;
      if (m.m) { var keepB = ex.m && ex.m.b; v.m = Object.assign({}, ex.m || {}); for (var k0 in m.m) if (m.m[k0] != null && m.m[k0] !== '' && m.m[k0] !== 0) v.m[k0] = m.m[k0]; if (keepB) { v.m.b = keepB; if (ex.m.s) v.m.s = ex.m.s; } }
    }
    if (!v.bk && m.bk) v.bk = m.bk;
    if (!v.t && m.t) v.t = m.t;
    if (v.a == null && m.a != null) v.a = m.a;
    if (v.ap == null && m.ap != null) v.ap = m.ap;
    if (m.m) {
      var mm = Object.assign({}, ex.m || {});
      for (var k in m.m) { var nv = m.m[k]; if (nv == null || nv === '' || nv === 0) continue; if (mm[k] == null || mm[k] === '' || mm[k] === 0) mm[k] = nv; }
      v.m = mm;
    }
    if ((ex.ty === 'omitted' || ex.ty === 'text') && m.ty && m.ty !== 'omitted' && m.ty !== 'text') v.ty = m.ty;
    var src = (ex.src || []).slice();
    (m.src || []).forEach(function (s) { if (src.indexOf(s) < 0) src.push(s); });
    v.src = src;
    if (m.notes) v.notes = m.notes;
    return v;
  }
  function docOf(v) { return { id: v.k, cid: v.cid, ts: v.ts, me: v.me, ty: v.ty, n: v.m.n, o: v.m.o || '', mi: v.m.mi || '', s: v.m.s || 0, b: v.m.b || null }; }

  // ------------------------------------------------------------------ estado
  var S = {
    contacts: [], byId: {}, settings: { myNames: '', media: { image: true, audio: false, video: false, sticker: false } },
    learnedMe: {}, view: 'clientes', open: null, docFilter: 'pdf', q: '', listLimit: 200, docLimit: 120,
    urls: [], busy: false, storageOk: true
  };
  var AVC = ['#00a884', '#53bdeb', '#e26ab6', '#e0803e', '#7f66ff', '#c9a227', '#5b8def', '#d1495b', '#3d9970', '#8e6e53'];
  function avatar(c, big) {
    var nm = c.name || '', ini = c.isGroup ? '👥' : (nm.replace(/[^A-Za-zÀ-ÿ ]/g, ' ').trim().split(/\s+/).filter(Boolean).slice(0, 2).map(function (w) { return w.charAt(0).toUpperCase(); }).join('') || '#');
    var hh = 0, id = String(c.id); for (var i = 0; i < id.length; i++) hh = (hh * 31 + id.charCodeAt(i)) >>> 0;
    return h('span', { class: 'av' + (big ? ' big' : ''), style: 'background:' + AVC[hh % AVC.length], 'aria-hidden': 'true' }, ini);
  }
  function label(c) { return c.name || (c.phone ? P.format(c.phone) : (c.isGroup ? 'Grupo' : 'Contato sem número')); }
  function indexContact(c) { S.byId[c.id] = c; }
  function phoneIndex() {
    var m = {};
    S.contacts.forEach(function (c) { if (c.phone) m[P.key(c.phone)] = c; });
    return m;
  }
  function nameForPhone(d) {
    if (!d) return null;
    var k = P.key(d);
    for (var i = 0; i < S.contacts.length; i++) { var c = S.contacts[i]; if (c.phone && c.name && P.key(c.phone) === k) return c.name; }
    return null;
  }
  async function saveContact(c) { c.updated = Date.now(); await DB.put('contacts', c); }
  async function loadAll() {
    S.contacts = await DB.getAll('contacts');
    S.byId = {}; S.contacts.forEach(indexContact);
    var st = await DB.get('meta', 'settings'); if (st && st.v) S.settings = Object.assign(S.settings, st.v);
    var lm = await DB.get('meta', 'learnedMe'); if (lm && lm.v) S.learnedMe = lm.v;
  }
  async function saveSettings() { await DB.put('meta', { key: 'settings', v: S.settings }); }
  function meFolded() {
    var out = {};
    String(S.settings.myNames || '').split(/[,;\n]/).forEach(function (n) { n = C.fold(n); if (n) out[n] = 1; });
    Object.keys(S.learnedMe).forEach(function (n) { if (S.learnedMe[n] >= 1) out[n] = 1; });
    return out;
  }
  async function learnMe(names) {
    if (!names || !names.length) return;
    names.forEach(function (n) { var f = C.fold(n); if (f) S.learnedMe[f] = (S.learnedMe[f] || 0) + 1; });
    await DB.put('meta', { key: 'learnedMe', v: S.learnedMe });
  }

  // ------------------------------------------------------------------ onde o app está rodando
  var Plat = {
    framed: !!(window.claude && typeof window.claude.use === 'function'),
    downloads: null,
    init: function () {
      if (!Plat.framed) return;
      try { window.claude.use('downloads').then(function (d) { Plat.downloads = d; }).catch(function () { }); } catch (e) { }
    },
    save: async function (blob, filename) {
      if (Plat.framed) {
        if (!Plat.downloads) { try { Plat.downloads = await window.claude.use('downloads'); } catch (e) { } }
        if (!Plat.downloads) { toast('Este visualizador não permite salvar arquivos. Abra o app no navegador.'); return false; }
        try { await Plat.downloads.save({ filename: filename, data: blob }); return true; }
        catch (e) {
          if (e && e.code === 'declined') return false;
          if (e && e.code === 'rejected_extension') { toast('Este tipo de arquivo não pode ser salvo por aqui.'); return false; }
          if (e && e.code === 'too_large') { toast('Arquivo grande demais para salvar por aqui. Abra o app no navegador do computador.'); return false; }
          toast('Não deu para salvar: ' + ((e && e.message) || 'erro desconhecido')); return false;
        }
      }
      var url = URL.createObjectURL(blob), a = h('a', { href: url, download: filename });
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 120000);
      return true;
    },
    canShare: function (file) { try { return !Plat.framed && !!navigator.canShare && navigator.canShare({ files: [file] }); } catch (e) { return false; } },
    share: async function (blob, name) {
      var f = new File([blob], name, { type: blob.type || C.mimeOf(name) });
      try { await navigator.share({ files: [f], title: name }); } catch (e) { if (e && e.name !== 'AbortError') toast('Não deu para enviar: ' + e.message); }
    },
    open: function (blob) { if (Plat.framed) return false; var u = URL.createObjectURL(blob); window.open(u, '_blank'); setTimeout(function () { URL.revokeObjectURL(u); }, 300000); return true; }
  };

  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement('script'); s.src = src; s.async = true;
      s.onload = function () { res(); }; s.onerror = function () { rej(new Error('Não carregou ' + src)); };
      (document.head || document.documentElement).appendChild(s);
    });
  }
  var sqlP = null, pdfP = null;
  function loadSql() {
    if (!sqlP) sqlP = (async function () {
      try {
        await loadScript('lib/sql-wasm.js');
        return await window.initSqlJs({ locateFile: function (f) { return 'lib/' + f; } });
      } catch (e) {
        console.warn('sql.js wasm indisponível, usando versão JS', e);
        window.initSqlJs = undefined;
        await loadScript('lib/sql-asm-memory-growth.js');
        return await window.initSqlJs();
      }
    })();
    sqlP.catch(function () { sqlP = null; });
    return sqlP;
  }
  function loadPdf() {
    if (!pdfP) pdfP = loadScript('lib/pdf.min.js').then(function () {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'lib/pdf.worker.min.js';
      return window.pdfjsLib;
    });
    pdfP.catch(function () { pdfP = null; });
    return pdfP;
  }

  // ------------------------------------------------------------------ contatos: criar, juntar, estatísticas
  function findByPhone(d) {
    if (!d) return null;
    var k = P.key(d);
    for (var i = 0; i < S.contacts.length; i++) { var c = S.contacts[i]; if (c.phone && P.key(c.phone) === k) return c; }
    return null;
  }
  async function upsertContact(info) {
    var c = info.phone ? findByPhone(info.phone) : null;
    if (!c) c = S.byId[info.id];
    if (!c) for (var i = 0; i < S.contacts.length && !c; i++) if ((S.contacts[i].aliases || []).indexOf(info.id) >= 0) c = S.contacts[i];
    if (!c) {
      c = { id: info.id, name: info.name || null, phone: info.phone || null, isGroup: !!info.isGroup, notes: '', status: '', nameSrc: info.nameSrc || '', created: Date.now(), st: {} };
      if (info.lid) c.lid = true;
      S.contacts.push(c); indexContact(c);
    } else {
      if (!c.name && info.name) { c.name = info.name; c.nameSrc = info.nameSrc || ''; }
      if (!c.phone && info.phone) c.phone = info.phone;
      if (info.isGroup) c.isGroup = true;
    }
    await saveContact(c);
    return c;
  }
  async function refreshStats(ids) {
    for (var i = 0; i < ids.length; i++) {
      var c = S.byId[ids[i]]; if (!c) continue;
      var n = await DB.countOf(c.id);
      var first = await DB.edge(c.id, 'next'), last = await DB.lastReal(c.id);
      var docs = await DB.docsOf(c.id);
      c.st = {
        n: n, first: first ? first.ts : 0, last: last ? last.ts : 0,
        docs: docs.filter(function (d) { return d.ty === 'doc'; }).length,
        pdf: docs.filter(function (d) { return d.ty === 'doc' && /pdf$/i.test(d.n); }).length,
        snip: last ? snippet(last) : ''
      };
      await saveContact(c);
    }
  }
  function snippet(m) {
    var who = m.me ? 'Você: ' : '';
    if (m.m) return who + (m.ty === 'doc' ? '📄 ' : '') + (m.m.n || 'arquivo');
    if (m.ty === 'deleted') return who + 'mensagem apagada';
    if (m.ty === 'omitted') return who + 'mídia';
    return who + (m.t || '').replace(/\s+/g, ' ').slice(0, 120);
  }
  function addAlias(c, id) { if (!id || id === c.id) return; c.aliases = c.aliases || []; if (c.aliases.indexOf(id) < 0) c.aliases.push(id); }
  function rekey(cid, k) { k = String(k); return cid + '|' + k.slice(k.indexOf('|') + 1); }
  // move tudo de um contato para outro (ex.: o mesmo cliente veio pelo nome e pelo número)
  async function mergeContacts(fromId, toId) {
    if (fromId === toId) return;
    var from = S.byId[fromId], to = S.byId[toId]; if (!from || !to) return;
    var msgs = await DB.messagesOf(fromId);
    var moved = msgs.map(function (m) { var v = Object.assign({}, m); v.cid = toId; v.k = rekey(toId, m.k); if (m.bk) v.bk = rekey(toId, m.bk); return v; });
    for (var i = 0; i < moved.length; i += 1000) await DB.upsert(moved.slice(i, i + 1000));
    var t = DB.tx(['messages', 'docs'], 'readwrite');
    msgs.forEach(function (m) { t.objectStore('messages').delete(m.k); t.objectStore('docs').delete(m.k); });
    await DB.done(t);
    if (from.name && (from.nameSrc === 'manual' || !to.name)) { to.name = from.name; to.nameSrc = from.nameSrc; }
    addAlias(to, fromId); (from.aliases || []).forEach(function (a) { addAlias(to, a); });
    if (!to.phone && from.phone) to.phone = from.phone;
    if (from.notes) to.notes = to.notes ? to.notes + '\n\n' + from.notes : from.notes;
    if (!to.status && from.status) to.status = from.status;
    await DB.del('contacts', fromId);
    S.contacts = S.contacts.filter(function (c) { return c.id !== fromId; });
    delete S.byId[fromId];
    await saveContact(to);
    await refreshStats([toId]);
    if (S.open === fromId) S.open = toId;
  }
  async function setPhone(c, raw) {
    var d = raw ? P.normalize(raw) : null;
    if (raw && !d) { toast('Número inválido. Use DDD + número, ex.: 11 98765-4321'); return false; }
    var other = d ? findByPhone(d) : null;
    c.phone = d;
    await saveContact(c);
    if (other && other.id !== c.id) { await mergeContacts(c.id, other.id); toast('Juntei com a outra conversa deste número.'); }
    return true;
  }
  var seedP = Promise.resolve();
  async function removeDemo() {
    await seedP;
    var demo = S.contacts.filter(function (c) { return c.demo; });
    if (!demo.length) return;
    for (var i = 0; i < demo.length; i++) {
      var msgs = await DB.messagesOf(demo[i].id), t = DB.tx(['messages', 'docs', 'blobs', 'contacts'], 'readwrite');
      msgs.forEach(function (m) { t.objectStore('messages').delete(m.k); t.objectStore('docs').delete(m.k); if (m.m && m.m.b) t.objectStore('blobs').delete(m.m.b); });
      t.objectStore('contacts').delete(demo[i].id);
      await DB.done(t);
    }
    S.contacts = S.contacts.filter(function (c) { return !c.demo; });
    S.byId = {}; S.contacts.forEach(indexContact);
    if (S.open && !S.byId[S.open]) S.open = null;
  }

  // ------------------------------------------------------------------ arquivos guardados
  function allowedKind(ty) {
    if (ty === 'doc' || ty === 'contact') return true;
    var m = S.settings.media || {};
    return !!m[ty];
  }
  async function saveBlob(cid, name, blob, mime) {
    var id = 'b:' + C.hash(cid + '|' + String(name).toLowerCase() + '|' + blob.size);
    var ex = await DB.get('blobs', id);
    if (!ex) {
      var b = blob.type === mime || !mime ? blob : new Blob([blob], { type: mime });
      await DB.put('blobs', { id: id, blob: b, n: name, mi: mime || blob.type || '', s: blob.size });
    }
    return id;
  }
  async function hitBlob(found, mime) { return found.entry ? found.zr.blob(found.entry, mime) : found; }
  // .zip da pasta do WhatsApp (ex.: "Compactar" no Meus Arquivos) vira uma lista de arquivos lidos sob demanda
  async function expandZips(files) {
    var out = [], zips = [];
    for (var i = 0; i < files.length; i++) {
      var f = files[i];
      out.push(f); // o próprio .zip pode ser um documento enviado no chat
      // só abre .zip escolhido sozinho (não os que estão dentro de uma pasta escolhida)
      if (/\.zip$/i.test(f.name) && !f.webkitRelativePath) {
        try {
          var zr = new C.ZipReader(f), ents = await zr.open();
          zips.push({ file: f, zr: zr, entries: ents });
          ents.forEach(function (e) { out.push({ name: C.baseName(e.name), path: e.name, size: e.size, entry: e, zr: zr }); });
        } catch (e) { /* não é um .zip legível: fica só como arquivo */ }
      }
    }
    return { items: out, zips: zips };
  }
  async function requestPersist() {
    try { if (navigator.storage && navigator.storage.persist) return await navigator.storage.persist(); } catch (e) { }
    return false;
  }

  // ------------------------------------------------------------------ importação: progresso
  var wake = null;
  async function busyStart(title) {
    if (S.busy) { toast('Espere a importação atual terminar.'); return false; }
    S.busy = true;
    $('#progress').hidden = false; $('#prog-title').textContent = title; $('#log').textContent = ''; setBar(0);
    $$('#v-importar input, #v-importar button').forEach(function (el) { el.disabled = true; });
    try { if (navigator.wakeLock) wake = await navigator.wakeLock.request('screen'); } catch (e) { wake = null; }
    $('#progress').scrollIntoView({ block: 'nearest' });
    return true;
  }
  function busyEnd(title) {
    S.busy = false; setBar(1);
    if (title) $('#prog-title').textContent = title;
    $$('#v-importar input, #v-importar button').forEach(function (el) { el.disabled = false; });
    if (wake) { try { wake.release(); } catch (e) { } wake = null; }
  }
  function log(msg, cls) { var l = $('#log'); l.appendChild(h('div', { class: cls || '' }, msg)); l.scrollTop = l.scrollHeight; }
  function setBar(f) { $('#prog-bar').style.width = Math.max(0, Math.min(100, f * 100)).toFixed(1) + '%'; }
  function errMsg(e) { return (e && e.message) || String(e); }

  // ------------------------------------------------------------------ importar: conversas exportadas
  async function importExports(files) {
    if (S.busy) { toast('Espere a importação atual terminar.'); return; }
    S.busy = true;
    var cands = files.filter(function (f) { return /\.(zip|txt)$/i.test(f.name); });
    var loose = files.filter(function (f) { return !/\.(zip|txt)$/i.test(f.name); });
    // um .txt que não é conversa exportada (ex.: medidas.txt enviado no chat) é tratado como anexo
    var chats = [];
    for (var t = 0; t < cands.length; t++) {
      var cf = cands[t];
      if (/\.txt$/i.test(cf.name)) {
        var head = C.decodeText(new Uint8Array(await cf.slice(0, 16384).arrayBuffer()));
        if (!C.looksLikeExport(head)) { loose.push(cf); continue; }
      }
      chats.push(cf);
    }
    S.busy = false;
    if (!chats.length) { toast('Escolha arquivos .zip ou .txt exportados do WhatsApp.'); return; }
    if (!(await busyStart('Importando ' + chats.length + (chats.length > 1 ? ' arquivos…' : ' arquivo…')))) return;
    await removeDemo(); requestPersist();
    var looseIdx = loose.length ? new C.MediaIndex(loose) : null, touched = {}, okN = 0, convN = 0, msgsN = 0, filesN = 0, errN = 0;
    for (var i = 0; i < chats.length; i++) {
      var f = chats[i];
      setBar(i / chats.length);
      try {
        var rs = await importOneExport(f, looseIdx);
        okN++;
        rs.forEach(function (r) {
          if (r.pkg) return;
          if (r.error) { errN++; log('✗ ' + r.label + ': ' + r.error, 'er'); return; }
          touched[r.cid] = 1; convN++; msgsN += r.n; filesN += r.files;
          log('✓ ' + r.label + ' — ' + pl(r.n, 'mensagem', 'mensagens') + (r.files ? ', ' + pl(r.files, 'arquivo', 'arquivos') : '') + (r.missing ? ' (' + pl(r.missing, 'arquivo não veio', 'arquivos não vieram') + ')' : '') + (r.unsure ? ' — confira quem é você em Ajustes' : ''), 'ok');
          if (r.hidden) log('• ' + pl(r.hidden, 'foto, PDF ou áudio veio', 'fotos, PDFs ou áudios vieram') + ' como “mídia oculta”: a conversa foi exportada sem mídia. Para trazer os arquivos, exporte de novo escolhendo “Incluir mídia” ou use o backup completo (pasta do WhatsApp Business).');
        });
      } catch (e) {
        errN++;
        log('✗ ' + f.name + ': ' + errMsg(e), 'er');
      }
      await tick();
    }
    log('Atualizando a lista…');
    await refreshStats(Object.keys(touched));
    busyEnd('Pronto: ' + pl(convN, 'conversa', 'conversas') + ', ' + pl(msgsN, 'mensagem', 'mensagens') + ', ' + pl(filesN, 'arquivo', 'arquivos') + (errN ? ' (' + pl(errN, 'problema', 'problemas') + ', veja abaixo)' : '') + '.');
    renderAll();
  }
  // Um arquivo pode ser um .txt ou um .zip com uma ou várias conversas
  async function importOneExport(f, looseIdx) {
    if (!/\.zip$/i.test(f.name)) {
      var text = C.decodeText(new Uint8Array(await f.arrayBuffer()));
      return [await importChatText(text, f.name, f.name, null, looseIdx)];
    }
    var zr = new C.ZipReader(f), ents = await zr.open();
    if (ents.some(function (e) { return e.name === 'arquivo.json'; })) { await importPackage(f, true); return [{ pkg: true }]; }
    var txts = ents.filter(function (e) { return /\.txt$/i.test(e.name) && !/(^|\/)__MACOSX\//.test(e.name); });
    var chatsIn = [];
    for (var i = 0; i < txts.length; i++) {
      var tx = await zr.text(txts[i]);
      if (C.looksLikeExport(tx)) chatsIn.push({ e: txts[i], text: tx });
    }
    if (!chatsIn.length) throw new Error('não achei nenhuma conversa exportada dentro do .zip');
    var chosen = chatsIn.map(function (c) { return c.e; });
    var zidx = new C.MediaIndex(ents.filter(function (e) { return chosen.indexOf(e) < 0; }).map(function (e) { return { name: C.baseName(e.name), path: e.name, size: e.size, entry: e, zr: zr }; }));
    var out = [];
    for (var j = 0; j < chatsIn.length; j++) {
      var ci = chatsIn[j];
      // "_chat.txt" não diz o nome: usa o nome do .zip (só quando o .zip tem uma conversa)
      var fallback = chatsIn.length === 1 ? f.name : ci.e.name;
      try { out.push(await importChatText(ci.text, ci.e.name, fallback, zidx, looseIdx)); }
      catch (e) { out.push({ error: errMsg(e), label: ci.e.name }); }
    }
    return out;
  }
  async function importChatText(text, txtName, fallbackName, zidx, looseIdx) {
    var parsed = C.parseExportText(text, { fileName: txtName });
    if (!parsed.title) parsed.title = C.titleFromFileName(fallbackName);
    if (!parsed.format || !parsed.messages.length) throw new Error('não reconheci o formato desta conversa');
    var who = C.identifyExport(parsed, meFolded(), fallbackName);
    await learnMe(who.inferredMe);
    var c = await upsertContact({ id: who.id, name: who.name, phone: who.phone, isGroup: who.isGroup, nameSrc: 'export' });
    var keyer = C.makeKeyer(c.id), meF = meFolded();
    var out = [], files = 0, missing = 0, hidden = 0;
    for (var j = 0; j < parsed.messages.length; j++) {
      var pm = parsed.messages[j];
      if (pm.kind === 'omitted') hidden++;
      var me = pm.author && pm.author !== who.other && (who.me[pm.author] || meF[C.fold(pm.author)]) ? 1 : 0;
      var rec = { cid: c.id, ts: pm.ts, seq: pm.seq, me: me, a: (me || pm.sys) ? null : pm.author, t: pm.text || '', ty: pm.kind, sys: pm.sys || 0, ed: pm.edited || 0, src: ['exp'] };
      if (pm.media) {
        var disp = C.displayFileName(pm.media.name);
        rec.m = { n: disp, p: pm.media.name, mi: C.mimeOf(disp) };
        var found = pm.kind === 'omitted' ? null : ((zidx && zidx.find({ name: pm.media.name })) || (looseIdx && looseIdx.find({ name: pm.media.name })));
        if (found && allowedKind(rec.ty)) {
          try { var blob = await hitBlob(found, rec.m.mi); rec.m.s = blob.size; rec.m.b = await saveBlob(c.id, disp, blob, rec.m.mi); files++; }
          catch (e) { missing++; }
        } else if (found) rec.m.s = found.size;
        else missing++;
        if (pm.kind === 'omitted') rec.ty = C.kindOf(disp);
      }
      rec.k = rec.bk = keyer(rec.ts, rec.me, rec.t, rec.m && rec.m.n, pm.kind);
      out.push(rec);
      if (out.length >= 1000) { await DB.upsert(out); out = []; }
    }
    await DB.upsert(out);
    var unsure = !who.isGroup && !who.other && !Object.keys(who.me).length && Object.keys(parsed.authors).length > 1;
    return { cid: c.id, label: label(c), n: parsed.messages.length, files: files, missing: missing, unsure: unsure, hidden: hidden };
  }

  // ------------------------------------------------------------------ importar: backup completo (crypt15)
  async function importBackup(file, keyText, mediaFiles) {
    if (!file) { toast('Escolha o arquivo msgstore.db.crypt15.'); return; }
    if (!(await busyStart('Abrindo o backup…'))) return;
    await removeDemo(); requestPersist();
    try {
      var src = file, extra = [];
      if (/\.zip$/i.test(file.name)) {
        log('Abrindo o .zip ' + file.name + ' (' + fSize(file.size) + ')…');
        var ex = await expandZips([file]);
        if (!ex.zips.length) throw new Error('Não consegui abrir este .zip. Ele pode estar incompleto: baixe ou copie de novo.');
        var ents = ex.zips[0].entries;
        var cands = ents.filter(function (e) { return /(^|\/)msgstore\.db\.crypt15$/i.test(e.name); });
        if (!cands.length) cands = ents.filter(function (e) { return /(^|\/)msgstore-\d{4}-\d{2}-\d{2}\.\d+\.db\.crypt15$/i.test(e.name); }).sort(function (a, b) { return C.baseName(b.name).localeCompare(C.baseName(a.name)); });
        if (!cands.length) cands = ents.filter(function (e) { return /(^|\/)msgstore\.db$/i.test(e.name); });
        if (!cands.length) {
          if (ents.some(function (e) { return /msgstore.*\.crypt14$/i.test(e.name); })) throw new Error('O .zip só tem backup .crypt14 (o tipo antigo). No S22, ative o backup com chave de 64 dígitos, toque em Fazer backup e compacte a pasta de novo.');
          throw new Error('Não achei o msgstore.db.crypt15 dentro do .zip. Compacte a pasta “WhatsApp Business” inteira (ela tem a subpasta Databases).');
        }
        var pick = cands[0];
        log('Usando ' + pick.name);
        src = await ex.zips[0].zr.blob(pick, 'application/octet-stream');
        extra = ex.items.filter(function (it) { return /(^|\/)Media\//i.test(it.path); });
        log(num(extra.length) + ' arquivos de mídia dentro do .zip.');
      }
      log('Lendo ' + (src.name || 'backup') + ' (' + fSize(src.size) + ')…');
      var buf = new Uint8Array(await src.arrayBuffer());
      log('Abrindo com a chave…');
      var res = await C.decryptCrypt15(buf, keyText);
      buf = null;
      if (res.zip) throw new Error('Este é um backup parcial (incremental ou de outra parte). Escolha o msgstore.db.crypt15, sem “increment” no nome.');
      if (res.info && res.info.appVersion) log('Backup do WhatsApp ' + res.info.appVersion + (res.info.phoneEnd ? ', número terminado em ' + res.info.phoneEnd : ''), 'ok');
      log('Carregando o leitor do banco…');
      var SQL = await loadSql();
      var cur = C.openMsgStore(SQL, res.sqlite);
      res = null;
      log('Encontrei ' + num(cur.chats.length) + ' conversas. Gravando…', 'ok');
      var map = {}, chatById = {};
      cur.chats.forEach(function (ch) { chatById[ch.id] = ch; });
      async function contactFor(chatId) {
        if (map[chatId]) return map[chatId];
        var ch = chatById[chatId];
        var c = await upsertContact({ id: ch.id, phone: ch.phone, name: ch.isGroup ? (ch.subject || 'Grupo') : null, isGroup: ch.isGroup, lid: ch.lid, nameSrc: ch.isGroup ? 'backup' : '' });
        return (map[chatId] = c.id);
      }
      var mlist = (mediaFiles || []).length ? (await expandZips(mediaFiles)).items : [];
      mlist = mlist.concat(extra);
      var idx = mlist.length ? new C.MediaIndex(mlist) : null;
      var keyers = {}, total = cur.total || 1, n = 0, files = 0, missing = 0, bad = 0, b;
      try {
        while ((b = cur.next())) {
          var out = [];
          for (var j = 0; j < b.length; j++) {
            var m = b[j], cid = await contactFor(m.chatId);
            var rec = { cid: cid, ts: m.ts, seq: m.seq, me: m.me, a: null, t: m.text || '', ty: m.kind, sys: 0, src: ['bkp'] };
            if (m.authorPhone) { rec.ap = m.authorPhone; }
            if (m.media) {
              rec.m = { n: m.media.name || m.media.orig || 'arquivo', p: m.media.path || '', mi: m.media.mime || C.mimeOf(m.media.name), s: m.media.size || 0 };
              if (m.media.orig && m.media.orig !== rec.m.n) rec.m.o = m.media.orig;
              var fnd = idx && idx.find(m.media);
              if (fnd && allowedKind(rec.ty)) {
                try { rec.m.b = await saveBlob(cid, rec.m.n, await hitBlob(fnd, rec.m.mi), rec.m.mi); if (!rec.m.s) rec.m.s = fnd.size; files++; }
                catch (e) { bad++; missing++; if (bad <= 5) log('• Não consegui ler ' + rec.m.n + ' (' + errMsg(e) + '). Sigo com o resto.'); }
              }
              else if (!fnd && (rec.ty === 'doc' || allowedKind(rec.ty))) missing++;
            }
            var kf = keyers[cid] || (keyers[cid] = C.makeKeyer(cid));
            rec.bk = kf(rec.ts, rec.me, rec.t, rec.m && rec.m.n, rec.ty);
            rec.k = m.keyId ? cid + '|w:' + (m.me ? 1 : 0) + ':' + m.keyId : rec.bk;
            out.push(rec);
          }
          await DB.upsert(out);
          n += b.length;
          setBar(cur.read / total);
          $('#prog-title').textContent = 'Gravando mensagens… ' + num(cur.read) + ' de ' + num(total);
          await tick();
        }
      } finally { cur.close(); }
      log('✓ ' + num(n) + ' mensagens gravadas' + (files ? ', ' + num(files) + ' arquivos ligados' : ''), 'ok');
      if (missing) log('• ' + pl(missing, 'arquivo ainda sem ligação', 'arquivos ainda sem ligação') + '. Use “Ligar PDFs e fotos que faltaram” com a pasta Media do S22.');
      if (idx && idx.sizeMismatch) log('• ' + pl(idx.sizeMismatch, 'arquivo tem', 'arquivos têm') + ' o mesmo nome de uma mensagem mas outro tamanho; por segurança não foram ligados (podem ser de outra conversa).');
      log('Atualizando a lista…');
      await refreshStats(Object.keys(map).map(function (k) { return map[k]; }));
      setBar(1);
      busyEnd('Pronto: ' + pl(Object.keys(map).length, 'conversa importada', 'conversas importadas') + '.');
      $('#k-backup').value = ''; updateKeyCount();
    } catch (e) {
      log('✗ ' + errMsg(e), 'er');
      busyEnd('Não deu certo. Veja a mensagem abaixo.');
    }
    renderAll();
  }

  // ------------------------------------------------------------------ ligar arquivos soltos às mensagens
  async function linkMedia(files) {
    if (!files.length) return;
    if (!(await busyStart('Procurando os arquivos nas conversas…'))) return;
    var done = 0, bad = 0, touched = {}, idx = null;
    try {
      var items = (await expandZips(files)).items;
      idx = new C.MediaIndex(items);
      var todo = [];
      await DB.each('messages', function (m) { if (m.m && !m.m.b) todo.push(m); });
      log(pl(todo.length, 'mensagem', 'mensagens') + ' com arquivo faltando.');
      for (var i = 0; i < todo.length; i++) {
        var m = todo[i];
        if (!allowedKind(m.ty)) continue;
        var f = idx.find({ name: m.m.p ? C.baseName(m.m.p) : m.m.n, path: m.m.p, size: m.m.s, orig: m.m.o });
        if (!f && m.m.n && m.m.p && C.baseName(m.m.p) !== m.m.n) f = idx.find({ name: m.m.n, size: m.m.s });
        if (!f) continue;
        try {
          var v = Object.assign({}, m); v.m = Object.assign({}, m.m);
          v.m.b = await saveBlob(m.cid, v.m.n, await hitBlob(f, v.m.mi || C.mimeOf(v.m.n)), v.m.mi || C.mimeOf(v.m.n)); if (!v.m.s) v.m.s = f.size;
          await DB.upsert([v]);
          done++; touched[m.cid] = 1;
        } catch (e) { bad++; if (bad <= 5) log('• Não consegui ler ' + m.m.n + ' (' + errMsg(e) + ').'); }
        if (i % 50 === 0) { setBar(i / todo.length); await tick(); }
      }
      await refreshStats(Object.keys(touched));
      log('✓ ' + pl(done, 'arquivo ligado', 'arquivos ligados') + ' às conversas.', 'ok');
      if (idx.sizeMismatch) log('• ' + pl(idx.sizeMismatch, 'arquivo tem', 'arquivos têm') + ' o nome certo mas outro tamanho; por segurança não foram ligados.');
      busyEnd('Pronto: ' + pl(done, 'arquivo encontrado', 'arquivos encontrados') + '.');
    } catch (e) {
      log('✗ ' + errMsg(e), 'er');
      busyEnd('Não deu certo. Veja a mensagem abaixo.');
    }
    renderAll();
  }

  // ------------------------------------------------------------------ nomes pelo .vcf
  async function importVcf(file) {
    if (!(await busyStart('Lendo contatos…'))) return;
    try {
      var cards = C.parseVcf(C.decodeText(new Uint8Array(await file.arrayBuffer())));
      log(num(cards.length) + ' contatos com telefone no arquivo.');
      var byKey = {}, byName = {};
      cards.forEach(function (cd) { cd.phones.forEach(function (p) { byKey[P.key(p)] = cd; }); if (cd.name) byName[C.fold(cd.name)] = cd; });
      var named = 0, linked = 0, merges = [];
      S.contacts.slice().forEach(function (c) {
        if (c.isGroup) return;
        if (c.phone) {
          var cd = byKey[P.key(c.phone)];
          if (cd && cd.name && (!c.name || c.nameSrc === 'backup' || P.looksLike(c.name)) && c.nameSrc !== 'manual') { c.name = cd.name; c.nameSrc = 'vcf'; named++; }
        } else if (c.name) {
          var cn = byName[C.fold(c.name)];
          if (cn && cn.phones.length) {
            // escolhe o número certo: primeiro um que já tem conversa aqui, depois um celular, depois o primeiro
            var o = null, pick = null;
            cn.phones.forEach(function (ph) { if (o) return; var x = findByPhone(ph); if (x && x !== c) { o = x; pick = ph; } });
            if (!pick) pick = cn.phones.filter(function (ph) { return P.isBR(ph) && (ph.length === 13 || /[6-9]/.test(ph.charAt(4))); })[0] || cn.phones[0];
            c.phone = pick; linked++;
            if (o) merges.push([c.id, o.id]);
          }
        }
      });
      for (var i = 0; i < S.contacts.length; i++) await saveContact(S.contacts[i]);
      for (var j = 0; j < merges.length; j++) await mergeContacts(merges[j][0], merges[j][1]);
      log('✓ ' + named + ' nomes colocados, ' + linked + ' conversas ganharam número' + (merges.length ? ', ' + merges.length + ' juntadas' : '') + '.', 'ok');
      busyEnd('Pronto.');
    } catch (e) { log('✗ ' + errMsg(e), 'er'); busyEnd('Não deu certo.'); }
    renderAll();
  }

  // ------------------------------------------------------------------ pacote: salvar e restaurar
  // nome seguro para pasta/arquivo: corta o meio do nome, nunca a extensão (.pdf)
  function safeName(s, max) {
    max = max || 80;
    var t = C.clean(s).normalize('NFC').replace(/[\\/:*?"<>|\u0000-\u001f]+/g, ' ').replace(/\s+/g, ' ').trim();
    var em = /\.[a-z0-9]{1,5}$/i.exec(t), ext = em ? em[0] : '', stem = ext ? t.slice(0, -ext.length) : t;
    if (t.length > max) t = stem.slice(0, Math.max(1, max - ext.length)).trim() + ext;
    return t || 'sem nome';
  }
  function folderOf(c) {
    var ph = c.phone ? P.format(c.phone).replace(/[()]/g, '') : '';
    var nm = c.name ? safeName(c.name, ph ? 80 - ph.length - 3 : 80).replace(/\.$/, '') : '';
    return 'clientes/' + ([nm, ph].filter(Boolean).join(' - ') || safeName(label(c))) + '/';
  }
  async function exportPackage() {
    if (S.busy) { toast('Espere a importação terminar antes de gerar o pacote.'); return; }
    var opt = { image: $('#e-image').checked, audio: $('#e-audio').checked, video: $('#e-video').checked, sticker: !!(S.settings.media && S.settings.media.sticker), doc: true, contact: true };
    var lg = $('#pkglog'); lg.hidden = false; lg.textContent = '';
    function plog(t) { lg.appendChild(h('div', null, t)); lg.scrollTop = lg.scrollHeight; }
    var btn = $('#go-pkg'); btn.disabled = true;
    try {
      var list = S.contacts.filter(function (c) { return !c.demo; }).sort(function (a, b) { return label(a).localeCompare(label(b), 'pt-BR'); });
      if (!list.length) { plog('Ainda não há conversas importadas.'); return; }
      var zw = new C.ZipWriter(), manifest = { app: 'arquivo-clientes', version: 1, exportedAt: Date.now(), settings: S.settings, learnedMe: S.learnedMe, contacts: [] };
      var idxLines = ['ARQUIVO DE CLIENTES — histórico do WhatsApp Business', 'Gerado em ' + fDate(Date.now()) + ' ' + fTime(Date.now()), '',
        'Cada pasta em "clientes" é uma conversa: nome e número no nome da pasta,', 'conversa.txt com as mensagens e a pasta "arquivos" com PDFs e fotos.',
        'Para voltar tudo ao app: Arquivo de Clientes › Importar › Restaurar um pacote salvo.', '', 'CLIENTES', ''];
      var nf = 0, bytes = 0, usedFolders = {};
      for (var i = 0; i < list.length; i++) {
        var c = list[i], folder = folderOf(c), base = folder, dup = 2;
        while (usedFolders[folder.toLowerCase()]) folder = base.replace(/\/$/, '') + ' (' + (dup++) + ')/';
        usedFolders[folder.toLowerCase()] = 1;
        var msgs = await DB.messagesOf(c.id), fileOf = {};
        for (var j = 0; j < msgs.length; j++) {
          var m = msgs[j];
          if (!m.m || !m.m.b || !opt[m.ty]) continue;
          var br = await DB.get('blobs', m.m.b); if (!br) continue;
          var put = await zw.add(folder + 'arquivos/' + safeName(m.m.n), br.blob, new Date(m.ts));
          fileOf[m.k] = put.slice(folder.length); nf++; bytes += br.s || br.blob.size;
        }
        var txt = C.transcript(c, msgs.map(function (m) { return Object.assign({}, m, { a: m.a || (m.ap ? (nameForPhone(m.ap) || P.format(m.ap)) : null) }); }), 'Eu', function (m) { return fileOf[m.k] || ('(não guardado) ' + m.m.n); });
        await zw.add(folder + 'conversa.txt', txt);
        var data = { contact: c, messages: msgs.map(function (m) { var v = Object.assign({}, m); if (v.m) { v.m = Object.assign({}, v.m); delete v.m.b; if (fileOf[m.k]) v.file = fileOf[m.k]; } return v; }) };
        await zw.add(folder + 'dados.json', JSON.stringify(data));
        manifest.contacts.push({ id: c.id, folder: folder });
        idxLines.push(label(c) + (c.phone && c.name ? '  ' + P.format(c.phone) : '') + '  —  ' + pl(msgs.length, 'mensagem', 'mensagens') + (c.st && c.st.docs ? ', ' + pl(c.st.docs, 'documento', 'documentos') : '') + (c.status ? '  [' + c.status + ']' : ''));
        if (i % 10 === 0) { plog('Montando… ' + (i + 1) + ' de ' + list.length + ' clientes'); await tick(); }
      }
      await zw.add('LEIA-ME.txt', idxLines.join('\n') + '\n');
      await zw.add('arquivo.json', JSON.stringify(manifest));
      var blob = zw.finish();
      var name = 'Arquivo-de-Clientes-' + new Date().toISOString().slice(0, 10) + '.zip';
      plog('Pacote pronto: ' + list.length + ' clientes, ' + num(nf) + ' arquivos, ' + fSize(blob.size) + '.');
      var ok = await Plat.save(blob, name);
      plog(ok ? 'Salvo como ' + name + '. Guarde no iCloud Drive ou no Google Drive.' : 'Não foi salvo.');
      if (ok) { await DB.put('meta', { key: 'lastPkg', v: Date.now() }); renderBackup(); }
    } catch (e) { plog('Erro: ' + errMsg(e)); }
    finally { btn.disabled = false; }
  }
  async function importPackage(file, nested) {
    if (!nested) { if (!(await busyStart('Restaurando pacote…'))) return; await removeDemo(); requestPersist(); }
    try {
      var zr = new C.ZipReader(file), ents = await zr.open(), by = {};
      ents.forEach(function (e) { by[e.name] = e; });
      // o pacote pode ter sido descompactado e compactado de novo (ganha uma pasta por fora)
      var manE = ents.filter(function (e) { return /(^|\/)arquivo\.json$/.test(e.name) && !/(^|\/)__MACOSX\//.test(e.name); }).sort(function (x, y) { return x.name.length - y.name.length; })[0];
      if (!manE) throw new Error('Este .zip não é um pacote do Arquivo de Clientes.');
      var pre = manE.name.slice(0, manE.name.length - 'arquivo.json'.length);
      var man = JSON.parse(await zr.text(manE));
      if (man.learnedMe) { Object.keys(man.learnedMe).forEach(function (k) { S.learnedMe[k] = Math.max(S.learnedMe[k] || 0, man.learnedMe[k]); }); await DB.put('meta', { key: 'learnedMe', v: S.learnedMe }); }
      if (man.settings) {
        if (!S.settings.myNames && man.settings.myNames) S.settings.myNames = man.settings.myNames;
        var mm0 = man.settings.media || {};
        ['image', 'audio', 'video', 'sticker'].forEach(function (k) { S.settings.media[k] = !!(S.settings.media[k] || mm0[k]); });
        await saveSettings(); syncSettingsUI();
      }
      var touched = {}, nm = 0, nf = 0, nc = 0, bad = 0, seenFolder = {};
      for (var i = 0; i < man.contacts.length; i++) {
        var fo = man.contacts[i].folder;
        // pacotes antigos: duas pessoas na mesma pasta ficaram como "dados.json" e "dados (2).json"
        var occ = seenFolder[fo] = (seenFolder[fo] || 0) + 1;
        var ent = by[pre + fo + (occ === 1 ? 'dados.json' : 'dados (' + occ + ').json')];
        if (!ent) { log('• Faltou ' + fo + 'dados.json no pacote.'); continue; }
        var data = JSON.parse(await zr.text(ent)), pc = data.contact;
        var c = await upsertContact({ id: pc.id, name: pc.name, phone: pc.phone, isGroup: pc.isGroup, nameSrc: pc.nameSrc });
        // o mesmo cliente pode estar aqui com outro id (juntado em outro aparelho)
        var ids = [pc.id].concat(pc.aliases || []).concat(c.aliases || []);
        for (var ai = 0; ai < ids.length; ai++) { var x = S.byId[ids[ai]]; if (x && x !== c && !x.isGroup) await mergeContacts(x.id, c.id); }
        (pc.aliases || []).forEach(function (al) { addAlias(c, al); });
        if (pc.id !== c.id) addAlias(c, pc.id);
        if (pc.nameSrc === 'manual' && pc.name) { c.name = pc.name; c.nameSrc = 'manual'; }
        if (pc.notes && c.notes !== pc.notes) {
          if (!c.notes || pc.notes.indexOf(c.notes) >= 0) c.notes = pc.notes;          // o pacote tem tudo e mais
          else if (c.notes.indexOf(pc.notes) < 0) c.notes = c.notes + '\n\n' + pc.notes; // textos diferentes: guarda os dois
          // senão: o que está aqui já contém o do pacote (é mais novo) e fica como está
        }
        if (pc.status && !c.status) c.status = pc.status;
        await saveContact(c);
        var out = [];
        for (var j = 0; j < data.messages.length; j++) {
          var m = data.messages[j], v = Object.assign({}, m);
          v.cid = c.id; v.k = rekey(c.id, m.k); if (m.bk) v.bk = rekey(c.id, m.bk);
          if (v.file && v.m) {
            var fe = by[pre + fo + v.file] || by[pre + fo + String(v.file).normalize('NFC')];
            if (fe) {
              try { var bl = await zr.blob(fe, v.m.mi || C.mimeOf(v.m.n)); v.m = Object.assign({}, v.m); v.m.b = await saveBlob(c.id, v.m.n, bl, v.m.mi); v.m.s = bl.size; nf++; }
              catch (e) { bad++; if (bad <= 5) log('• ' + errMsg(e)); }
            }
          }
          delete v.file;
          out.push(v);
          if (out.length >= 1000) { await DB.upsert(out); out = []; }
        }
        await DB.upsert(out);
        nm += data.messages.length; touched[c.id] = 1; nc++;
        if (!nested) { setBar(i / man.contacts.length); $('#prog-title').textContent = 'Restaurando… ' + (i + 1) + ' de ' + man.contacts.length + ' clientes'; }
        await tick();
      }
      if (bad) log('• ' + pl(bad, 'arquivo danificado não foi restaurado', 'arquivos danificados não foram restaurados') + '. Se tiver outra cópia do pacote, restaure também.');
      await refreshStats(Object.keys(touched));
      log('✓ Pacote de ' + fDate(man.exportedAt) + ': ' + pl(nc, 'cliente', 'clientes') + ', ' + pl(nm, 'mensagem', 'mensagens') + ', ' + pl(nf, 'arquivo', 'arquivos') + '.', 'ok');
      if (!nested) { setBar(1); busyEnd('Pacote restaurado.'); }
    } catch (e) {
      log('✗ ' + errMsg(e), 'er');
      if (!nested) busyEnd('Não deu certo.');
      else throw e;
    }
    if (!nested) renderAll();
  }
  async function exportCsv() {
    var rows = [['Nome', 'Número', 'Situação', 'Primeira mensagem', 'Última mensagem', 'Mensagens', 'Documentos', 'Anotações']];
    S.contacts.filter(function (c) { return !c.demo; }).sort(byLast).forEach(function (c) {
      var st = c.st || {};
      // número sem o "+" para a planilha não transformar em conta
      rows.push([c.name || '', c.phone ? P.format(c.phone).replace(/^\+/, '') : '', c.status || '', st.first ? fDate(st.first) : '', st.last ? fDate(st.last) : '', st.n || 0, st.docs || 0, c.notes || '']);
    });
    var csv = '\ufeff' + rows.map(function (r) { return r.map(function (v, ci) { v = String(v); if (ci !== 1 && /^[=+\-@\t\r]/.test(v)) v = "'" + v; return /[;"\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(';'); }).join('\r\n');
    await Plat.save(new Blob([csv], { type: 'text/csv' }), 'clientes-' + new Date().toISOString().slice(0, 10) + '.csv');
  }

  // ------------------------------------------------------------------ exemplo (quando ainda não há nada)
  async function seedDemo() {
    var base = new Date(); base.setHours(0, 0, 0, 0);
    var day = 86400000, t0 = base.getTime() - 40 * day;
    var pdf = new Blob([C.samplePdf(['Proposta comercial (EXEMPLO)', 'Cliente: Ana Ribeiro (ficticia)', 'Reforma de cozinha planejada', 'Valor: R$ 18.400,00', 'Validade: 15 dias', '', 'Este PDF e so uma demonstracao do Arquivo de Clientes.'])], { type: 'application/pdf' });
    var people = [
      { id: 'demo:ana', name: 'Ana Ribeiro (exemplo)', phone: '5511987650000', status: 'Proposta enviada', notes: 'Exemplo: quer começar em janeiro. Ligar dia 10.', msgs: [
        [0, 0, 'Oi! Vi o anúncio de vocês. Fazem cozinha planejada?'], [0, 1, 'Fazemos sim, Ana! Me passa as medidas da parede?'], [1, 0, '3,20 m por 2,60 m. Tem janela no meio.'],
        [3, 1, 'Segue a proposta. Qualquer dúvida me chama.', 'Proposta Cozinha Ana.pdf'], [4, 0, 'Recebi! Vou ver com meu marido e te falo.']] },
      { id: 'demo:marcos', name: 'Marcos Lima (exemplo)', phone: '5521998760000', status: 'Fechado', notes: '', msgs: [
        [10, 0, 'Bom dia, o orçamento do banheiro ainda vale?'], [10, 1, 'Vale sim até sexta.'], [11, 0, 'Fechado então. Pode começar segunda.']] },
      { id: 'demo:loja', name: null, phone: '5531988880000', status: '', notes: '', msgs: [[20, 0, 'Olá, vocês atendem em BH?'], [20, 1, 'Atendemos sim! Qual bairro?']] }
    ];
    for (var i = 0; i < people.length; i++) {
      var p = people[i], c = { id: p.id, name: p.name, phone: p.phone, isGroup: false, notes: p.notes, status: p.status, demo: true, created: Date.now(), st: {} };
      S.contacts.push(c); indexContact(c); await saveContact(c);
      var keyer = C.makeKeyer(c.id), out = [];
      for (var j = 0; j < p.msgs.length; j++) {
        var q = p.msgs[j], ts = t0 + q[0] * day + (9 + j) * 3600000 + i * 7 * day;
        var rec = { cid: c.id, ts: ts, seq: j, me: q[1], a: q[1] ? null : (p.name || null), t: q[2], ty: 'text', sys: 0, src: ['demo'] };
        if (q[3]) { rec.ty = 'doc'; rec.m = { n: q[3], mi: 'application/pdf', s: pdf.size, b: await saveBlob(c.id, q[3], pdf, 'application/pdf') }; }
        rec.k = rec.bk = keyer(rec.ts, rec.me, rec.t, rec.m && rec.m.n, rec.ty);
        out.push(rec);
      }
      await DB.upsert(out);
    }
    await refreshStats(people.map(function (p) { return p.id; }));
  }

  // ------------------------------------------------------------------ telas
  function byLast(a, b) { return ((b.st && b.st.last) || 0) - ((a.st && a.st.last) || 0); }
  var STATUS = [['', 'Sem situação'], ['Novo contato', 'Novo contato'], ['Proposta enviada', 'Proposta enviada'], ['Negociando', 'Negociando'], ['Fechado', 'Fechado'], ['Cliente ativo', 'Cliente ativo'], ['Perdido', 'Perdido']];
  function statusClass(s) {
    return { 'Novo contato': 'st-novo', 'Proposta enviada': 'st-proposta', 'Negociando': 'st-negociando', 'Fechado': 'st-fechado', 'Cliente ativo': 'st-ativo', 'Perdido': 'st-perdido' }[s] || '';
  }
  function highlight(text, q) {
    var t = String(text || '');
    if (!q) return t;
    var ft = C.fold(t), fq = C.fold(q);
    if (!fq || ft.length !== t.length) {
      var i0 = t.toLowerCase().indexOf(q.toLowerCase());
      if (i0 < 0) return t;
      return h('span', null, t.slice(0, i0), h('mark', null, t.slice(i0, i0 + q.length)), t.slice(i0 + q.length));
    }
    var i = ft.indexOf(fq); if (i < 0) return t;
    return h('span', null, t.slice(0, i), h('mark', null, t.slice(i, i + fq.length)), t.slice(i + fq.length));
  }
  // "(011) 98765-4321": tira o zero de discagem antes do DDD
  function trunk(qd) { return /^0[1-9]{2}\d{8,9}$/.test(qd) ? qd.slice(1) : qd; }
  function filtered() {
    var q = S.q.trim(), qd = trunk(P.digits(q)), qf = C.fold(q);
    var hasLetters = /[a-z]/.test(qf);
    var list = S.contacts.filter(function (c) {
      if (!q) return true;
      if (qd.length >= 3 && !hasLetters) return c.phone ? P.matches(c.phone, qd) : false;
      if (qf && C.fold(c.name || '').indexOf(qf) >= 0) return true;
      if (qf && c.notes && C.fold(c.notes).indexOf(qf) >= 0) return true;
      if (qf && c.status && C.fold(c.status).indexOf(qf) >= 0) return true;
      return false;
    });
    return list.sort(byLast);
  }

  function renderList() {
    var box = $('#list'); box.textContent = '';
    var list = filtered(), demo = S.contacts.some(function (c) { return c.demo; });
    if (demo) box.appendChild(h('div', { class: 'banner' },
      h('p', null, h('b', null, 'Estes clientes são exemplos fictícios. '), 'Quando você importar o histórico do S22, eles somem sozinhos.'),
      h('a', { class: 'btn small', href: '#importar' }, 'Importar agora')));
    var real = S.contacts.length;
    box.appendChild(h('p', { class: 'count' }, h('span', null, S.q ? num(list.length) + ' de ' + num(real) + ' contatos' : num(real) + ' contatos'), S.q && P.digits(S.q).length >= 3 && !/[a-z]/i.test(S.q) ? h('span', null, 'busca por número') : null));
    if (!real) {
      box.appendChild(h('div', { class: 'empty' }, h('p', null, 'Nenhuma conversa ainda.'), h('a', { class: 'btn', href: '#importar' }, 'Importar do S22')));
      return;
    }
    var ul = h('ul', { class: 'clist', role: 'listbox', 'aria-label': 'Clientes' });
    list.slice(0, S.listLimit).forEach(function (c) {
      var st = c.st || {};
      var li = h('li', { class: 'crow', role: 'option', tabindex: '0', 'aria-selected': S.open === c.id ? 'true' : 'false', 'data-id': c.id },
        avatar(c),
        h('span', { class: 'nm' }, highlight(label(c), /[a-z]/i.test(S.q) ? S.q.trim() : '')),
        h('span', { class: 'dt' }, fShort(st.last)),
        h('span', { class: 'ph' }, c.phone && c.name ? P.format(c.phone) : (c.isGroup ? 'grupo' : (c.lid ? 'sem número (contato oculto)' : (c.phone ? '' : 'sem número')))),
        h('span', { class: 'tags' },
          c.demo ? h('span', { class: 'pill demo' }, 'exemplo') : null,
          c.status ? h('span', { class: 'pill ' + statusClass(c.status) }, c.status) : null,
          st.docs ? h('span', { class: 'pill doc', title: st.docs + ' documentos' }, st.docs + (st.pdf === st.docs ? ' pdf' : ' doc')) : null),
        st.snip ? h('span', { class: 'sn' }, st.snip) : null);
      ul.appendChild(li);
    });
    box.appendChild(ul);
    if (list.length > S.listLimit) box.appendChild(h('div', { class: 'more' }, h('button', { class: 'btn ghost small', type: 'button', onclick: function () { S.listLimit += 300; renderList(); } }, 'Mostrar mais ' + Math.min(300, list.length - S.listLimit))));
    var q = S.q.trim();
    if (q.length >= 2) {
      var hits = h('div', { class: 'hits', id: 'hits' },
        h('button', { class: 'btn ghost small', type: 'button', onclick: function () { searchMessages(q); } }, 'Procurar “' + q + '” dentro das conversas'));
      box.appendChild(hits);
    }
  }
  async function searchMessages(q) {
    var box = $('#hits'); if (!box) return;
    box.textContent = 'Procurando…';
    var qf = C.fold(q), out = [], max = 300;
    await DB.each('messages', function (m) {
      if ((m.t && C.fold(m.t).indexOf(qf) >= 0) || (m.m && m.m.n && C.fold(m.m.n).indexOf(qf) >= 0)) { out.push(m); if (out.length >= max) return false; }
    });
    box.textContent = '';
    box.appendChild(h('p', { class: 'count' }, out.length >= max ? 'Primeiros ' + max + ' resultados' : num(out.length) + ' mensagens com “' + q + '”'));
    out.sort(function (a, b) { return b.ts - a.ts; }).forEach(function (m) {
      var c = S.byId[m.cid];
      box.appendChild(h('button', { class: 'hit', type: 'button', onclick: function () { openContact(m.cid, m.k); } },
        h('span', { class: 'who' }, c ? label(c) : '?'), h('span', { class: 'when' }, fDate(m.ts)),
        h('span', { class: 'tx' }, highlight(m.m ? m.m.n + (m.t ? ' — ' + m.t : '') : m.t, q))));
    });
  }

  async function openContact(id, focusKey, stay) {
    S.open = id;
    if (S.view !== 'clientes' && !stay) { location.hash = '#clientes'; }
    $$('.crow').forEach(function (r) { r.setAttribute('aria-selected', r.getAttribute('data-id') === id ? 'true' : 'false'); });
    $('#v-clientes').classList.add('open');
    await renderDetail(focusKey);
    if (window.innerWidth < 900 && !stay) window.scrollTo(0, 0);
  }
  function closeContact() {
    S.open = null; $('#v-clientes').classList.remove('open'); revokeUrls();
    $$('.crow').forEach(function (r) { r.setAttribute('aria-selected', 'false'); });
    renderDetailEmpty();
  }
  function revokeUrls() { S.urls.forEach(function (u) { URL.revokeObjectURL(u); }); S.urls = []; }
  function renderDetailEmpty() {
    var d = $('#detail'); d.textContent = '';
    if (!S.contacts.length) return;
    d.appendChild(h('div', { class: 'empty' }, h('p', null, 'Escolha um cliente na lista ou busque pelo número.'), h('p', { class: 'mono', style: 'font-size:.8rem' }, 'Dica: digite só o final do número, ex.: 4321')));
  }

  var detailTab = 'conversa';
  var renderSeq = 0;
  async function renderDetail(focusKey) {
    var seq = ++renderSeq, c = S.byId[S.open], d = $('#detail');
    if (!c) { revokeUrls(); return renderDetailEmpty(); }
    var st = c.st || {};
    var msgs = await DB.messagesOf(c.id);
    if (seq !== renderSeq) return; // outro cliente foi aberto enquanto carregava
    revokeUrls();
    d.textContent = '';
    var docs = msgs.filter(function (m) { return m.m && m.ty === 'doc'; });
    var waNum = c.phone ? P.full(c.phone) : null;
    var phoneLine = h('div', { class: 'phone' },
      c.phone ? (c.name ? h('span', null, P.format(c.phone)) : null) : h('span', { class: 'mute' }, c.isGroup ? 'Grupo' : (c.lid ? 'Sem número (o WhatsApp escondeu o número deste contato)' : 'Sem número — dá para colocar na aba Anotações')),
      c.phone ? h('button', { class: 'btn ghost small', type: 'button', onclick: function () { copy(P.format(c.phone)); } }, 'Copiar') : null,
      waNum ? h('a', { class: 'btn ghost small', href: 'https://wa.me/' + waNum, target: '_blank', rel: 'noopener' }, 'Abrir no WhatsApp') : null);
    var head = h('div', { class: 'fhead' },
      h('div', { class: 'fh-top' }, avatar(c, true), h('div', null, h('h2', null, label(c)), phoneLine)),
      h('div', { class: 'stats' },
        h('span', null, h('b', null, num(st.n)), st.n === 1 ? ' mensagem' : ' mensagens'),
        h('span', null, h('b', null, num(docs.length)), docs.length === 1 ? ' documento' : ' documentos'),
        st.first ? h('span', null, 'desde ', h('b', null, fDate(st.first))) : null,
        st.last ? h('span', null, 'último ', h('b', null, fDate(st.last))) : null),
      h('div', { class: 'acts' }, c.status ? h('span', { class: 'pill ' + statusClass(c.status) }, c.status) : null, c.demo ? h('span', { class: 'pill demo' }, 'exemplo fictício') : null));
    var tabs = h('div', { class: 'ftabs', role: 'tablist' });
    [['conversa', 'Conversa'], ['documentos', 'Arquivos (' + docs.length + ')'], ['ficha', 'Anotações']].forEach(function (t) {
      tabs.appendChild(h('button', { type: 'button', role: 'tab', 'aria-selected': detailTab === t[0] ? 'true' : 'false', onclick: function () { detailTab = t[0]; renderDetail(); } }, t[1]));
    });
    var body = h('div', { class: 'fbody' });
    var card = h('div', { class: 'card ficha' }, head, tabs, body);
    d.appendChild(h('button', { class: 'back', type: 'button', onclick: closeContact }, '‹ Clientes'));
    d.appendChild(card);
    if (focusKey) detailTab = 'conversa';
    if (detailTab === 'documentos') renderDocsOf(body, docs, c);
    else if (detailTab === 'ficha') renderFicha(body, c);
    else renderChat(body, msgs, c, focusKey);
  }
  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { toast('Copiado: ' + text); }, function () { toast(text); });
    } else toast(text);
  }

  function renderChat(body, msgs, c, focusKey) {
    var CH = 300, shown = CH, filter = '';
    var bar = h('div', { class: 'chatbar' },
      h('input', { class: 'txt', type: 'search', placeholder: 'Procurar nesta conversa', 'aria-label': 'Procurar nesta conversa', oninput: function (e) { filter = e.target.value.trim(); shown = CH; draw(); } }),
      h('button', { class: 'btn ghost small', type: 'button', onclick: function () { shown = msgs.length; draw(); var f = box.firstElementChild; if (f) f.scrollIntoView(); } }, 'Ir para o início'));
    var box = h('div', { class: 'chat' });
    body.appendChild(bar); body.appendChild(box);
    if (!msgs.length) { box.appendChild(h('p', { class: 'mute' }, 'Sem mensagens.')); return; }
    if (focusKey) { var fi = msgs.findIndex(function (m) { return m.k === focusKey; }); if (fi >= 0) shown = Math.max(CH, msgs.length - fi + 20); }
    function draw() {
      box.textContent = ''; revokeUrls();
      var list = msgs;
      if (filter) { var ff = C.fold(filter); list = msgs.filter(function (m) { return (m.t && C.fold(m.t).indexOf(ff) >= 0) || (m.m && C.fold(m.m.n).indexOf(ff) >= 0); }); }
      var start = Math.max(0, list.length - shown);
      if (start > 0) box.appendChild(h('div', { class: 'more' }, h('button', { class: 'btn ghost small', type: 'button', onclick: function () { shown += CH; draw(); } }, 'Mostrar ' + Math.min(CH, start) + ' anteriores (faltam ' + num(start) + ')')));
      if (filter && !list.length) box.appendChild(h('p', { class: 'mute' }, 'Nada encontrado nesta conversa.'));
      var lastDay = '';
      for (var i = start; i < list.length; i++) {
        var m = list[i], dk = new Date(m.ts).toDateString();
        if (dk !== lastDay) { box.appendChild(h('div', { class: 'day' }, fDay(m.ts))); lastDay = dk; }
        box.appendChild(bubble(m, c, filter));
      }
      lazyMedia(box);
      if (focusKey) {
        var el = box.querySelector('[data-k="' + cssEsc(focusKey) + '"]');
        if (el) { el.classList.add('flash'); el.scrollIntoView({ block: 'center' }); }
        focusKey = null;
      }
    }
    draw();
  }
  function cssEsc(s) { return window.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/["\\]/g, '\\$&'); }
  function bubble(m, c, q) {
    var cls = 'msg' + (m.me ? ' me' : '') + (m.sys ? ' sys' : '') + (m.ty === 'deleted' ? ' del' : '');
    var el = h('div', { class: cls, 'data-k': m.k });
    if (m.sys) { el.appendChild(document.createTextNode(m.t)); return el; }
    if (c.isGroup && !m.me) {
      var au = m.a || (m.ap ? (nameForPhone(m.ap) || P.format(m.ap)) : null);
      if (au) el.appendChild(h('span', { class: 'au' }, au));
    }
    if (m.m) el.appendChild(mediaEl(m, c));
    else if (m.ty === 'omitted') el.appendChild(h('span', { class: 'tx mute' }, '‹ mídia que não veio na exportação ›'));
    if (m.t && m.ty !== 'omitted') el.appendChild(h('span', { class: 'tx' }, q ? highlight(m.t, q) : m.t));
    el.appendChild(h('span', { class: 'tm' }, fTime(m.ts) + (m.ed ? ' · editada' : '')));
    return el;
  }
  function icLabel(n, ty) {
    var e = C.extOf(n);
    if (ty === 'image') return 'FOTO';
    if (ty === 'audio') return 'ÁUDIO';
    if (ty === 'video') return 'VÍDEO';
    return (e || 'ARQ').toUpperCase().slice(0, 4);
  }
  function mediaEl(m, c) {
    var mm = m.m, name = mm.o && /\.[a-z0-9]{2,5}$/i.test(mm.o) ? mm.o : mm.n;
    if (mm.b && m.ty === 'image') {
      var img = h('img', { class: 'thumb', alt: name, 'data-b': mm.b, loading: 'lazy', onclick: function () { openFile(mm.b, name, mm.mi); } });
      return img;
    }
    if (mm.b && (m.ty === 'audio' || m.ty === 'video')) {
      var w = h('div', null, h('button', { class: 'att', type: 'button', onclick: function () { openFile(mm.b, name, mm.mi); } },
        h('span', { class: 'ic' }, icLabel(name, m.ty)), h('span', { class: 'ai' }, h('span', { class: 'an' }, name), h('span', { class: 'am' }, fSize(mm.s) + ' · tocar'))));
      return w;
    }
    if (mm.b) {
      return h('button', { class: 'att', type: 'button', onclick: function () { openFile(mm.b, name, mm.mi); } },
        h('span', { class: 'ic' }, icLabel(name, m.ty)),
        h('span', { class: 'ai' }, h('span', { class: 'an' }, name), h('span', { class: 'am' }, [fSize(mm.s), 'abrir'].filter(Boolean).join(' · '))));
    }
    return h('div', { class: 'att missing', title: 'O arquivo não veio. Use Importar › Ligar PDFs e fotos que faltaram.' },
      h('span', { class: 'ic' }, icLabel(name, m.ty)),
      h('span', { class: 'ai' }, h('span', { class: 'an' }, name), h('span', { class: 'am' }, 'arquivo não importado' + (mm.s ? ' · ' + fSize(mm.s) : ''))));
  }
  var io = null;
  function lazyMedia(root) {
    var imgs = $$('img[data-b]', root);
    if (!imgs.length) return;
    function load(img) {
      var id = img.getAttribute('data-b'); img.removeAttribute('data-b');
      DB.get('blobs', id).then(function (r) { if (!r) return; var u = URL.createObjectURL(r.blob); S.urls.push(u); img.src = u; });
    }
    if (!('IntersectionObserver' in window)) return imgs.forEach(load);
    if (io) io.disconnect();
    io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); load(e.target); } }); }, { rootMargin: '400px' });
    imgs.forEach(function (i) { io.observe(i); });
  }
  function renderDocsOf(body, docs, c) {
    if (!docs.length) { body.appendChild(h('p', { class: 'mute' }, 'Nenhum documento nesta conversa.')); return; }
    var list = h('div', { class: 'dlist' });
    docs.slice().sort(function (a, b) { return b.ts - a.ts; }).forEach(function (m) { list.appendChild(docRow({ id: m.k, cid: m.cid, ts: m.ts, me: m.me, ty: m.ty, n: m.m.n, o: m.m.o, mi: m.m.mi, s: m.m.s, b: m.m.b }, false)); });
    body.appendChild(list);
  }
  function docRow(d, withContact) {
    var c = S.byId[d.cid], name = d.o && /\.[a-z0-9]{2,5}$/i.test(d.o) ? d.o : d.n;
    var row = h('div', { class: 'drow' + (d.b ? '' : ' missing') },
      h('span', { class: 'ic' }, icLabel(name, d.ty)),
      h('span', { class: 'dn' }, name),
      h('span', { class: 'dd' }, fDate(d.ts), h('br'), d.s ? fSize(d.s) : ''),
      h('span', { class: 'dm' },
        (d.me ? 'enviado' : 'recebido') + (withContact && c ? ' · ' : ''),
        withContact && c ? h('button', { type: 'button', onclick: function (e) { e.stopPropagation(); detailTab = 'documentos'; openContact(c.id); } }, label(c) + (c.phone && c.name ? ' · ' + P.format(c.phone) : '')) : null,
        d.b ? '' : ' · arquivo não importado'));
    if (d.b) { row.style.cursor = 'pointer'; row.tabIndex = 0; row.addEventListener('click', function () { openFile(d.b, name, d.mi); }); row.addEventListener('keydown', function (e) { if (e.key === 'Enter') openFile(d.b, name, d.mi); }); }
    return row;
  }
  function renderFicha(body, c) {
    var sel = h('select', { class: 'txt', id: 'f-status' });
    STATUS.forEach(function (s) { sel.appendChild(h('option', { value: s[0], selected: c.status === s[0] }, s[1])); });
    sel.addEventListener('change', async function () { c.status = sel.value; await saveContact(c); renderList(); renderDetail(); });
    var notes = h('textarea', { class: 'txt', id: 'f-notes', rows: '6', placeholder: 'Ex.: valor combinado, próximos passos, data para retornar…' });
    notes.value = c.notes || '';
    var tmr; notes.addEventListener('input', function () { clearTimeout(tmr); tmr = setTimeout(async function () { c.notes = notes.value; await saveContact(c); $('#saved').textContent = 'salvo ' + fTime(Date.now()); }, 500); });
    var nameIn = h('input', { class: 'txt', type: 'text', id: 'f-name', value: c.name || '', placeholder: 'Nome do cliente' });
    var phoneIn = h('input', { class: 'txt', type: 'tel', id: 'f-phone', value: c.phone ? P.format(c.phone) : '', placeholder: '(11) 98765-4321' });
    body.appendChild(h('div', { class: 'edit', style: 'border-top:0;background:transparent;padding:0' },
      h('div', { class: 'field' }, h('label', { for: 'f-status' }, 'Situação'), sel),
      h('div', { class: 'field' }, h('span', { class: 'lbl' }, 'Anotações salvas'), h('span', { class: 'mono mute', id: 'saved', style: 'font-size:.78rem' }, c.updated ? 'última alteração ' + fDate(c.updated) : '')),
      h('div', { class: 'field full' }, h('label', { for: 'f-notes' }, 'Anotações'), notes),
      h('div', { class: 'field' }, h('label', { for: 'f-name' }, 'Nome'), nameIn),
      h('div', { class: 'field' }, h('label', { for: 'f-phone' }, 'Número'), phoneIn),
      h('div', { class: 'full' }, h('button', { class: 'btn', type: 'button', onclick: async function () {
        c.name = nameIn.value.trim() || null; c.nameSrc = 'manual';
        var ok = await setPhone(c, phoneIn.value.trim());
        if (ok !== false) { await saveContact(S.byId[S.open] || c); toast('Dados salvos.'); renderAll(); }
      } }, 'Salvar nome e número')),
      h('p', { class: 'full mute', style: 'margin:0;font-size:.86rem' }, 'Se este cliente aparece duas vezes (uma pelo nome, outra pelo número), coloque o número aqui: as duas conversas viram uma só.')));
  }

  // ------------------------------------------------------------------ visualizador de arquivos
  var cur = null;
  async function openFile(blobId, name, mime) {
    var r = await DB.get('blobs', blobId);
    if (!r) { toast('Arquivo não encontrado.'); return; }
    var blob = r.blob, mi = mime || r.mi || blob.type || C.mimeOf(name);
    cur = { blob: blob, name: name, mime: mi };
    $('#vt').textContent = name;
    var vb = $('#vbody'); vb.textContent = '';
    var file = new File([blob], name, { type: mi });
    $('#v-share').hidden = !Plat.canShare(file);
    $('#v-open').hidden = Plat.framed;
    $('#viewer').hidden = false; document.body.style.overflow = 'hidden';
    $('#v-close').focus();
    if (/pdf$/i.test(mi) || /\.pdf$/i.test(name)) return renderPdf(blob, vb);
    var u = URL.createObjectURL(blob); cur.url = u;
    if (/^image\//.test(mi) && !/heic|heif/.test(mi)) vb.appendChild(h('img', { src: u, alt: name }));
    else if (/^audio\//.test(mi)) vb.appendChild(h('audio', { src: u, controls: true }));
    else if (/^video\//.test(mi)) vb.appendChild(h('video', { src: u, controls: true, playsinline: true, style: 'max-height:70vh' }));
    else if (/^text\//.test(mi)) { var t = await blob.text(); vb.appendChild(h('pre', { style: 'white-space:pre-wrap;max-width:70ch;background:var(--surface);padding:12px' }, t.slice(0, 200000))); }
    else vb.appendChild(h('p', { class: 'vnote' }, 'Pré-visualização indisponível para este tipo de arquivo (' + (C.extOf(name) || mi) + '). Use Salvar para abrir em outro app.'));
  }
  async function renderPdf(blob, vb) {
    var token = cur;
    var note = h('p', { class: 'vnote' }, 'Abrindo PDF…'); vb.appendChild(note);
    try {
      var lib = await loadPdf();
      if (cur !== token) return;
      var data = new Uint8Array(await blob.arrayBuffer());
      if (cur !== token) return;
      var doc = await lib.getDocument({ data: data, isEvalSupported: false }).promise;
      if (cur !== token) return;
      note.textContent = doc.numPages + (doc.numPages > 1 ? ' páginas' : ' página');
      var w = Math.min(vb.clientWidth - 24, 900), dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      for (var p = 1; p <= doc.numPages && p <= 60; p++) {
        if (cur !== token) return;
        var page = await doc.getPage(p);
        if (cur !== token) return;
        var vp0 = page.getViewport({ scale: 1 }), scale = w / vp0.width;
        var vp = page.getViewport({ scale: scale * dpr }), cv = h('canvas');
        cv.width = Math.floor(vp.width); cv.height = Math.floor(vp.height); cv.style.width = Math.floor(vp.width / dpr) + 'px';
        vb.appendChild(cv);
        await page.render({ canvasContext: cv.getContext('2d'), viewport: vp }).promise;
      }
      if (doc.numPages > 60) vb.appendChild(h('p', { class: 'vnote' }, 'Mostrando as 60 primeiras páginas. Use Salvar para ver o resto.'));
    } catch (e) {
      note.textContent = 'Não consegui mostrar este PDF aqui (' + errMsg(e) + '). Use Salvar' + (Plat.framed ? '' : ' ou Abrir') + '.';
    }
  }
  function closeViewer() {
    $('#viewer').hidden = true; document.body.style.overflow = ''; $('#vbody').textContent = '';
    if (cur && cur.url) URL.revokeObjectURL(cur.url);
    cur = null;
  }

  // ------------------------------------------------------------------ aba documentos
  var allDocs = null;
  async function renderDocsView() {
    if (!allDocs) allDocs = await DB.getAll('docs');
    var q = S.q.trim(), qf = C.fold(q), qd = trunk(P.digits(q)), letters = /[a-z]/.test(qf);
    var f = S.docFilter;
    var list = allDocs.filter(function (d) {
      if (f === 'pdf' && !(d.ty === 'doc' && (/pdf/i.test(d.mi) || /\.pdf$/i.test(d.n) || /\.pdf$/i.test(d.o || '')))) return false;
      if (f === 'doc' && d.ty !== 'doc') return false;
      if (f === 'image' && d.ty !== 'image') return false;
      if (f === 'missing' && (d.b || d.ty !== 'doc')) return false;
      if (!q) return true;
      var c = S.byId[d.cid];
      if (qd.length >= 3 && !letters) return !!(c && c.phone && P.matches(c.phone, qd));
      if (C.fold(d.n).indexOf(qf) >= 0 || C.fold(d.o || '').indexOf(qf) >= 0) return true;
      return !!(c && C.fold(c.name || '').indexOf(qf) >= 0);
    }).sort(function (a, b) { return b.ts - a.ts; });
    $$('#docfilters button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-f') === f ? 'true' : 'false'); });
    $('#doccount').textContent = num(list.length) + (list.length === 1 ? ' arquivo' : ' arquivos') + (q ? ' para “' + q + '”' : '');
    var box = $('#docs'); box.textContent = '';
    if (!list.length) box.appendChild(h('div', { class: 'empty' }, allDocs.length ? 'Nenhum arquivo com esse filtro.' : 'Nenhum documento ainda. Importe as conversas na aba Importar.'));
    list.slice(0, S.docLimit).forEach(function (d) { box.appendChild(docRow(d, true)); });
    var more = $('#docmore'); more.textContent = '';
    if (list.length > S.docLimit) more.appendChild(h('button', { class: 'btn ghost small', type: 'button', onclick: function () { S.docLimit += 200; renderDocsView(); } }, 'Mostrar mais'));
  }

  // ------------------------------------------------------------------ aba backup
  async function renderBackup() {
    var nm = await DB.count('messages'), nd = 0, nf = 0;
    await DB.each('docs', function (d) { if (d.ty === 'doc') { nd++; if (d.b) nf++; } });
    var real = S.contacts.filter(function (c) { return !c.demo; }).length;
    var lp = await DB.get('meta', 'lastPkg');
    var kv = $('#kv'); kv.textContent = '';
    [[num(real), 'clientes'], [num(nm), 'mensagens'], [num(nf) + (nd > nf ? ' / ' + num(nd) : ''), 'documentos guardados'], [lp && lp.v ? fDate(lp.v) : 'nunca', 'último pacote']].forEach(function (x) {
      kv.appendChild(h('div', null, h('b', null, x[0]), h('span', null, x[1])));
    });
    var stp = $('#storage');
    try {
      var est = navigator.storage && navigator.storage.estimate ? await navigator.storage.estimate() : null;
      var per = navigator.storage && navigator.storage.persisted ? await navigator.storage.persisted() : false;
      stp.textContent = (est ? 'Usando ' + fSize(est.usage) + (est.quota ? ' de ' + fSize(est.quota) + ' disponíveis' : '') + '. ' : '') +
        (per ? 'O navegador foi avisado para não apagar estes dados.' : 'O navegador pode apagar dados de sites pouco usados. No iPhone, adicione esta página à Tela de Início e guarde o pacote no iCloud Drive.');
      $('#go-persist').hidden = !!per;
    } catch (e) { stp.textContent = 'Não consegui medir o espaço.'; }
  }

  // ------------------------------------------------------------------ navegação
  function setView(v) {
    if (['clientes', 'documentos', 'importar', 'backup'].indexOf(v) < 0) v = 'clientes';
    S.view = v;
    ['clientes', 'documentos', 'importar', 'backup'].forEach(function (x) { $('#v-' + x).hidden = x !== v; });
    $$('.tabs a').forEach(function (a) { if (a.getAttribute('data-view') === v) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
    $('#searchbar').hidden = !(v === 'clientes' || v === 'documentos');
    if (v === 'documentos') renderDocsView();
    if (v === 'backup') renderBackup();
    if (v === 'importar') updateMissingNote();
  }
  async function updateMissingNote() {
    var n = 0;
    await DB.each('docs', function (d) { if (!d.b && d.ty === 'doc') n++; });
    var el = $('#missing-note');
    if (n) el.textContent = (n === 1 ? '1 documento aparece' : num(n) + ' documentos aparecem') + ' como “arquivo não importado”. Escolha aqui a pasta Media do S22 (ou um .zip dela, ou os PDFs soltos) e o app liga cada arquivo à sua mensagem pelo nome.';
  }
  function renderCounts() {
    $('#n-cli').textContent = S.contacts.length ? num(S.contacts.length) : '';
    var d = 0; S.contacts.forEach(function (c) { d += (c.st && c.st.docs) || 0; });
    $('#n-doc').textContent = d ? num(d) : '';
  }
  function renderAll() {
    allDocs = null;
    renderCounts();
    renderList();
    if (S.open && S.byId[S.open]) renderDetail(); else { S.open = null; $('#v-clientes').classList.remove('open'); renderDetailEmpty(); }
    if (S.view === 'documentos') renderDocsView();
    if (S.view === 'backup') renderBackup();
    if (S.view === 'importar') updateMissingNote();
  }

  function updateKeyCount() {
    var n = C.cleanKey($('#k-backup').value).length, kc = $('#kc');
    kc.textContent = n + ' de 64' + (n === 64 ? ' ✓' : '');
    kc.className = 'keycount' + (n === 64 ? ' ok' : '');
  }
  function picked(input, out) {
    var f = input.files, el = $(out);
    if (!f || !f.length) { el.textContent = ''; return; }
    el.textContent = f.length === 1 ? f[0].name + ' (' + fSize(f[0].size) + ')' : num(f.length) + ' arquivos';
  }

  function syncSettingsUI() {
    $('#s-me').value = S.settings.myNames || '';
    ['image', 'audio', 'video', 'sticker'].forEach(function (k) { $('#s-' + k).checked = !!S.settings.media[k]; });
  }
  function bind() {
    window.addEventListener('hashchange', function () { setView(location.hash.slice(1)); });
    var qt;
    $('#q').addEventListener('input', function (e) {
      clearTimeout(qt);
      qt = setTimeout(function () {
        S.q = e.target.value; S.listLimit = 200; S.docLimit = 120;
        if (S.view === 'documentos') return renderDocsView();
        if (window.innerWidth < 900 && $('#v-clientes').classList.contains('open')) closeContact();
        renderList();
      }, 120);
    });
    $('#q').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var first = $('.crow'); if (first && S.view === 'clientes') openContact(first.getAttribute('data-id')); }
    });
    $('#list').addEventListener('click', function (e) { var r = e.target.closest('.crow'); if (r) openContact(r.getAttribute('data-id')); });
    $('#list').addEventListener('keydown', function (e) { var r = e.target.closest('.crow'); if (r && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openContact(r.getAttribute('data-id')); } });
    $('#docfilters').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; S.docFilter = b.getAttribute('data-f'); S.docLimit = 120; renderDocsView(); });

    $('#k-backup').addEventListener('input', updateKeyCount);
    $('#f-backup').addEventListener('change', function () { picked(this, '#p-backup'); });
    var bmedia = [];
    function bm(input) { bmedia = Array.prototype.slice.call(input.files || []); $('#p-bmedia').textContent = bmedia.length ? num(bmedia.length) + ' arquivos' : 'nenhum'; }
    $('#f-bmedia').addEventListener('change', function () { bm(this); });
    $('#f-bmedia-dir').addEventListener('change', function () { bm(this); });
    $('#go-backup').addEventListener('click', function () {
      var f = $('#f-backup').files[0];
      if (!f) { toast('Escolha primeiro o arquivo msgstore.db.crypt15.'); return; }
      if (!/\.(db|sqlite)$/i.test(f.name) && C.cleanKey($('#k-backup').value).length !== 64) { toast('Digite a chave de 64 dígitos (ela aparece no S22 quando você ativa o backup com chave).'); return; }
      importBackup(f, $('#k-backup').value, bmedia);
    });
    $('#f-export').addEventListener('change', function () { picked(this, '#p-export'); var fs = Array.prototype.slice.call(this.files); this.value = ''; if (fs.length) importExports(fs); });
    function lk(input) { var fs = Array.prototype.slice.call(input.files || []); input.value = ''; $('#p-link').textContent = fs.length ? num(fs.length) + ' arquivos' : ''; if (fs.length) linkMedia(fs); }
    $('#f-link').addEventListener('change', function () { lk(this); });
    $('#f-link-dir').addEventListener('change', function () { lk(this); });
    $('#f-vcf').addEventListener('change', function () { picked(this, '#p-vcf'); var f = this.files[0]; this.value = ''; if (f) importVcf(f); });
    $('#f-pkg').addEventListener('change', function () { picked(this, '#p-pkg'); var f = this.files[0]; this.value = ''; if (f) importPackage(f); });

    syncSettingsUI();
    $('#s-me').addEventListener('change', async function () { S.settings.myNames = this.value; await saveSettings(); });
    ['image', 'audio', 'video', 'sticker'].forEach(function (k) {
      var el = $('#s-' + k);
      el.addEventListener('change', async function () { S.settings.media[k] = el.checked; await saveSettings(); });
    });

    $('#go-pkg').addEventListener('click', exportPackage);
    $('#go-csv').addEventListener('click', exportCsv);
    $('#go-persist').addEventListener('click', async function () { var ok = await requestPersist(); toast(ok ? 'Pronto: o navegador vai manter os dados.' : 'O navegador não confirmou. Guarde o pacote no iCloud Drive por segurança.'); renderBackup(); });
    $('#go-wipe').addEventListener('click', async function () {
      if (S.busy) { toast('Espere a importação terminar antes de apagar.'); return; }
      if ($('#wipe-confirm').value.trim().toUpperCase() !== 'APAGAR') { toast('Digite APAGAR no campo para confirmar.'); return; }
      await DB.clear(); S.contacts = []; S.byId = {}; S.open = null; S.learnedMe = {};
      await DB.put('meta', { key: 'demoSeen', v: 1 }); await saveSettings();
      $('#wipe-confirm').value = ''; toast('Tudo apagado deste aparelho.'); renderAll();
    });

    $('#v-close').addEventListener('click', closeViewer);
    $('#viewer').addEventListener('click', function (e) { if (e.target === this) closeViewer(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !$('#viewer').hidden) closeViewer(); });
    $('#v-save').addEventListener('click', function () { if (cur) Plat.save(cur.blob, cur.name); });
    $('#v-share').addEventListener('click', function () { if (cur) Plat.share(cur.blob, cur.name); });
    $('#v-open').addEventListener('click', function () { if (cur) Plat.open(cur.blob); });
    window.addEventListener('beforeunload', function (e) { if (S.busy) { e.preventDefault(); e.returnValue = ''; } });
  }

  async function start() {
    Plat.init();
    // iPhone e iPad não escolhem pastas: lá o caminho é o .zip da pasta
    if (/iP(hone|ad|od)/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
      $$('label[for$="-dir"]').forEach(function (l) { l.hidden = true; });
    }
    var v0 = location.hash.slice(1);
    ['clientes', 'documentos', 'importar', 'backup'].forEach(function (x) { $('#v-' + x).hidden = x !== (['documentos', 'importar', 'backup'].indexOf(v0) >= 0 ? v0 : 'clientes'); });
    try { await DB.open(); }
    catch (e) {
      S.storageOk = false;
      $('#list').appendChild(h('div', { class: 'banner' }, h('p', null, h('b', null, 'Este navegador não deixou guardar dados. '), 'Abra o app fora da janela anônima (ou em outro navegador) para importar o histórico. Detalhe: ' + errMsg(e))));
      bind(); setView(location.hash.slice(1));
      return;
    }
    await loadAll();
    bind();
    setView(location.hash.slice(1));
    if (!S.contacts.length) { var seeded = await DB.get('meta', 'demoSeen'); if (!seeded) { await DB.put('meta', { key: 'demoSeen', v: 1 }); seedP = seedDemo(); await seedP; } }
    renderAll();
    if (window.innerWidth >= 900 && !S.open) {
      var first = S.contacts.slice().sort(byLast)[0];
      if (first) openContact(first.id, null, true);
    }
  }
  window.ArqApp = { S: S, DB: DB, importExports: importExports, importBackup: importBackup, linkMedia: linkMedia, importVcf: importVcf, importPackage: importPackage, exportPackage: exportPackage, openContact: openContact };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
