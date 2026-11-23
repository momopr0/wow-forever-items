#!/usr/bin/env bash
# Descarga las fuentes de datos abiertas en ./fuentes (ejecutar desde la raíz del proyecto).
set -e
mkdir -p fuentes && cd fuentes
# 1) Items y orígenes de WoW Forever (rama gh-pages con la API en JSON)
[ -d dl/pages ] || git clone --depth 1 -b gh-pages https://github.com/gBlaku/wow-forever-kb.git dl/pages
# 2) Iconos por item, talentos y estadísticas base por clase
[ -d dl2/ag ] || git clone --depth 1 https://github.com/Nastyschmo/AeternumGuildLootAwarder.git dl2/ag
# 3) Imágenes de iconos (solo se descargan los que hacen falta, lo hace build2.py)
if [ ! -d dl2/zi ]; then
  git clone --depth 1 --filter=blob:none --no-checkout https://github.com/ZHamburglar/wow-forever-icons-and-macros.git dl2/zi
  git -C dl2/zi sparse-checkout init --no-cone
fi
# 4) Nombres oficiales en español (items, PNJ, misiones, facciones)
if [ ! -d dl3/ps ]; then
  git clone --depth 1 --filter=blob:none --no-checkout https://github.com/fitzforge/polestar.git dl3/ps
  git -C dl3/ps sparse-checkout init --no-cone
  printf '/addon/Polestar_esES/Names.lua\n/addon/Polestar_esMX/Names.lua\n' > dl3/ps/.git/info/sparse-checkout
  git -C dl3/ps checkout HEAD
fi
# 5) Datos en vivo de Forever (caché de hotfixes) del simulador wowsims
if [ ! -d dl4/ws ]; then
  git clone --depth 1 --filter=blob:none --no-checkout https://github.com/wowsims/forever.git dl4/ws
  git -C dl4/ws sparse-checkout init --no-cone
  printf '/assets/database/db.json\n' > dl4/ws/.git/info/sparse-checkout
  git -C dl4/ws checkout HEAD
fi
echo "Fuentes listas en ./fuentes"
