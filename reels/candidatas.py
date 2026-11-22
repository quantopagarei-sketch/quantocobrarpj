#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lista as ofertas que podem entrar no Reel de hoje (ver reels.md).
Regra: já POSTADAS no canal nas últimas 24 h (o vídeo manda a pessoa procurar o link no canal) e
que não apareceram em Reel nos últimos 7 dias. Ordena por desconto e potencial; a comissão você confere na página.
Uso: python3 reels/candidatas.py   (rodar na raiz do repositório)
"""
import datetime as dt
import glob
import json
import os

FUSO = dt.timezone(dt.timedelta(hours=-3))
agora = dt.datetime.now(FUSO)
itens = json.load(open('estado.json', encoding='utf-8')).get('itens', {})

usadas = set()
for f in glob.glob('reels/roteiros/*.json'):
    try:
        dia = dt.datetime.strptime(os.path.basename(f)[:8], '%Y%m%d').replace(tzinfo=FUSO)
    except ValueError:
        continue
    if (agora - dia).days <= 7:
        usadas |= {o.get('id') for o in json.load(open(f, encoding='utf-8')).get('ofertas', [])}

linhas = []
for f in sorted(glob.glob('fila/*.json'))[-80:]:
    d = json.load(open(f, encoding='utf-8'))
    i = d.get('id') or os.path.basename(f)[:-5]
    st = itens.get(i, {})
    if st.get('status') != 'postado' or i in usadas:
        continue
    em = dt.datetime.fromisoformat(st['em'])
    if (agora - em).total_seconds() > 24 * 3600:
        continue
    de, por = d.get('preco_de'), d.get('preco')
    off = int((1 - por / de) * 100) if de and de > por else 0
    linhas.append((off + 5 * (d.get('potencial') or 0), i, d, off, st['em'][5:16]))

if not linhas:
    print('Nenhuma oferta postada no canal nas últimas 24 h (ou todas já usadas em Reel). Sem Reel hoje: registre e termine.')
for _, i, d, off, em in sorted(linhas, key=lambda x: -x[0]):
    pix = ' [no Pix]' if 'pix' in (d.get('motivo') or '').lower() else ''
    print(f"{i} | -{off}% | por {d.get('preco')} de {d.get('preco_de')}{pix} | potencial {d.get('potencial')} | "
          f"{d.get('categoria')} | postado {em}\n   {d.get('nome')}\n   motivo: {d.get('motivo')}\n"
          f"   pagina: {d.get('pagina')}\n   imagem: {d.get('imagem')}")
