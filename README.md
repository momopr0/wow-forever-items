# WoW Forever — Items, equipo y talentos

Aplicación web para **World of Warcraft: Forever** (build 1.60.1) en español (Latinoamérica y España) e inglés:

- **Buscador** de más de 12.000 armaduras y armas: por tipo, estadísticas, ranura, nivel, calidad, origen y si se pueden comprar en la subasta.
- **Mi equipo**: simulador de personaje con las casillas del juego, iconos, auto‑equipar por estadísticas, candado para fijar piezas, filtro de subasta y profesiones, y estadísticas totales con las fórmulas de Forever (esquivar, crítico, poder de ataque, vida, maná, regeneración, raciales, talentos).
- **Talentos**: calculadora de las 9 clases con lo que aporta cada talento a tus estadísticas.
- **Sets**: todos los sets que tu clase puede usar, con dónde cae cada pieza.

## Estructura

```
web/        La página lista para publicar (abrir index.html con un servidor web)
  index.html          Toda la aplicación (HTML + CSS + JavaScript)
  items.json          Items con stats, origen, ligado, icono
  icons.jpg, atlas.json   Iconos en una sola imagen
  talents.json, talents_es.json   Talentos y su traducción al español
  classdata.json      Stats base por clase/nivel, raciales y proficiencias
  names_*.json, src_*.json   Nombres de items y orígenes en cada idioma
scripts/    Scripts que generan los datos de web/
  descargar_fuentes.sh   Descarga las fuentes de datos en ./fuentes
  construir_datos.sh     Regenera todos los archivos de web/
```

## Probar en tu computadora

Hace falta un servidor web (abrir el archivo con doble clic no funciona porque la página carga los JSON):

```bash
cd web
python3 -m http.server 8000
# abre http://localhost:8000 en el navegador
```

## Publicar gratis en GitHub Pages

El repositorio incluye el proceso automático `.github/workflows/pages.yml`, que publica la carpeta `web/` cada vez que cambia.
Solo hay que activarlo una vez: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
La página queda en `https://momopr0.github.io/wow-forever-items/`.

## Actualizar los datos (cuando Blizzard revele más items o haya hotfixes)

Requiere Git, Python 3 y Pillow (`pip install pillow`). Desde la raíz del proyecto:

```bash
bash scripts/descargar_fuentes.sh     # la primera vez (o borra ./fuentes para bajar todo de nuevo)
bash scripts/construir_datos.sh       # regenera web/
```

Para actualizar fuentes ya descargadas: `git -C fuentes/dl4/ws pull` (datos en vivo), `git -C fuentes/dl/pages pull`, etc.

## Fuentes de datos (proyectos abiertos de la comunidad)

| Qué | De dónde |
|---|---|
| Items, orígenes (jefes, misiones, vendedores), base SQLite | [gBlaku/wow-forever-kb](https://github.com/gBlaku/wow-forever-kb) |
| Stats confirmadas en el juego (caché de hotfixes de Blizzard) y fórmulas de stats | [wowsims/forever](https://github.com/wowsims/forever) |
| Iconos por item, talentos, stats base por clase | [Nastyschmo/AeternumGuildLootAwarder](https://github.com/Nastyschmo/AeternumGuildLootAwarder) |
| Imágenes de iconos | [ZHamburglar/wow-forever-icons-and-macros](https://github.com/ZHamburglar/wow-forever-icons-and-macros) |
| Nombres oficiales en español (items, PNJ, misiones, facciones) | [fitzforge/polestar](https://github.com/fitzforge/polestar) |

La traducción al español de los **talentos** y de los **efectos** de los items es propia de este proyecto (no oficial).
World of Warcraft y todo su arte son © Blizzard Entertainment. Revisa las licencias de cada fuente antes de redistribuir sus datos.

## Notas

- Unos 1.985 items siguen ocultos por Blizzard en Forever; usan datos de Classic y se marcan «Classic».
- Las tablas de índices (golpe, crítico, esquivar del equipo) solo están confirmadas a nivel 60; por debajo se usan estimaciones (marcadas «est.»).
- El personaje del usuario se guarda en su navegador (localStorage) y se puede compartir con «Guardar / cargar código».
