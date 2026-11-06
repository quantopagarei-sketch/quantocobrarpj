/* Arquivo de Clientes — núcleo sem interface.
   Lê exportações do WhatsApp (.txt/.zip), abre o backup criptografado do Android
   (msgstore.db.crypt15 + chave de 64 dígitos), lê e grava .zip e trata telefones.
   Roda no navegador e no Node 18+ (usado nos testes). Nada sai do aparelho. */
(function (root) {
  'use strict';

  // ---------------------------------------------------------------- texto
  var INVIS = /[​-‏‪-‮⁦-⁩﻿]/g;
  function clean(s) {
    return String(s == null ? '' : s).replace(INVIS, '').replace(/[    ]/g, ' ').replace(/[‐‑‒–]/g, '-');
  }
  function fold(s) {
    return clean(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
  }
  function slug(s) {
    return fold(s).replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60) || 'sem-nome';
  }
  // cyrb53: hash rápido de 53 bits, só para chaves (não é criptografia)
  function hash(str, seed) {
    var h1 = 0xdeadbeef ^ (seed || 0), h2 = 0x41c6ce57 ^ (seed || 0);
    for (var i = 0, ch; i < str.length; i++) {
      ch = str.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 2654435761);
      h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
    return (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(36);
  }
  function baseName(p) { return String(p || '').replace(/^.*[\\/]/, ''); }
  // marcas de direção que o WhatsApp põe no texto; o resto do texto fica exatamente como veio
  var BIDI = /[‎‏‪-‮⁦-⁩﻿]/g;
  function stripBidi(s) { return String(s == null ? '' : s).replace(BIDI, ''); }
  // iPhone prefixa anexos com um número sequencial, ex.: "00000023-Proposta.pdf"
  function displayFileName(name) { return baseName(stripBidi(name)).replace(/^0\d{7}-(?=.)/, '').trim(); }
  function decodeText(bytes) {
    var t;
    try { t = new TextDecoder('utf-8', { fatal: true }).decode(bytes); }
    catch (e) {
      // UTF-16 com BOM ou texto antigo em Latin-1
      if (bytes[0] === 0xff && bytes[1] === 0xfe) t = new TextDecoder('utf-16le').decode(bytes);
      else if (bytes[0] === 0xfe && bytes[1] === 0xff) t = new TextDecoder('utf-16be').decode(bytes);
      else t = new TextDecoder('windows-1252').decode(bytes);
    }
    return t.replace(/^﻿/, '');
  }

  // ---------------------------------------------------------------- tipos de arquivo
  var EXT = {
    pdf: ['doc', 'application/pdf'],
    doc: ['doc', 'application/msword'], docx: ['doc', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    xls: ['doc', 'application/vnd.ms-excel'], xlsx: ['doc', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
    ppt: ['doc', 'application/vnd.ms-powerpoint'], pptx: ['doc', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'],
    odt: ['doc', 'application/vnd.oasis.opendocument.text'], ods: ['doc', 'application/vnd.oasis.opendocument.spreadsheet'],
    txt: ['doc', 'text/plain'], csv: ['doc', 'text/csv'], rtf: ['doc', 'application/rtf'],
    zip: ['doc', 'application/zip'], rar: ['doc', 'application/vnd.rar'], '7z': ['doc', 'application/x-7z-compressed'],
    xml: ['doc', 'application/xml'], ofx: ['doc', 'application/x-ofx'], dwg: ['doc', 'application/acad'], cdr: ['doc', 'application/octet-stream'],
    jpg: ['image', 'image/jpeg'], jpeg: ['image', 'image/jpeg'], png: ['image', 'image/png'], gif: ['image', 'image/gif'],
    heic: ['image', 'image/heic'], heif: ['image', 'image/heif'], bmp: ['image', 'image/bmp'],
    webp: ['image', 'image/webp'],
    opus: ['audio', 'audio/ogg'], ogg: ['audio', 'audio/ogg'], m4a: ['audio', 'audio/mp4'], mp3: ['audio', 'audio/mpeg'],
    aac: ['audio', 'audio/aac'], amr: ['audio', 'audio/amr'], wav: ['audio', 'audio/wav'],
    mp4: ['video', 'video/mp4'], '3gp': ['video', 'video/3gpp'], mov: ['video', 'video/quicktime'], mkv: ['video', 'video/x-matroska'], webm: ['video', 'video/webm'],
    vcf: ['contact', 'text/vcard']
  };
  function extOf(name) { var m = /\.([a-z0-9]{1,5})$/i.exec(baseName(name)); return m ? m[1].toLowerCase() : ''; }
  function kindOf(name, mime) {
    var b = baseName(name), e = extOf(b);
    if (/^STK-/i.test(b) || (e === 'webp' && /sticker|figurinha/i.test(b))) return 'sticker';
    if (EXT[e]) return EXT[e][0];
    if (mime) {
      if (/^image\//.test(mime)) return 'image';
      if (/^audio\//.test(mime)) return 'audio';
      if (/^video\//.test(mime)) return 'video';
      return 'doc';
    }
    return 'doc';
  }
  function mimeOf(name, fallback) { var e = extOf(name); return (EXT[e] && EXT[e][1]) || fallback || 'application/octet-stream'; }

  // ---------------------------------------------------------------- telefones
  var Phone = {
    digits: function (s) { return clean(s).replace(/\D/g, ''); },
    // número completo só com dígitos e código do país (padrão Brasil)
    normalize: function (s, cc) {
      cc = cc || '55';
      var raw = clean(s).trim(), d = Phone.digits(raw);
      if (!d) return null;
      if (d.indexOf('00') === 0 && raw.charAt(0) !== '+') d = d.slice(2);
      if (raw.charAt(0) !== '+') {
        if ((d.length === 11 || d.length === 12) && d.charAt(0) === '0') d = d.slice(1); // 0 + DDD + número
        if ((d.length === 10 || d.length === 11) && /^[1-9][1-9]/.test(d)) d = cc + d;
      }
      if (d.length < 8 || d.length > 15) return null;
      return d;
    },
    isBR: function (d) { return !!d && d.indexOf('55') === 0 && (d.length === 12 || d.length === 13); },
    // chave que ignora o 9º dígito (o WhatsApp guarda muitos celulares antigos sem ele)
    key: function (d) {
      if (!d) return '';
      if (Phone.isBR(d)) { var n = d.slice(4); return '55' + d.slice(2, 4) + (n.length === 9 ? n.slice(1) : n); }
      return d;
    },
    // forma completa atual (com o 9 nos celulares brasileiros)
    full: function (d) {
      if (Phone.isBR(d) && d.length === 12 && /[6-9]/.test(d.charAt(4))) return d.slice(0, 4) + '9' + d.slice(4);
      return d;
    },
    format: function (d) {
      if (!d) return '';
      var f = Phone.full(d);
      if (Phone.isBR(f)) {
        var ddd = f.slice(2, 4), n = f.slice(4);
        return '+55 (' + ddd + ') ' + (n.length === 9 ? n.slice(0, 5) + '-' + n.slice(5) : n.slice(0, 4) + '-' + n.slice(4));
      }
      return '+' + f;
    },
    // textos usados na busca: com e sem 55, com e sem o 9
    variants: function (d) {
      if (!d) return [];
      var out = [d];
      if (Phone.isBR(d)) {
        var ddd = d.slice(2, 4), n = d.slice(4), n8 = n.length === 9 ? n.slice(1) : n;
        out.push(ddd + n, ddd + n8, '55' + ddd + n8, n8);
        if (/[6-9]/.test(n8.charAt(0))) out.push('55' + ddd + '9' + n8, ddd + '9' + n8, '9' + n8);
      }
      var seen = {}, res = [];
      for (var i = 0; i < out.length; i++) if (!seen[out[i]]) { seen[out[i]] = 1; res.push(out[i]); }
      return res;
    },
    looksLike: function (s) {
      var c = clean(s).trim();
      return /^\+?[\d\s().\-]{8,22}$/.test(c) && Phone.digits(c).length >= 8;
    },
    // busca: a consulta (só dígitos) aparece em alguma variante?
    matches: function (d, q) {
      if (!d || !q) return false;
      var v = Phone.variants(d);
      for (var i = 0; i < v.length; i++) if (v[i].indexOf(q) !== -1) return true;
      return false;
    }
  };

  // ---------------------------------------------------------------- exportações (.txt)
  // Android: "06/11/2026 14:32 - Fulano: texto"   iPhone: "[06/11/2026, 14:32:10] Fulano: texto"
  var HDR_ANDROID = /^(\d{1,4})[\/.\-](\d{1,2})[\/.\-](\d{1,4}),?\s+(\d{1,2})[:.h](\d{2})(?:[:.](\d{2}))?\s*([AaPp]\.?\s?[Mm]\.?)?\s+-\s+/;
  var HDR_IOS = /^\[(\d{1,4})[\/.\-](\d{1,2})[\/.\-](\d{1,4}),?\s+(\d{1,2})[:.h](\d{2})(?:[:.](\d{2}))?\s*([AaPp]\.?\s?[Mm]\.?)?\]\s+/;
  var RE_ATT_ANDROID = /^(.+?)\s*\((?:arquivo anexado|file attached|archivo adjunto|fichier joint|Datei angehängt|file allegato)\)\s*$/i;
  var RE_ATT_IOS = /<(?:anexado|attached|adjunto|anexo|pièce jointe|Anhang|allegato):\s*([^>]+)>/i;
  var RE_OMIT = /^<\s*(?:Mídia oculta|Arquivo de mídia oculto|Media omitted|Multimedia omitido|Archivo omitido|Médias omis|Medien ausgeschlossen|Media omessi)\s*>$/i;
  var RE_OMIT_IOS = /^(imagem|vídeo|áudio|figurinha|documento|gif|cartão de contato|image|video|audio|sticker|document|contact card|imagen|vídeo|audio|sticker|documento|tarjeta de contacto)\s+(ocultad[oa]|omitid[oa]|omitted|omitida)$/i;
  var RE_DELETED = /^(Esta mensagem foi apagada|Você apagou esta mensagem|Mensagem apagada|This message was deleted|You deleted this message|Se eliminó este mensaje|Eliminaste este mensaje)\.?$/i;
  var RE_EDITED = /\s*<\s*(Mensagem editada|This message was edited|Se editó este mensaje)\s*>\s*$/i;
  var RE_GROUP_SYS = /(criou o grupo|criou este grupo|created group|created this group|adicionou|added|entrou usando|joined using|saiu|left|removeu|removed|creó el grupo|añadió|se unió)/i;
  var RE_SYS_PHRASES = /(criptografia de ponta a ponta|end-to-end encrypted|cifrad[oa]s de extremo a extremo|criou (o|este) grupo|created (group|this group)|adicionou|added|entrou usando|joined using|saiu|left|removeu|removed|mudou (o|a|para|seu)|changed (the|their|to|this)|código de segurança|security code|mensagens temporárias|disappearing messages|conta comercial|business account|Toque para saber mais|Tap to learn more|bloqueou|blocked|fixou|pinned)/i;
  var RE_OMIT_TAIL = /^(.*?)\s*(imagem|vídeo|áudio|figurinha|documento|gif|image|video|audio|sticker|document)\s+(omitid[oa]|ocultad[oa]|omitted)\s*$/i;
  var RE_TITLE = /^(?:Conversa do WhatsApp com|Conversa no WhatsApp com|Conversa do WhatsApp -|WhatsApp Chat with|WhatsApp Chat -|Chat de WhatsApp con|Chat de WhatsApp -|Discussion WhatsApp avec|WhatsApp Chat mit)\s*/i;
  var DAY = 86400000;

  function titleFromFileName(name) {
    var b = baseName(stripBidi(name)).replace(/\.(txt|zip)$/i, '').replace(/\s*\(\d+\)\s*$/, '').trim();
    if (!b || /^_?chat$/i.test(b) || /^WhatsApp Chat$/i.test(b)) return null;
    var pref = RE_TITLE.test(b);
    if (pref) b = b.replace(RE_TITLE, '').trim();
    else if (/^(archive|arquivo|download|export|exportação|conversa|chat|whatsapp)(\s|$|[-_])/i.test(b)) return null;
    // cópia renomeada pelo app Arquivos do iPhone: "Nome 2"
    if (!Phone.looksLike(b)) b = b.replace(/\s+\d{1,2}$/, '').trim();
    return b || null;
  }

  function pickFormat(lines) {
    var a = 0, i = 0, n = Math.min(lines.length, 400);
    for (var k = 0; k < n; k++) {
      var l = clean(lines[k]);
      if (HDR_ANDROID.test(l)) a++;
      else if (HDR_IOS.test(l)) i++;
    }
    if (!a && !i) return null;
    return i > a ? 'ios' : 'android';
  }
  function looksLikeExport(text) { return !!pickFormat(String(text).replace(/\r\n?/g, '\n').split('\n').slice(0, 60)); }

  function parseExportText(raw, opts) {
    opts = opts || {};
    var text = String(raw).replace(/^﻿/, '').replace(/\r\n?/g, '\n');
    var lines = text.split('\n');
    var fmt = pickFormat(lines);
    var res = { title: opts.fileName ? titleFromFileName(opts.fileName) : null, format: fmt, messages: [], authors: {}, sysAuthors: {}, groupHints: 0, dateOrder: 'dmy', lang: 'pt', folded: 0 };
    if (!fmt) return res;
    var RE = fmt === 'ios' ? HDR_IOS : HDR_ANDROID;
    var raws = [], cur = null;
    for (var k = 0; k < lines.length; k++) {
      var line = lines[k], cl = clean(line);
      var m = RE.exec(cl);
      if (m) {
        cur = { m: m, line: line, rest: [] };
        // corpo cru sem o cabeçalho (mantém U+200E para reconhecer avisos do iPhone)
        var rawNoHdr = line.replace(/^[‎‏‪-‮﻿]+/, '');
        var rm = RE.exec(clean(rawNoHdr));
        cur.rawBody = rm ? stripPrefix(rawNoHdr, rm[0].length) : cl.slice(m[0].length);
        raws.push(cur);
      } else if (cur) {
        cur.rest.push(line);
      }
    }
    // ordem da data (dia/mês ou mês/dia)
    var dmy = 0, mdy = 0, ymd = 0, r;
    for (r = 0; r < raws.length; r++) {
      var g = raws[r].m;
      if (g[1].length === 4) { ymd++; continue; }
      if (+g[1] > 12) dmy++; else if (+g[2] > 12) mdy++;
    }
    var en = /\((?:file attached)\)|<Media omitted>|<attached:|Messages and calls are end-to-end encrypted/.test(text);
    var es = /\(archivo adjunto\)|<Multimedia omitido>|<adjunto:/.test(text);
    res.lang = en ? 'en' : es ? 'es' : 'pt';
    res.dateOrder = ymd > dmy + mdy ? 'ymd' : dmy > mdy ? 'dmy' : mdy > dmy ? 'mdy' : (en ? 'mdy' : 'dmy');
    var count = {};
    for (r = 0; r < raws.length; r++) {
      var it = raws[r], gg = it.m, Y, M, D;
      if (res.dateOrder === 'ymd' || gg[1].length === 4) { Y = +gg[1]; M = +gg[2]; D = +gg[3]; }
      else if (res.dateOrder === 'mdy') { M = +gg[1]; D = +gg[2]; Y = +gg[3]; }
      else { D = +gg[1]; M = +gg[2]; Y = +gg[3]; }
      if (Y < 100) Y += 2000;
      var hh = +gg[4], mi = +gg[5], ss = gg[6] ? +gg[6] : 0, ap = gg[7] ? gg[7].replace(/[\s.]/g, '').toLowerCase() : '';
      if (ap === 'pm' && hh < 12) hh += 12;
      if (ap === 'am' && hh === 12) hh = 0;
      it.ts = (M >= 1 && M <= 12 && D >= 1 && D <= 31 && hh < 24 && mi < 60) ? new Date(Y, M - 1, D, hh, mi, ss).getTime() : NaN;
      var ci = indexOfAuthorSep(it.rawBody);
      it.author = ci > 0 ? stripBidi(it.rawBody.slice(0, ci)).trim() : null;
      it.body = ci > 0 ? it.rawBody.slice(ci + 2) : it.rawBody;
      if (it.author) count[it.author] = (count[it.author] || 0) + 1;
    }
    // Linha com cara de cabeçalho dentro de uma mensagem (ex.: um cronograma "12/11/2026 08:00 - demolição"):
    // a exportação é cronológica, então uma linha sem autor conhecido e fora da ordem do tempo volta para a mensagem anterior.
    var trusted = raws.map(function (x) { return isFinite(x.ts) && x.author && count[x.author] > 1; });
    var nextTs = new Array(raws.length), nx = null;
    for (r = raws.length - 1; r >= 0; r--) { nextTs[r] = nx; if (trusted[r]) nx = raws[r].ts; }
    var keep = [], prevTs = null, now = Date.now();
    for (r = 0; r < raws.length; r++) {
      var x = raws[r];
      if (!trusted[r]) {
        var odd = !isFinite(x.ts) || x.ts > now + DAY || (prevTs != null && x.ts < prevTs - DAY) || (nextTs[r] != null && x.ts > nextTs[r] + DAY);
        if (odd && keep.length) { var pv = keep[keep.length - 1]; pv.rest.push(x.line); for (var q = 0; q < x.rest.length; q++) pv.rest.push(x.rest[q]); res.folded++; continue; }
        if (!isFinite(x.ts)) continue;
      }
      keep.push(x);
      if (trusted[r]) prevTs = x.ts;
    }
    var seq = 0;
    for (var j = 0; j < keep.length; j++) {
      var kk = keep[j], author = kk.author;
      var full = kk.body + (kk.rest.length ? '\n' + kk.rest.join('\n') : '');
      var msg = parseBody(full, fmt, author);
      msg.ts = kk.ts; msg.author = author; msg.seq = seq++;
      if (msg.sys) {
        if (RE_GROUP_SYS.test(msg.text)) res.groupHints++;
        if (author) res.sysAuthors[author] = (res.sysAuthors[author] || 0) + 1;
      } else if (author) res.authors[author] = (res.authors[author] || 0) + 1;
      res.messages.push(msg);
    }
    return res;
  }
  function stripPrefix(rawLine, cleanLen) {
    // avança no texto cru até cobrir cleanLen caracteres "limpos"
    var c = 0, i = 0, inv = /[​-‏‪-‮⁦-⁩﻿]/;
    while (i < rawLine.length && c < cleanLen) {
      if (!inv.test(rawLine.charAt(i))) c++;
      i++;
    }
    return rawLine.slice(i);
  }
  function indexOfAuthorSep(body) {
    var i = body.indexOf(': ');
    if (i <= 0 || i > 90) return -1;
    return i;
  }
  function parseBody(full, fmt, author) {
    var lrm = /^\s*‎/.test(full);
    var t = stripBidi(full).replace(/^\s+/, '').replace(/\s+$/, '');
    var out = { text: t, kind: 'text', media: null, sys: 0, edited: 0 };
    if (!author) { out.sys = 1; out.kind = 'system'; return out; }
    if (RE_EDITED.test(t)) { out.edited = 1; t = t.replace(RE_EDITED, ''); out.text = t; }
    var lines2 = t.split('\n'), firstLine = lines2[0], restLines = lines2.slice(1).join('\n').trim();
    var ma = RE_ATT_ANDROID.exec(firstLine);
    if (ma) {
      var nm = ma[1].trim();
      out.media = { name: nm }; out.kind = kindOf(nm); out.text = restLines; return out;
    }
    var mi = RE_ATT_IOS.exec(t);
    if (mi) {
      var nm2 = mi[1].trim();
      out.media = { name: nm2 }; out.kind = kindOf(nm2);
      var before = t.slice(0, mi.index).trim(), after = t.slice(mi.index + mi[0].length).trim();
      // "Proposta.pdf • 3 páginas" é só a descrição do documento
      if (/•|·/.test(before) && /(página|pagina|page|hoja|seite)/i.test(before)) before = '';
      if (before && fold(before) === fold(displayFileName(nm2))) before = '';
      out.text = [before, after].filter(Boolean).join('\n');
      return out;
    }
    if (RE_OMIT.test(t)) { out.kind = 'omitted'; out.text = ''; return out; }
    var mo = RE_OMIT_IOS.exec(t);
    if (mo) { out.kind = 'omitted'; out.text = ''; out.omittedType = mo[1].toLowerCase(); return out; }
    var mt = RE_OMIT_TAIL.exec(t);
    if (mt && t.indexOf('\n') < 0) {
      out.kind = 'omitted'; out.text = ''; out.omittedType = mt[2].toLowerCase();
      var fn = /^(.+?\.[a-z0-9]{2,5})(\s*[•·].*)?$/i.exec(mt[1].trim());
      if (fn) out.media = { name: fn[1].trim() };
      return out;
    }
    if (RE_DELETED.test(t)) { out.kind = 'deleted'; return out; }
    if (t === 'null') { out.kind = 'other'; out.text = ''; return out; }
    if (fmt === 'ios' && lrm && RE_SYS_PHRASES.test(t)) { out.sys = 1; out.kind = 'system'; }
    return out;
  }

  // Quem é o contato e quem sou eu numa conversa exportada.
  // Na dúvida, não marca ninguém como "eu" (melhor mostrar o nome do autor do que trocar os lados).
  function identifyExport(parsed, meNamesFolded, fileName) {
    meNamesFolded = meNamesFolded || {};
    var title = parsed.title || null;
    var authors = Object.keys(parsed.authors);
    var sysAuthors = Object.keys(parsed.sysAuthors || {});
    var me = {}, other = null, sure = false, k;
    var titleFold = title ? fold(title) : '';
    var titlePhone = title && Phone.looksLike(title) ? Phone.normalize(title) : null;
    function isTitle(a) {
      var fa = fold(a);
      if (titleFold && (fa === titleFold || fa.replace(/\s+\d{1,2}$/, '') === titleFold)) return true;
      if (titlePhone && Phone.looksLike(a)) return Phone.key(Phone.normalize(a)) === Phone.key(titlePhone);
      return false;
    }
    var isGroup = authors.length > 2 || parsed.groupHints > 0;
    if (!isGroup) {
      for (k = 0; k < authors.length; k++) if (isTitle(authors[k])) { other = authors[k]; sure = true; }
      if (!other) {
        // iPhone: o aviso de criptografia vem no nome do contato
        for (k = 0; k < sysAuthors.length; k++) if (authors.indexOf(sysAuthors[k]) >= 0 && !meNamesFolded[fold(sysAuthors[k])]) { other = sysAuthors[k]; sure = true; }
      }
      if (!other) {
        var notMine = authors.filter(function (a) { return !meNamesFolded[fold(a)]; });
        if (authors.length === 2 && notMine.length === 1) { other = notMine[0]; sure = true; }
        else if (authors.length === 1 && notMine.length === 1) {
          // só uma pessoa escreveu e ela não é o contato do título: quem escreveu foi você
          if (title || sysAuthors.length) me[authors[0]] = 1;
          else other = authors[0];
        }
      }
      if (sure) for (k = 0; k < authors.length; k++) if (authors[k] !== other) me[authors[k]] = 1;
    }
    for (k = 0; k < authors.length; k++) if (authors[k] !== other && meNamesFolded[fold(authors[k])]) me[authors[k]] = 1;
    var phone = titlePhone || (other && Phone.looksLike(other) ? Phone.normalize(other) : null);
    var name;
    if (isGroup) name = title || 'Grupo';
    else if (titlePhone) name = null;
    else name = (other && !Phone.looksLike(other)) ? other : title;
    var id = isGroup ? 'g:' + slug(title || fileName || 'grupo') : phone ? 'p:' + Phone.key(phone) : 'n:' + slug(name || fileName || 'contato');
    return { id: id, name: name || null, phone: phone, isGroup: isGroup, me: me, other: other, inferredMe: !isGroup && sure ? authors.filter(function (a) { return a !== other; }) : [] };
  }

  // chave para não duplicar a mesma mensagem vinda de fontes diferentes
  var MEDIA_KINDS = { image: 1, audio: 1, video: 1, doc: 1, sticker: 1, omitted: 1 };
  function msgBodyKey(ts, me, text, mediaName, kind) {
    var minute = Math.floor(ts / 60000);
    var body = (mediaName || MEDIA_KINDS[kind]) ? 'm' : 't:' + fold(text).slice(0, 300);
    return hash(minute + '|' + (me ? 1 : 0) + '|' + body);
  }
  function makeKeyer(cid) {
    var seen = {};
    return function (ts, me, text, mediaName, kind) {
      var b = msgBodyKey(ts, me, text, mediaName, kind);
      var n = (seen[b] = (seen[b] || 0) + 1);
      return cid + '|' + b + (n > 1 ? '.' + n : '');
    };
  }

  // ---------------------------------------------------------------- vCard (.vcf)
  function qpDecode(s) {
    var bytes = [], i = 0;
    s = s.replace(/=\r?\n/g, '');
    while (i < s.length) {
      var c = s.charAt(i);
      if (c === '=' && /^[0-9A-Fa-f]{2}$/.test(s.substr(i + 1, 2))) { bytes.push(parseInt(s.substr(i + 1, 2), 16)); i += 3; }
      else { var code = s.charCodeAt(i); if (code < 128) bytes.push(code); else { var e = new TextEncoder().encode(c); for (var j = 0; j < e.length; j++) bytes.push(e[j]); } i++; }
    }
    return new TextDecoder('utf-8').decode(new Uint8Array(bytes));
  }
  function parseVcf(text) {
    var t = String(text).replace(/\r\n?/g, '\n');
    t = t.replace(/=\n/g, '=\u0001'); // linha suave do quoted-printable
    t = t.replace(/\n[ \t]/g, '');
    t = t.replace(/=\u0001/g, '=\n');
    var cards = [], cur = null;
    t.split('\n').forEach(function (line) {
      if (/^BEGIN:VCARD/i.test(line)) { cur = { name: '', n: '', phones: [] }; return; }
      if (/^END:VCARD/i.test(line)) { if (cur) { if (!cur.name && cur.n) cur.name = cur.n; if (cur.phones.length) cards.push(cur); } cur = null; return; }
      if (!cur) return;
      var ci = line.indexOf(':'); if (ci < 0) return;
      var left = line.slice(0, ci), val = line.slice(ci + 1);
      var prop = left.split(';')[0].replace(/^item\d+\./i, '').toUpperCase();
      if (/ENCODING=QUOTED-PRINTABLE/i.test(left)) val = qpDecode(val);
      val = val.replace(/\\,/g, ',').replace(/\\;/g, ';').replace(/\\n/gi, ' ').trim();
      if (prop === 'FN') cur.name = val;
      else if (prop === 'N' && !cur.n) cur.n = val.split(';').filter(Boolean).reverse().join(' ').trim();
      else if (prop === 'TEL') { var p = Phone.normalize(val.replace(/^tel:/i, '')); if (p) cur.phones.push(p); }
    });
    return cards;
  }

  // ---------------------------------------------------------------- CRC32 e ZIP
  var CRC_TABLE = (function () {
    var t = new Uint32Array(256);
    for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t;
  })();
  function crc32Update(crc, u8) {
    var c = crc ^ 0xffffffff;
    for (var i = 0; i < u8.length; i++) c = CRC_TABLE[(c ^ u8[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }
  async function crc32Blob(blob) {
    var crc = 0, CH = 4 * 1024 * 1024;
    for (var off = 0; off < blob.size; off += CH) {
      var buf = new Uint8Array(await blob.slice(off, Math.min(blob.size, off + CH)).arrayBuffer());
      crc = crc32Update(crc, buf);
    }
    return crc;
  }
  function utf8(s) { return new TextEncoder().encode(s); }

  // nomes de arquivo em .zip feitos no Windows sem UTF-8 (página de código 850, a do Brasil)
  var CP850 = "ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌█▄¦Ì▀ÓßÔÒõÕµþÞÚÛÙýÝ¯´­±‗¾¶§÷¸°¨·¹³²■ ";
  function cp850(bytes) { var o = ''; for (var i = 0; i < bytes.length; i++) o += bytes[i] < 128 ? String.fromCharCode(bytes[i]) : CP850.charAt(bytes[i] - 128); return o; }
  function ZipReader(blob) { this.src = blob; this.entries = []; }
  ZipReader.prototype.bytes = async function (start, len) {
    return new Uint8Array(await this.src.slice(start, start + len).arrayBuffer());
  };
  ZipReader.prototype.open = async function () {
    var size = this.src.size;
    if (size < 22) throw new Error('Arquivo .zip vazio ou incompleto.');
    var tailLen = Math.min(size, 65535 + 22 + 20);
    var tailStart = size - tailLen;
    var tail = await this.bytes(tailStart, tailLen);
    var dv = new DataView(tail.buffer, tail.byteOffset, tail.byteLength), eocd = -1;
    for (var i = tail.length - 22; i >= 0; i--) { if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; } }
    if (eocd < 0) throw new Error('Este arquivo não parece ser um .zip válido.');
    var count = dv.getUint16(eocd + 10, true), cdSize = dv.getUint32(eocd + 12, true), cdOff = dv.getUint32(eocd + 16, true);
    if ((count === 0xffff || cdSize === 0xffffffff || cdOff === 0xffffffff) && eocd >= 20 && dv.getUint32(eocd - 20, true) === 0x07064b50) {
      var z64off = Number(dv.getBigUint64(eocd - 20 + 8, true));
      var z = await this.bytes(z64off, 56), zd = new DataView(z.buffer, z.byteOffset, 56);
      if (zd.getUint32(0, true) === 0x06064b50) {
        count = Number(zd.getBigUint64(32, true)); cdSize = Number(zd.getBigUint64(40, true)); cdOff = Number(zd.getBigUint64(48, true));
      }
    }
    var cd = await this.bytes(cdOff, cdSize), cv = new DataView(cd.buffer, cd.byteOffset, cd.byteLength), p = 0;
    var out = [];
    while (p + 46 <= cd.length && cv.getUint32(p, true) === 0x02014b50) {
      var flags = cv.getUint16(p + 8, true), method = cv.getUint16(p + 10, true);
      var dtime = cv.getUint16(p + 12, true), ddate = cv.getUint16(p + 14, true);
      var crc = cv.getUint32(p + 16, true), csize = cv.getUint32(p + 20, true), usize = cv.getUint32(p + 24, true);
      var nl = cv.getUint16(p + 28, true), xl = cv.getUint16(p + 30, true), cl = cv.getUint16(p + 32, true);
      var loff = cv.getUint32(p + 42, true);
      var nameBytes = cd.subarray(p + 46, p + 46 + nl), name;
      if (flags & 0x800) name = new TextDecoder('utf-8').decode(nameBytes);
      else { try { name = new TextDecoder('utf-8', { fatal: true }).decode(nameBytes); } catch (e) { name = cp850(nameBytes); } }
      var x = p + 46 + nl, xe = x + xl;
      while (x + 4 <= xe) {
        var id = cv.getUint16(x, true), sz = cv.getUint16(x + 2, true), q = x + 4;
        if (id === 0x0001) {
          if (usize === 0xffffffff) { usize = Number(cv.getBigUint64(q, true)); q += 8; }
          if (csize === 0xffffffff) { csize = Number(cv.getBigUint64(q, true)); q += 8; }
          if (loff === 0xffffffff) { loff = Number(cv.getBigUint64(q, true)); q += 8; }
        }
        x += 4 + sz;
      }
      var date = new Date(1980 + (ddate >> 9), ((ddate >> 5) & 15) - 1, ddate & 31, dtime >> 11, (dtime >> 5) & 63, (dtime & 31) * 2);
      if (!/\/$/.test(name)) out.push({ name: name, method: method, csize: csize, size: usize, offset: loff, crc: crc, date: date, flags: flags });
      p += 46 + nl + xl + cl;
    }
    this.entries = out;
    return out;
  };
  ZipReader.prototype.blob = async function (e, type) {
    var lh = await this.bytes(e.offset, 30), lv = new DataView(lh.buffer, lh.byteOffset, 30);
    if (lv.getUint32(0, true) !== 0x04034b50) throw new Error('Parte do .zip danificada: ' + e.name);
    var start = e.offset + 30 + lv.getUint16(26, true) + lv.getUint16(28, true);
    var raw = this.src.slice(start, start + e.csize);
    type = type || mimeOf(e.name);
    if (e.flags & 1) throw new Error('Arquivo protegido por senha dentro do .zip: ' + e.name);
    if (e.method === 0) return raw.slice(0, raw.size, type);
    if (e.method === 8) {
      var ds = raw.stream().pipeThrough(new DecompressionStream('deflate-raw'));
      var b = await new Response(ds).blob();
      return new Blob([b], { type: type });
    }
    throw new Error('Compressão não suportada (' + e.method + ') em ' + e.name);
  };
  ZipReader.prototype.text = async function (e) {
    var b = await this.blob(e, 'text/plain');
    return decodeText(new Uint8Array(await b.arrayBuffer()));
  };

  function dosTime(d) { return ((d.getHours() << 11) | (d.getMinutes() << 5) | (Math.floor(d.getSeconds() / 2))) & 0xffff; }
  function dosDate(d) { var y = Math.max(1980, d.getFullYear()); return (((y - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate()) & 0xffff; }
  // Grava .zip sem compressão (PDF e fotos já são comprimidos). Suporta ZIP64.
  function ZipWriter() { this.parts = []; this.cd = []; this.offset = 0; this.names = {}; }
  ZipWriter.prototype.uniqueName = function (name) {
    var n = name, i = 2, dot = name.lastIndexOf('.'), stem = dot > name.lastIndexOf('/') ? name.slice(0, dot) : name, ext = dot > name.lastIndexOf('/') ? name.slice(dot) : '';
    while (this.names[n.toLowerCase()]) n = stem + ' (' + (i++) + ')' + ext;
    this.names[n.toLowerCase()] = 1;
    return n;
  };
  ZipWriter.prototype.add = async function (name, data, mtime) {
    var blob = data instanceof Blob ? data : new Blob([data]);
    name = this.uniqueName(name);
    var crc = await crc32Blob(blob), size = blob.size, nb = utf8(name), d = mtime || new Date();
    var big = size >= 0xffffffff || this.offset >= 0xffffffff;
    var h = new Uint8Array(30 + nb.length + (big ? 20 : 0)), v = new DataView(h.buffer);
    v.setUint32(0, 0x04034b50, true); v.setUint16(4, big ? 45 : 20, true); v.setUint16(6, 0x0800, true); v.setUint16(8, 0, true);
    v.setUint16(10, dosTime(d), true); v.setUint16(12, dosDate(d), true); v.setUint32(14, crc, true);
    v.setUint32(18, big ? 0xffffffff : size, true); v.setUint32(22, big ? 0xffffffff : size, true);
    v.setUint16(26, nb.length, true); v.setUint16(28, big ? 20 : 0, true); h.set(nb, 30);
    if (big) { var q = 30 + nb.length; v.setUint16(q, 1, true); v.setUint16(q + 2, 16, true); v.setBigUint64(q + 4, BigInt(size), true); v.setBigUint64(q + 12, BigInt(size), true); }
    this.cd.push({ nb: nb, crc: crc, size: size, offset: this.offset, time: dosTime(d), date: dosDate(d) });
    this.parts.push(h, blob);
    this.offset += h.length + size;
    return name;
  };
  ZipWriter.prototype.finish = function () {
    var cdStart = this.offset, cdParts = [], cdLen = 0;
    for (var i = 0; i < this.cd.length; i++) {
      var e = this.cd[i], big = e.size >= 0xffffffff || e.offset >= 0xffffffff;
      var r = new Uint8Array(46 + e.nb.length + (big ? 28 : 0)), v = new DataView(r.buffer);
      v.setUint32(0, 0x02014b50, true); v.setUint16(4, big ? 45 : 20, true); v.setUint16(6, big ? 45 : 20, true);
      v.setUint16(8, 0x0800, true); v.setUint16(10, 0, true); v.setUint16(12, e.time, true); v.setUint16(14, e.date, true);
      v.setUint32(16, e.crc, true); v.setUint32(20, big ? 0xffffffff : e.size, true); v.setUint32(24, big ? 0xffffffff : e.size, true);
      v.setUint16(28, e.nb.length, true); v.setUint16(30, big ? 28 : 0, true); v.setUint32(42, big ? 0xffffffff : e.offset, true);
      r.set(e.nb, 46);
      if (big) { var q = 46 + e.nb.length; v.setUint16(q, 1, true); v.setUint16(q + 2, 24, true); v.setBigUint64(q + 4, BigInt(e.size), true); v.setBigUint64(q + 12, BigInt(e.size), true); v.setBigUint64(q + 20, BigInt(e.offset), true); }
      cdParts.push(r); cdLen += r.length;
    }
    var n = this.cd.length, need64 = n >= 0xffff || cdStart >= 0xffffffff || cdLen >= 0xffffffff, tail = [];
    if (need64) {
      var z = new Uint8Array(56), zv = new DataView(z.buffer);
      zv.setUint32(0, 0x06064b50, true); zv.setBigUint64(4, 44n, true); zv.setUint16(12, 45, true); zv.setUint16(14, 45, true);
      zv.setBigUint64(24, BigInt(n), true); zv.setBigUint64(32, BigInt(n), true); zv.setBigUint64(40, BigInt(cdLen), true); zv.setBigUint64(48, BigInt(cdStart), true);
      var loc = new Uint8Array(20), lv = new DataView(loc.buffer);
      lv.setUint32(0, 0x07064b50, true); lv.setBigUint64(8, BigInt(cdStart + cdLen), true); lv.setUint32(16, 1, true);
      tail.push(z, loc);
    }
    var eo = new Uint8Array(22), ev = new DataView(eo.buffer);
    ev.setUint32(0, 0x06054b50, true); ev.setUint16(8, need64 ? 0xffff : n, true); ev.setUint16(10, need64 ? 0xffff : n, true);
    ev.setUint32(12, need64 ? 0xffffffff : cdLen, true); ev.setUint32(16, need64 ? 0xffffffff : cdStart, true);
    tail.push(eo);
    return new Blob(this.parts.concat(cdParts, tail), { type: 'application/zip' });
  };

  // ---------------------------------------------------------------- backup criptografado (crypt15)
  function cleanKey(s) { return String(s || '').replace(/[^0-9a-fA-F]/g, '').toLowerCase(); }
  function hexToBytes(h) { var u = new Uint8Array(h.length / 2); for (var i = 0; i < u.length; i++) u[i] = parseInt(h.substr(i * 2, 2), 16); return u; }
  function readVarint(u8, p) {
    var v = 0, s = 0, b;
    do { if (p.i >= u8.length) throw new Error('protobuf'); b = u8[p.i++]; v += (b & 0x7f) * Math.pow(2, s); s += 7; } while (b & 0x80 && s < 64);
    return v;
  }
  // lê os campos de primeiro nível de uma mensagem protobuf
  function pbFields(u8) {
    var p = { i: 0 }, out = [];
    while (p.i < u8.length) {
      var tag = readVarint(u8, p), f = Math.floor(tag / 8), wt = tag & 7;
      if (wt === 0) out.push({ f: f, v: readVarint(u8, p) });
      else if (wt === 2) { var len = readVarint(u8, p); if (p.i + len > u8.length) throw new Error('protobuf'); out.push({ f: f, b: u8.subarray(p.i, p.i + len) }); p.i += len; }
      else if (wt === 1) p.i += 8;
      else if (wt === 5) p.i += 4;
      else throw new Error('protobuf');
    }
    return out;
  }
  // Cabeçalho: [tamanho em varint][protobuf BackupPrefix][dados][tag GCM 16][MD5 16, opcional]
  function readHeaderAt(u8, start, size) {
    var pb = u8.subarray(start, start + size), r = { iv: null, version: '', suffix: '', c14: false, keyType: null };
    pbFields(pb).forEach(function (fl) {
      if (fl.f === 3 && fl.b) pbFields(fl.b).forEach(function (g) { if (g.f === 1 && g.b) r.iv = g.b.slice(); });
      if (fl.f === 2 && fl.b) r.c14 = true;
      if (fl.f === 6 && fl.v != null) r.keyType = fl.v;
      if (fl.f === 4 && fl.b) {
        try { pbFields(fl.b).forEach(function (g) { if (g.f === 1 && g.b) r.version = new TextDecoder().decode(g.b); if (g.f === 3 && g.b) r.suffix = new TextDecoder().decode(g.b); }); } catch (e) { }
      }
    });
    if (r.iv && r.iv.length !== 16) r.iv = null;
    r.dataStart = start + size;
    return r;
  }
  function parseCrypt15Header(u8) {
    if (u8.length < 64) throw new Error('Arquivo de backup pequeno demais.');
    var tries = [], p = { i: 0 };
    try { var n = readVarint(u8, p); tries.push([p.i, n]); } catch (e) { }
    tries.push([u8[1] === 1 ? 2 : 1, u8[0]]); // layout antigo: 1 byte de tamanho + 0x01
    var hdr = null, c14 = false, kt = null;
    for (var t = 0; t < tries.length && !hdr; t++) {
      try {
        var r = readHeaderAt(u8, tries[t][0], tries[t][1]);
        if (r.c14) c14 = true;
        if (r.keyType != null) kt = r.keyType;
        if (r.iv) hdr = r;
      } catch (e) { }
    }
    if (!hdr && c14) throw new Error('Este backup é do tipo antigo (.crypt14). Ele só abre com uma chave escondida dentro do celular. No S22, ative o backup com chave de 64 dígitos e faça um backup novo (veja o passo a passo).');
    if (!hdr) throw new Error('Não reconheci este arquivo como backup do WhatsApp (.crypt15).');
    if (kt === 2 || kt === 4) hdr.lockedBy = kt === 2 ? 'senha' : 'chave de acesso (passkey)';
    return { iv: hdr.iv, dataStart: hdr.dataStart, appVersion: hdr.version, phoneEnd: hdr.suffix, keyType: kt, lockedBy: hdr.lockedBy || null };
  }
  async function inflateZlib(u8) {
    var ds = new Blob([u8]).stream().pipeThrough(new DecompressionStream('deflate'));
    return new Uint8Array(await new Response(ds).arrayBuffer());
  }
  var SQLITE_MAGIC = 'SQLite format 3';
  function isSqlite(u8) { if (!u8 || u8.length < 16) return false; for (var i = 0; i < 15; i++) if (u8[i] !== SQLITE_MAGIC.charCodeAt(i)) return false; return true; }
  // GCM com IV de 16 bytes, feito como AES-CTR (para navegadores que não aceitam esse IV no AES-GCM)
  function bytesToBig(b) { var x = 0n; for (var i = 0; i < b.length; i++) x = (x << 8n) | BigInt(b[i]); return x; }
  function bigToBytes(x) { var b = new Uint8Array(16); for (var i = 15; i >= 0; i--) { b[i] = Number(x & 0xffn); x >>= 8n; } return b; }
  function gfmul(X, Y) {
    var R = 0xe1n << 120n, Z = 0n, V = Y;
    for (var i = 127; i >= 0; i--) { if ((X >> BigInt(i)) & 1n) Z ^= V; V = (V & 1n) ? ((V >> 1n) ^ R) : (V >> 1n); }
    return Z;
  }
  async function gcmViaCtr(subtle, rawKey, iv, data) {
    var cbc = await subtle.importKey('raw', rawKey, 'AES-CBC', false, ['encrypt']);
    var Hb = new Uint8Array(await subtle.encrypt({ name: 'AES-CBC', iv: new Uint8Array(16) }, cbc, new Uint8Array(16))).slice(0, 16);
    var H = bytesToBig(Hb), y = 0n;
    var blocks = [iv];
    if (iv.length % 16) { var padded = new Uint8Array(Math.ceil(iv.length / 16) * 16); padded.set(iv); blocks = [padded]; }
    for (var bi = 0; bi < blocks[0].length; bi += 16) y = gfmul(y ^ bytesToBig(blocks[0].subarray(bi, bi + 16)), H);
    y = gfmul(y ^ BigInt(iv.length * 8), H);
    var j0 = bigToBytes(y), ctr = j0.slice();
    var c = ((ctr[12] << 24) | (ctr[13] << 16) | (ctr[14] << 8) | ctr[15]) >>> 0; c = (c + 1) >>> 0;
    ctr[12] = c >>> 24; ctr[13] = (c >>> 16) & 255; ctr[14] = (c >>> 8) & 255; ctr[15] = c & 255;
    var k = await subtle.importKey('raw', rawKey, 'AES-CTR', false, ['decrypt']);
    return new Uint8Array(await subtle.decrypt({ name: 'AES-CTR', counter: ctr, length: 32 }, k, data));
  }
  async function decryptCrypt15(buf, keyText) {
    var u8 = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
    if (isSqlite(u8)) return { sqlite: u8, info: { plain: true } };
    var hex = cleanKey(keyText);
    if (hex.length !== 64) throw new Error('A chave precisa ter 64 caracteres (números de 0 a 9 e letras de a até f). Você digitou ' + hex.length + '.');
    var hdr = parseCrypt15Header(u8);
    var subtle = (root.crypto || globalThis.crypto).subtle;
    var ikm = await subtle.importKey('raw', hexToBytes(hex), 'HKDF', false, ['deriveBits']);
    var bits = new Uint8Array(await subtle.deriveBits({ name: 'HKDF', hash: 'SHA-256', salt: new Uint8Array(32), info: utf8('backup encryption') }, ikm, 256));
    var key = await subtle.importKey('raw', bits, 'AES-GCM', false, ['decrypt']);
    var plain = null, ends = [u8.length - 16, u8.length]; // com e sem os 16 bytes finais de checagem (MD5)
    for (var i = 0; i < ends.length && !plain; i++) {
      try { plain = new Uint8Array(await subtle.decrypt({ name: 'AES-GCM', iv: hdr.iv, tagLength: 128 }, key, u8.subarray(hdr.dataStart, ends[i]))); }
      catch (e) { plain = null; }
    }
    if (!plain) {
      // plano B: alguns navegadores recusam IV de 16 bytes no AES-GCM; o conteúdo é conferido depois (zlib + SQLite)
      try {
        var p2 = await gcmViaCtr(subtle, bits, hdr.iv, u8.subarray(hdr.dataStart, u8.length - 32));
        if (p2[0] === 0x78) { var t = await inflateZlib(p2).catch(function () { return null; }); if (t && (isSqlite(t) || (t[0] === 0x50 && t[1] === 0x4b))) plain = p2; }
      } catch (e) { }
    }
    if (!plain) {
      if (hdr.lockedBy) throw new Error('Este backup foi protegido com ' + hdr.lockedBy + ', não com a chave de 64 dígitos, e por isso não abre fora do WhatsApp. No S22, desative o backup criptografado, ative de novo escolhendo “Usar chave de criptografia de 64 dígitos” e faça um backup novo.');
      throw new Error('A chave não abriu este backup. Confira os 64 caracteres e se o arquivo é o backup feito depois de ativar essa chave.');
    }
    var out = plain;
    if (plain[0] === 0x78) out = await inflateZlib(plain);
    if (!isSqlite(out)) {
      if (out[0] === 0x50 && out[1] === 0x4b) return { zip: out, info: hdr };
      throw new Error('O backup abriu, mas o conteúdo não é o banco de conversas. Escolha o arquivo msgstore.db.crypt15.');
    }
    return { sqlite: out, info: hdr };
  }

  // ---------------------------------------------------------------- msgstore.db (SQLite do WhatsApp)
  var TYPE_MAP = { 0: 'text', 1: 'image', 2: 'audio', 3: 'video', 4: 'contact', 5: 'location', 9: 'doc', 13: 'video', 14: 'contact', 15: 'deleted', 16: 'location', 20: 'sticker', 42: 'image', 43: 'video', 64: 'deleted', 81: 'video', 82: 'audio' };
  var SKIP_TYPES = { 7: 1, 8: 1, 10: 1, 11: 1, 12: 1, 18: 1, 19: 1, 31: 1, 36: 1, 90: 1, 99: 1, 112: 1, 116: 1 };
  function cols(db, table) {
    try { var r = db.exec('PRAGMA table_info(' + table + ')'); return r.length ? r[0].values.map(function (v) { return v[1]; }) : []; }
    catch (e) { return []; }
  }
  function tables(db) {
    var r = db.exec("SELECT name FROM sqlite_master WHERE type='table'");
    return r.length ? r[0].values.map(function (v) { return v[0]; }) : [];
  }
  function relMediaPath(p) {
    if (!p) return '';
    p = String(p).replace(/\\/g, '/');
    var i = p.search(/(^|\/)Media\//);
    return i >= 0 ? p.slice(p.charAt(i) === '/' ? i + 1 : i) : p.replace(/^\/+/, '');
  }
  // Abre o banco e entrega conversas e depois mensagens em lotes (next()), para o chamador gravar sem estourar memória
  function openMsgStore(SQL, bytes) {
    var db = new SQL.Database(bytes), has = {};
    tables(db).forEach(function (t) { has[t] = 1; });
    var cur;
    try {
      if (has.message && has.chat && has.jid) cur = modernCursor(db, has);
      else if (has.messages) cur = legacyCursor(db, has);
      else throw new Error('Este banco não tem as tabelas de conversas do WhatsApp.');
    } catch (e) { db.close(); throw e; }
    var closed = false;
    cur.close = function () { if (closed) return; closed = true; try { cur.free(); } catch (e) { } db.close(); };
    return cur;
  }
  function readMsgStore(SQL, bytes, H) {
    var cur = openMsgStore(SQL, bytes), b;
    try {
      if (H.onChats) H.onChats(cur.chats);
      while ((b = cur.next())) H.onMessages(b);
    } finally { cur.close(); }
    return cur;
  }
  function modernCursor(db, has) {
    var jid = {}, r;
    var jc = cols(db, 'jid');
    r = db.exec('SELECT _id, user, server' + (jc.indexOf('raw_string') >= 0 ? ', raw_string' : ", ''") + ' FROM jid');
    if (r.length) r[0].values.forEach(function (v) { jid[v[0]] = { user: v[1] == null ? '' : String(v[1]), server: v[2] || '', raw: v[3] || '' }; });
    var lidTo = {};
    if (has.jid_map) {
      var mc = cols(db, 'jid_map');
      if (mc.indexOf('lid_row_id') >= 0 && mc.indexOf('jid_row_id') >= 0) {
        r = db.exec('SELECT lid_row_id, jid_row_id FROM jid_map');
        if (r.length) r[0].values.forEach(function (v) { lidTo[v[0]] = v[1]; });
      }
    }
    function phoneOf(jidId) {
      var j = jid[jidId]; if (!j) return null;
      if (j.server === 'lid' && lidTo[jidId] != null) j = jid[lidTo[jidId]] || j;
      if (j.server === 's.whatsapp.net' || j.server === 'c.us') { var d = Phone.digits(j.user); return d.length >= 8 ? d : null; }
      return null;
    }
    var cc = cols(db, 'chat');
    r = db.exec('SELECT _id, jid_row_id' + (cc.indexOf('subject') >= 0 ? ', subject' : ', NULL') + ' FROM chat');
    var chats = {};
    if (r.length) r[0].values.forEach(function (v) {
      var j = jid[v[1]]; if (!j) return;
      var srv = j.server, info = { rowId: v[0], jid: j.raw || (j.user + '@' + srv), subject: v[2] || null };
      if (srv === 'g.us') { info.isGroup = true; info.id = 'g:' + slug(j.user || info.jid); }
      else if (srv === 'broadcast' || srv === 'newsletter' || srv === 'call' || /status/.test(j.user)) return;
      else {
        var ph = phoneOf(v[1]);
        if (ph) { info.phone = ph; info.id = 'p:' + Phone.key(ph); }
        else { info.id = 'l:' + slug(j.user || info.jid); info.lid = true; }
      }
      chats[v[0]] = info;
    });
    var mc2 = cols(db, 'message'), md = has.message_media ? cols(db, 'message_media') : [];
    function c(table, list, name, alias) { return list.indexOf(name) >= 0 ? table + '.' + name + ' AS ' + alias : 'NULL AS ' + alias; }
    var sql = 'SELECT m._id AS id, m.chat_row_id AS chat, ' + c('m', mc2, 'from_me', 'me') + ', m.timestamp AS ts, ' + c('m', mc2, 'message_type', 'type') + ', ' + c('m', mc2, 'text_data', 'text') + ', ' + c('m', mc2, 'sender_jid_row_id', 'sender') + ', ' + c('m', mc2, 'key_id', 'kid');
    if (md.length) sql += ', ' + c('mm', md, 'file_path', 'path') + ', ' + c('mm', md, 'mime_type', 'mime') + ', ' + c('mm', md, 'media_name', 'mname') + ', ' + c('mm', md, 'file_size', 'fsize') + ', ' + c('mm', md, 'media_caption', 'cap') + ' FROM message m LEFT JOIN message_media mm ON mm.message_row_id = m._id';
    else sql += ', NULL AS path, NULL AS mime, NULL AS mname, NULL AS fsize, NULL AS cap FROM message m';
    sql += ' WHERE m.chat_row_id IS NOT NULL AND m.timestamp > 0 ORDER BY m.chat_row_id, m.timestamp, m._id';
    var total = 0;
    try { var cr = db.exec('SELECT COUNT(*) FROM message'); total = cr.length ? cr[0].values[0][0] : 0; } catch (e) { }
    var st = db.prepare(sql), senderCache = {}, done = false;
    var cur = { chats: Object.keys(chats).map(function (k) { return chats[k]; }), total: total, read: 0, kind: 'modern' };
    cur.free = function () { st.free(); };
    cur.next = function () {
      if (done) return null;
      var batch = [];
      while (batch.length < 2000) {
        if (!st.step()) { done = true; break; }
        var o = st.getAsObject(); cur.read++;
        var ch = chats[o.chat]; if (!ch) continue;
        var ty = o.type == null ? 0 : +o.type;
        if (SKIP_TYPES[ty] && !o.path) continue;
        var kind = TYPE_MAP[ty] || (o.path ? kindOf(o.path, o.mime) : (o.text ? 'text' : null));
        if (!kind) continue;
        var text = o.text == null ? '' : String(o.text);
        if (!text && o.cap) text = String(o.cap);
        if (kind === 'text' && !text) continue;
        var m = { ts: +o.ts, me: o.me ? 1 : 0, kind: kind, text: text, seq: +o.id, keyId: o.kid ? String(o.kid) : null };
        if (ty === 15 || ty === 64) { m.kind = 'deleted'; m.text = m.me ? 'Você apagou esta mensagem' : 'Esta mensagem foi apagada'; }
        else if (o.path || o.mname) {
          var rel = relMediaPath(o.path);
          var nm = rel ? baseName(rel) : String(o.mname || '');
          m.media = { name: nm, path: rel, mime: o.mime || mimeOf(nm), size: o.fsize ? +o.fsize : 0, orig: o.mname ? String(o.mname) : '' };
          var k2 = kindOf(nm || o.mname, o.mime);
          m.kind = k2 === 'sticker' ? 'sticker' : (ty === 9 ? 'doc' : (TYPE_MAP[ty] || k2));
        }
        if (ch.isGroup && !m.me && o.sender != null) {
          if (!(o.sender in senderCache)) senderCache[o.sender] = phoneOf(o.sender);
          m.authorPhone = senderCache[o.sender];
        }
        m.chatId = ch.id;
        batch.push(m);
      }
      return batch.length || !done ? batch : null;
    };
    return cur;
  }
  function legacyCursor(db, has) {
    var mc = cols(db, 'messages');
    function c(name, alias) { return mc.indexOf(name) >= 0 ? name + ' AS ' + alias : 'NULL AS ' + alias; }
    var subj = {};
    if (has.chat_list) {
      try {
        var r = db.exec('SELECT key_remote_jid, subject FROM chat_list');
        if (r.length) r[0].values.forEach(function (v) { if (v[1]) subj[v[0]] = v[1]; });
      } catch (e) { }
    }
    var chats = {};
    var rj = db.exec("SELECT DISTINCT key_remote_jid FROM messages WHERE key_remote_jid IS NOT NULL");
    if (rj.length) rj[0].values.forEach(function (v) {
      var j = String(v[0] || ''), at = j.indexOf('@'), user = at > 0 ? j.slice(0, at) : j, srv = at > 0 ? j.slice(at + 1) : '';
      if (at < 0 || user === '-1' || srv === 'broadcast' || srv === 'newsletter' || /^status/.test(user)) return;
      var ch = { jid: j, subject: subj[j] || null };
      if (srv === 'g.us') { ch.isGroup = true; ch.id = 'g:' + slug(user); }
      else { var d = Phone.digits(user); ch.phone = d.length >= 8 ? d : null; ch.id = ch.phone ? 'p:' + Phone.key(ch.phone) : 'l:' + slug(user); }
      chats[j] = ch;
    });
    var sql = 'SELECT _id AS id, key_remote_jid AS jid, ' + c('key_from_me', 'me') + ', timestamp AS ts, ' + c('data', 'text') + ', ' + c('media_wa_type', 'type') + ', ' + c('media_name', 'mname') + ', ' + c('media_caption', 'cap') + ', ' + c('media_mime_type', 'mime') + ', ' + c('media_size', 'fsize') + ', ' + c('remote_resource', 'sender') + ', ' + c('key_id', 'kid') + " FROM messages WHERE key_remote_jid IS NOT NULL AND timestamp > 0 ORDER BY key_remote_jid, timestamp, _id";
    var total = 0;
    try { var cr = db.exec('SELECT COUNT(*) FROM messages'); total = cr.length ? cr[0].values[0][0] : 0; } catch (e) { }
    var st = db.prepare(sql), done = false;
    var cur = { chats: Object.keys(chats).map(function (k) { return chats[k]; }), total: total, read: 0, kind: 'legacy' };
    cur.free = function () { st.free(); };
    cur.next = function () {
      if (done) return null;
      var batch = [];
      while (batch.length < 2000) {
        if (!st.step()) { done = true; break; }
        var o = st.getAsObject(); cur.read++;
        var ch = chats[String(o.jid || '')]; if (!ch) continue;
        var ty = o.type == null ? 0 : +o.type, kind = TYPE_MAP[ty] || 'text';
        if (ty === 0 && !o.text) continue;
        var m = { ts: +o.ts, me: o.me ? 1 : 0, kind: kind, text: String(o.text || o.cap || ''), seq: +o.id, chatId: ch.id, keyId: o.kid ? String(o.kid) : null };
        if (ty !== 0 && o.mname) m.media = { name: String(o.mname), path: '', mime: o.mime || mimeOf(String(o.mname)), size: o.fsize ? +o.fsize : 0, orig: String(o.mname) };
        if (ch.isGroup && !m.me && o.sender) { var sd = Phone.digits(String(o.sender).split('@')[0]); m.authorPhone = sd.length >= 8 ? sd : null; }
        batch.push(m);
      }
      return batch.length || !done ? batch : null;
    };
    return cur;
  }

  // ---------------------------------------------------------------- casar arquivos de mídia com mensagens
  function normPath(p) { return clean(p).normalize('NFC').replace(/\\/g, '/').toLowerCase(); }
  // Acha o arquivo de uma mensagem pelo caminho e pelo nome. Quando a mensagem diz o tamanho,
  // só aceita arquivo com o mesmo tamanho: nunca liga a proposta de um cliente à conversa de outro.
  function MediaIndex(files) {
    this.byTail3 = {}; this.byTail2 = {}; this.byName = {}; this.byAlias = {}; this.sizeMismatch = 0;
    for (var i = 0; i < files.length; i++) this.add(files[i]);
  }
  MediaIndex.prototype.add = function (f) {
    var p = normPath(f.path || f.webkitRelativePath || f.name), seg = p.split('/');
    var t3 = seg.slice(-3).join('/'), t2 = seg.slice(-2).join('/'), nm = seg[seg.length - 1];
    var it = { file: f, path: p, size: f.size };
    (this.byTail3[t3] = this.byTail3[t3] || []).push(it);
    (this.byTail2[t2] = this.byTail2[t2] || []).push(it);
    (this.byName[nm] = this.byName[nm] || []).push(it);
    var dn = displayFileName(nm).toLowerCase();
    if (dn !== nm) (this.byAlias[dn] = this.byAlias[dn] || []).push(it);
  };
  MediaIndex.prototype.find = function (media) {
    if (!media) return null;
    var self = this, p = normPath(media.path || media.name || ''), seg = p.split('/'), size = media.size || 0, sawWrongSize = false;
    function pick(list) {
      if (!list || !list.length) return null;
      if (size) {
        for (var i = 0; i < list.length; i++) if (list[i].size === size) return list[i].file;
        sawWrongSize = true;
        return null;
      }
      return list[0].file;
    }
    var hit = null;
    if (seg.length >= 3) hit = pick(this.byTail3[seg.slice(-3).join('/')]);
    if (!hit && seg.length >= 2) hit = pick(this.byTail2[seg.slice(-2).join('/')]);
    var nm = seg[seg.length - 1];
    if (!hit) hit = pick(this.byName[nm]);
    if (!hit && !size) hit = pick(this.byAlias[nm]) || pick(this.byName[displayFileName(nm).toLowerCase()]);
    if (!hit && media.orig) hit = pick(this.byName[normPath(media.orig)]);
    if (!hit && sawWrongSize) self.sizeMismatch++;
    return hit;
  };

  // ---------------------------------------------------------------- texto legível de uma conversa (para o pacote)
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function fmtStamp(ts) { var d = new Date(ts); return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function transcript(contact, messages, meLabel, fileNameOf) {
    var who = contact.name || (contact.phone ? Phone.format(contact.phone) : 'Contato');
    var lines = ['Conversa com ' + who + (contact.phone ? ' (' + Phone.format(contact.phone) + ')' : ''), 'Arquivo de Clientes — ' + messages.length + ' mensagens', ''];
    for (var i = 0; i < messages.length; i++) {
      var m = messages[i], a = m.me ? (meLabel || 'Eu') : (m.a || who);
      var body = m.t || '';
      if (m.m) body = '[arquivo: ' + (fileNameOf ? fileNameOf(m) : m.m.n) + ']' + (body ? '\n' + body : '');
      if (m.ty === 'deleted') body = body || 'Mensagem apagada';
      if (m.ty === 'omitted') body = '<mídia não incluída na exportação>';
      if (m.sys) lines.push(fmtStamp(m.ts) + ' - ' + body);
      else lines.push(fmtStamp(m.ts) + ' - ' + a + ': ' + body);
    }
    return lines.join('\n') + '\n';
  }

  // ---------------------------------------------------------------- PDF de exemplo (para a demonstração)
  function samplePdf(lines) {
    function esc(s) { return s.replace(/[\\()]/g, '\\$&'); }
    var content = 'BT /F1 22 Tf 64 760 Td (' + esc(lines[0]) + ') Tj ET\n';
    for (var i = 1; i < lines.length; i++) content += 'BT /F1 12 Tf 64 ' + (720 - i * 22) + ' Td (' + esc(lines[i]) + ') Tj ET\n';
    var objs = ['<< /Type /Catalog /Pages 2 0 R >>', '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
      '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>',
      '<< /Length ' + content.length + ' >>\nstream\n' + content + 'endstream', '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>'];
    var out = '%PDF-1.4\n', offs = [];
    for (var k = 0; k < objs.length; k++) { offs.push(out.length); out += (k + 1) + ' 0 obj\n' + objs[k] + '\nendobj\n'; }
    var xref = out.length;
    out += 'xref\n0 ' + (objs.length + 1) + '\n0000000000 65535 f \n';
    for (var q = 0; q < offs.length; q++) out += ('000000000' + offs[q]).slice(-10) + ' 00000 n \n';
    out += 'trailer\n<< /Size ' + (objs.length + 1) + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF\n';
    var bytes = new Uint8Array(out.length);
    for (var b = 0; b < out.length; b++) bytes[b] = out.charCodeAt(b) & 0xff;
    return bytes;
  }

  var api = {
    clean: clean, fold: fold, slug: slug, hash: hash, baseName: baseName, displayFileName: displayFileName, decodeText: decodeText,
    extOf: extOf, kindOf: kindOf, mimeOf: mimeOf, Phone: Phone,
    titleFromFileName: titleFromFileName, parseExportText: parseExportText, looksLikeExport: looksLikeExport, stripBidi: stripBidi, identifyExport: identifyExport,
    msgBodyKey: msgBodyKey, makeKeyer: makeKeyer, parseVcf: parseVcf,
    crc32Blob: crc32Blob, ZipReader: ZipReader, ZipWriter: ZipWriter,
    cleanKey: cleanKey, parseCrypt15Header: parseCrypt15Header, decryptCrypt15: decryptCrypt15, isSqlite: isSqlite, _gcmViaCtr: gcmViaCtr,
    readMsgStore: readMsgStore, openMsgStore: openMsgStore, relMediaPath: relMediaPath, MediaIndex: MediaIndex,
    transcript: transcript, fmtStamp: fmtStamp, samplePdf: samplePdf
  };
  root.ArqCore = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
