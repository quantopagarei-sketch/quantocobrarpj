#!/usr/bin/env python3
"""Robô postador do canal de ofertas (Telegram). Só biblioteca padrão.

Roda de hora em hora no GitHub Actions. Em cada execução:
1. sem token -> sai sem erro (projeto ainda não configurado);
2. descobre sozinho o canal onde o bot foi colocado como administrador;
3. anota o número de inscritos do dia (metricas.csv);
4. se a hora atual é um horário de postagem ainda não usado hoje, publica a
   próxima oferta pendente da pasta fila/ e registra em estado.json e postados.csv.

O robô nunca apaga nem edita os arquivos de fila/: quem escreve lá são os
agentes (Curador) e o coletor da Shopee. O robô só escreve estado.json e os CSV.
Teste local: DRY_RUN=1 TELEGRAM_BOT_TOKEN=x python3 bot.py
"""
import csv, html, json, os, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
DRY = os.environ.get("DRY_RUN") == "1"
CFG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
TZ = ZoneInfo(CFG.get("fuso", "America/Sao_Paulo"))
ESTADO_ARQ = BASE / "estado.json"


def agora():
    falso = os.environ.get("AGORA_FALSO")  # só para teste: 2026-11-13T12:07
    return datetime.fromisoformat(falso).replace(tzinfo=TZ) if falso else datetime.now(TZ)


def api(metodo, **params):
    """Chama a API do Telegram. Devolve (ok, resultado_ou_descricao)."""
    if DRY:
        print("[DRY]", metodo, json.dumps(params, ensure_ascii=False)[:400])
        falso = {"getMe": {"username": "teste_bot", "id": 1},
                 "getUpdates": [{"my_chat_member": {"chat": {"id": -100123, "type": "channel", "title": "Canal Teste", "username": "canalteste"},
                                                    "new_chat_member": {"status": "administrator"}}}],
                 "getChatMemberCount": 42, "getChat": {"id": -100123, "type": "channel", "title": "Canal Teste", "username": "canalteste"}}
        return True, falso.get(metodo, {"message_id": 999})
    dados = json.dumps(params).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/{metodo}", data=dados,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            j = json.load(r)
    except urllib.error.HTTPError as e:
        try:
            j = json.load(e)
        except Exception:
            j = {"ok": False, "description": f"HTTP {e.code}"}
    except Exception as e:  # rede fora do ar etc. (nunca imprime o token)
        j = {"ok": False, "description": type(e).__name__}
    return bool(j.get("ok")), j.get("result") if j.get("ok") else str(j.get("description", "erro"))


def carregar_estado():
    if ESTADO_ARQ.exists():
        return json.loads(ESTADO_ARQ.read_text(encoding="utf-8"))
    return {"chat_id": None, "slots": {}, "itens": {}}


