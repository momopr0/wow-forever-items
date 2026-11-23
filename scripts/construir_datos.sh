#!/usr/bin/env bash
# Regenera todos los datos de web/ a partir de ./fuentes (ejecutar desde la raíz del proyecto).
# Requiere Python 3 y Pillow (pip install pillow).
set -e
python3 scripts/build.py fuentes/dl/pages/api/items.json web/items.json      # items base (wow-forever-kb)
python3 scripts/build_ws.py web/items.json fuentes/dl4/ws/assets/database/db.json  # stats en vivo de Forever + items nuevos
python3 scripts/build_src.py      # dónde cae cada item, estructurado + diccionarios de idioma
python3 scripts/build_bind.py     # ligado (subasta / al recogerlo)
python3 scripts/build_classdata.py   # stats base por clase, raciales y proficiencias
python3 scripts/build2.py         # iconos (atlas icons.jpg) y talentos
python3 scripts/build3.py         # nombres de items en español (esMX / esES)
python3 - <<'PY'
import json
a=json.load(open('scripts/tal_es_1.json'));b=json.load(open('scripts/tal_es_2.json'))
json.dump({**a,**b},open('web/talents_es.json','w'),ensure_ascii=False,separators=(",",":"))
print("talents_es.json:",len(a)+len(b))
PY
echo "Datos regenerados en web/"
