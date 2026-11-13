#!/usr/bin/env python3
"""Coletor automático de ofertas pela API oficial de afiliados da Shopee (Open API).

Só funciona quando existirem os segredos SHOPEE_APP_ID e SHOPEE_APP_SECRET no GitHub
(painel de afiliado da Shopee > Open API). Sem eles, sai sem fazer nada e quem abastece
a fila é o agente Curador. Quando a fila está baixa, busca produtos de casa bem
avaliados, com desconto e comissão, e grava em fila/ já com o link de afiliado.

ATENÇÃO: escrito pela documentação pública; ainda NÃO testado com credenciais reais.
Na primeira execução com credenciais, conferir o log e 1 link no relatório de cliques.
"""
import hashlib, json, os, re, sys, time, urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
APP_ID = os.environ.get("SHOPEE_APP_ID", "").strip()
SECRET = os.environ.get("SHOPEE_APP_SECRET", "").strip()
CFG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
S = CFG["shopee"]
TZ = ZoneInfo(CFG.get("fuso", "America/Sao_Paulo"))
URL = "https://open-api.affiliate.shopee.com.br/graphql"


def chamar(query):
    corpo = json.dumps({"query": query}, separators=(",", ":"), ensure_ascii=False)
    ts = str(int(time.time()))
    assinatura = hashlib.sha256((APP_ID + ts + corpo + SECRET).encode("utf-8")).hexdigest()
    req = urllib.request.Request(URL, data=corpo.encode("utf-8"), headers={
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={APP_ID}, Timestamp={ts}, Signature={assinatura}"})
    with urllib.request.urlopen(req, timeout=40) as r:
        j = json.load(r)
    if j.get("errors"):
        raise RuntimeError(str(j["errors"])[:300])
    return j["data"]


def num(v, padrao=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return padrao


def main():
    if not (APP_ID and SECRET):
        print("Sem credenciais da API da Shopee: coletor desligado.")
        return 0
    estado = json.loads((BASE / "estado.json").read_text(encoding="utf-8")) if (BASE / "estado.json").exists() else {}
    if not estado.get("chat_id"):
        print("Canal ainda não ligado: não coleto.")
        return 0
    t = datetime.now(TZ)
    hoje = t.strftime("%Y%m%d")
    fila = BASE / "fila"
    fila.mkdir(exist_ok=True)
    if estado.get("pendentes", 0) >= S["coletar_quando_fila_menor_que"] or list(fila.glob(f"{hoje}-api-*.json")):
        print("Fila abastecida ou coleta de hoje já feita.")
        return 0
    ja = set()
    for arq in fila.glob("*.json"):
        try:
            ja.add(str(json.loads(arq.read_text(encoding="utf-8")).get("item_id", "")))
        except Exception:
            pass
    f = S["filtros"]
    palavra = S["palavras"][t.timetuple().tm_yday % len(S["palavras"])]
    q = ('{productOfferV2(keyword:%s,sortType:2,page:1,limit:40){nodes{itemId productName priceMin priceMax '
         'commissionRate sales ratingStar priceDiscountRate imageUrl shopName offerLink productLink}}}') % json.dumps(palavra, ensure_ascii=False)
    try:
        nos = chamar(q)["productOfferV2"]["nodes"]
    except Exception as e:
        print("API da Shopee falhou:", type(e).__name__, str(e)[:200])
        return 0
    bons = []
    for n in nos:
        preco = num(n.get("priceMin"))
        if (str(n.get("itemId")) in ja or num(n.get("ratingStar")) < f["nota_min"] or num(n.get("sales")) < f["vendas_min"]
                or num(n.get("priceDiscountRate")) < f["desconto_min_pct"] or not f["preco_min"] <= preco <= f["preco_max"]
                or num(n.get("commissionRate")) < f["comissao_min"]):
            continue
        bons.append(n)
    bons.sort(key=lambda n: num(n.get("sales")) * num(n.get("commissionRate")), reverse=True)
    feitos = 0
    for n in bons[: S["max_novos_por_dia"]]:
        link = n.get("offerLink") or ""
        try:  # link curto com sub_id, para o relatório da Shopee separar o que veio do Telegram
            m = 'mutation{generateShortLink(input:{originUrl:%s,subIds:[%s]}){shortLink}}' % (json.dumps(n["productLink"]), json.dumps(S["sub_id"]))
            link = chamar(m)["generateShortLink"]["shortLink"] or link
        except Exception as e:
            print("link curto falhou, uso o link da oferta:", type(e).__name__)
        if not link:
            continue
        feitos += 1
        vendas = int(num(n.get("sales")))
        item = {"id": f"{hoje}-api-{feitos:02d}", "item_id": str(n.get("itemId")), "loja": "Shopee",
                "nome": re.sub(r"\s+", " ", str(n.get("productName", "")))[:110].strip(),
                "preco": round(num(n.get("priceMin")), 2), "desconto_pct": int(num(n.get("priceDiscountRate"))),
                "motivo": f"{num(n.get('ratingStar')):.1f}★ · {vendas:,} vendidos".replace(",", "."),
                "link": link, "imagem": n.get("imageUrl") or "", "conferido_em": t.isoformat(timespec="minutes"),
                "origem": f"API Shopee ({palavra})", "comissao": num(n.get("commissionRate"))}
        (fila / f"{item['id']}.json").write_text(json.dumps(item, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Coletor Shopee: {feitos} oferta(s) nova(s) para '{palavra}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
