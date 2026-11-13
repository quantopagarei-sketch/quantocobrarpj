#!/usr/bin/env bash
# Roteiro único do robô. Os dois workflows chamam este arquivo:
#  - main:     .github/workflows/telegram-ofertas.yml (de hora em hora)
#  - telegram: .github/workflows/telegram-agora.yml   (na hora, quando a fila ou disparar.txt muda)
python3 coletor_shopee.py || true   # desligado enquanto não houver os segredos da Shopee
python3 bot.py; rc=$?
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "Estado do robô $(TZ=America/Sao_Paulo date +%d/%m-%Hh) [skip netlify]"
  ok=1
  for i in 1 2 3; do
    git pull -q --rebase origin telegram && git push -q origin HEAD:telegram && ok=0 && break
    sleep 5
  done
  [ $ok -eq 0 ] || exit 1
fi
exit $rc