def salvar_estado(e):
    ESTADO_ARQ.write_text(json.dumps(e, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def descobrir_canal(e):
    """Acha o canal: config.canal (se preenchido) ou o canal onde o bot virou administrador."""
    fixo = (CFG.get("canal") or "").strip()
    if fixo:
        ok, r = api("getChat", chat_id=fixo if fixo.startswith(("@", "-")) else "@" + fixo)
        if ok:
            return r
        print("config.canal não abriu:", r)
    ok, r = api("getUpdates", allowed_updates=["my_chat_member", "channel_post"], timeout=0)
    if not ok:
        print("getUpdates falhou:", r)
        return None
    achado = None
    vistos = []  # diagnóstico: onde o bot foi colocado (grupo? canal? com que papel?)
    for u in r:
        m = u.get("my_chat_member")
        if m:
            vistos.append({"tipo": m.get("chat", {}).get("type"), "titulo": m.get("chat", {}).get("title") or "",
                           "papel": m.get("new_chat_member", {}).get("status")})
        if m and m.get("chat", {}).get("type") == "channel":
            if m.get("new_chat_member", {}).get("status") == "administrator":
                achado = m["chat"]
            elif achado and achado.get("id") == m["chat"].get("id"):
                achado = None  # o bot foi removido desse canal depois
        p = u.get("channel_post")
        if p and p.get("chat", {}).get("type") == "channel" and not achado:
            achado = p["chat"]
    e["vistos"] = vistos[-5:]
    return achado


def brl(v):
    return "R$ " + f"{float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def dominio_ok(link):
    try:
        u = urllib.parse.urlparse(link)
    except Exception:
        return False
    host = (u.hostname or "").lower()
    return u.scheme == "https" and any(host == d or host.endswith("." + d) for d in CFG["dominios_permitidos"])


def validar(item):
    if not isinstance(item.get("nome"), str) or not 5 <= len(item["nome"].strip()) <= 140:
        return "nome ausente ou fora do tamanho"
    try:
        if float(item.get("preco")) <= 0:
            return "preço inválido"
    except (TypeError, ValueError):
        return "preço inválido"
    if not dominio_ok(str(item.get("link", ""))):
        return "link fora das lojas permitidas"
    if item.get("imagem") and not str(item["imagem"]).startswith("https://"):
        return "imagem não é https"
    return None


def vencido(item, t):
    if item.get("valido_ate"):
        try:
            return t.date().isoformat() > str(item["valido_ate"])[:10]
        except Exception:
            return False
    c = item.get("conferido_em")
    if not c:
        return False
    try:
        d = datetime.fromisoformat(str(c))
        d = d if d.tzinfo else d.replace(tzinfo=TZ)
        return t - d > timedelta(hours=CFG.get("validade_horas", 72))
    except Exception:
        return False


def legenda(item, t):
    e = html.escape
    preco = float(item["preco"])
    linhas = [f"🔥 <b>{e(item['nome'].strip())}</b>", ""]
    de = item.get("preco_de")
    pct = item.get("desconto_pct")
    try:
        de = float(de) if de else None
    except (TypeError, ValueError):
        de = None
    if de and de > preco * 1.03:
        linhas.append(f"De <s>{brl(de)}</s> por <b>{brl(preco)}</b> (-{round((1 - preco / de) * 100)}%)")
    elif pct:
        linhas.append(f"💰 <b>{brl(preco)}</b> (-{int(float(pct))}%)")
    else:
        linhas.append(f"💰 <b>{brl(preco)}</b>")
    if item.get("cupom"):
        linhas.append(f"🎟 Cupom: <code>{e(str(item['cupom']))}</code>")
    if item.get("motivo"):
        linhas.append(f"✅ {e(str(item['motivo'])[:160])}")
    loja = e(str(item.get("loja") or "Loja"))
    visto = "O preço pode mudar."
    try:  # mostra a hora em que o preço foi realmente conferido (não a hora da postagem)
        c = datetime.fromisoformat(str(item["conferido_em"]))
        visto = f"Preço visto em {c.strftime('%d/%m às %Hh%M')}. Pode mudar."
    except Exception:
        pass
    linhas += ["", f"🛒 {loja}: {e(item['link'])}", "", f"<i>{visto}</i>"]
    return "\n".join(linhas)[:1020]


def publicar(chat_id, item, t):
    texto = legenda(item, t)
    botao = {"inline_keyboard": [[{"text": "🛒 Ver oferta", "url": item["link"]}]]}
    if item.get("imagem"):
        ok, r = api("sendPhoto", chat_id=chat_id, photo=item["imagem"], caption=texto, parse_mode="HTML", reply_markup=botao)
        if ok:
            return ok, r
        print("foto recusada, envio só texto:", r)
    return api("sendMessage", chat_id=chat_id, text=texto, parse_mode="HTML", reply_markup=botao,
               link_preview_options={"is_disabled": not item.get("imagem")})


def anotar_csv(nome, cabecalho, linha, chave_unica=False):
    arq = BASE / nome
    linhas = list(csv.reader(arq.open(encoding="utf-8"))) if arq.exists() else [cabecalho]
    if chave_unica:
        linhas = [l for l in linhas if not l or l[0] != linha[0]]
    linhas.append([str(x) for x in linha])
    with arq.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(linhas)


def main():
    if not TOKEN:
        print("Sem TELEGRAM_BOT_TOKEN: projeto ainda não configurado. Nada a fazer.")
        return 0
    e = carregar_estado()
    t = agora()
    hoje = t.date().isoformat()

    ok, eu = api("getMe")
    if not ok:
        print("Token recusado pelo Telegram:", eu)
        e["erro"] = f"{hoje}: token recusado"
        salvar_estado(e)
        return 0
    e["bot"] = "@" + str(eu.get("username"))
    e.pop("erro", None)

    if not e.get("chat_id"):
        c = descobrir_canal(e)
        if not c:
            print("Bot ativo, mas ainda não é administrador de nenhum canal.")
            e["aguardando"] = "canal"
            salvar_estado(e)
            return 0
        e.update(chat_id=c["id"], chat_username=c.get("username") or "", chat_titulo=c.get("title") or "", ligado_em=t.isoformat(timespec="minutes"))
        e.pop("aguardando", None)
        print("Canal encontrado:", e["chat_titulo"], e["chat_username"])
    chat = e["chat_id"]

    if not e.get("boas_vindas_ok"):
        api("setChatDescription", chat_id=chat, description=CFG["descricao_canal"][:255])
        ok, r = api("sendMessage", chat_id=chat, text=CFG["boas_vindas"], parse_mode="HTML")
        if ok:
            api("pinChatMessage", chat_id=chat, message_id=r["message_id"], disable_notification=True)
            e["boas_vindas_ok"] = True
        else:
            print("Não consegui postar no canal (falta permissão de postar?):", r)
            e["erro"] = f"{hoje}: sem permissão para postar ({r})"
            salvar_estado(e)
            return 0

    ok, n = api("getChatMemberCount", chat_id=chat)
    membros = n if ok else ""
    slots_hoje = e.setdefault("slots", {}).setdefault(hoje, [])
    for d in [d for d in e["slots"] if d < (t.date() - timedelta(days=7)).isoformat()]:
        del e["slots"][d]

    itens = e.setdefault("itens", {})
    pendentes = []
    for arq in sorted((BASE / "fila").glob("*.json")):
        try:
            item = json.loads(arq.read_text(encoding="utf-8"))
        except Exception:
            itens.setdefault(arq.stem, {"status": "erro", "motivo": "arquivo ilegível"})
            continue
        iid = str(item.get("id") or arq.stem)
        if iid in itens:
            continue
        problema = validar(item)
        if problema:
            itens[iid] = {"status": "erro", "motivo": problema}
        elif vencido(item, t):
            itens[iid] = {"status": "vencido"}
        else:
            pendentes.append((-(item.get("prioridade") or 0), arq.name, iid, item))
    pendentes.sort(key=lambda x: (x[0], x[1]))
    e["pendentes"] = len(pendentes)

    if t.hour in CFG["horarios"] and t.hour not in slots_hoje and pendentes:
        _, _, iid, item = pendentes[0]
        ok, r = publicar(chat, item, t)
        if ok:
            itens[iid] = {"status": "postado", "message_id": r.get("message_id"), "em": t.isoformat(timespec="minutes")}
            slots_hoje.append(t.hour)
            e["pendentes"] -= 1
            anotar_csv("postados.csv", ["data_hora", "id", "loja", "nome", "preco", "link", "message_id"],
                       [t.isoformat(timespec="minutes"), iid, item.get("loja", ""), item["nome"], item["preco"], item["link"], r.get("message_id")])
            print("Postado:", iid)
        else:
            itens[iid] = {"status": "erro", "motivo": f"Telegram recusou: {r}"[:200]}
            print("Falhou:", iid, r)
    else:
        print(f"Sem postagem agora (hora {t.hour}h, pendentes {len(pendentes)}).")

    anotar_csv("metricas.csv", ["data", "inscritos", "posts_no_dia", "pendentes_na_fila"],
               [hoje, membros, len(slots_hoje), e["pendentes"]], chave_unica=True)
    if t.hour in CFG["horarios"]:  # batimento só nos horários de postagem (menos commits)
        e["ultima_execucao"] = t.isoformat(timespec="minutes")
    salvar_estado(e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
