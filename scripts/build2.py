import json, os, subprocess, collections
from PIL import Image
ROOT = "fuentes/dl2/zi"
items = json.load(open("web/items.json"))
ag = json.load(open("fuentes/dl2/ag/data/forever/items.json"))["items"]
agic = {i["id"]: i["ic"].lower() for i in ag if i.get("ic")}
t = open("fuentes/dl2/ag/data/forever/talents.js").read()
tal = json.loads(t[t.index("{"):t.rindex("}") + 1])

def icon_name(m):
    return (m.get("icn") or agic.get(m["i"]) or "").lower() or None

# icono aproximado por tipo+ranura para los que no tienen
fb = collections.defaultdict(collections.Counter)
for m in items:
    n = icon_name(m)
    if n: fb[(m["c"], m["t"], m["s"])][n] += 1
fbm = {k: v.most_common(1)[0][0] for k, v in fb.items()}
need = {icon_name(m) for m in items if icon_name(m)} | set(fbm.values())
need |= {ta["icon"].lower() for c in tal["classes"].values() for tr in c["trees"] for ta in tr["talents"]}
need.add("inv_misc_questionmark")

tree = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", "HEAD"], capture_output=True, text=True).stdout.splitlines()
paths = {}
for line in tree:
    n = os.path.splitext(os.path.basename(line))[0].lower()
    if n in need and n not in paths: paths[n] = line
missing_files = [p for p in paths.values() if not os.path.exists(os.path.join(ROOT, p))]
if missing_files:
    sc = os.path.join(ROOT, ".git/info/sparse-checkout")
    with open(sc, "w") as f:
        f.write("\n".join("/" + p.replace("[", "\\[").replace("*", "\\*") for p in paths.values()) + "\n")
    subprocess.run(["git", "-C", ROOT, "checkout", "HEAD"], capture_output=True, timeout=500)

T, COLS = 40, 40
names = sorted(n for n, p in paths.items() if os.path.exists(os.path.join(ROOT, p)))
idx = {n: k for k, n in enumerate(names)}
rows = (len(names) + COLS - 1) // COLS
atlas = Image.new("RGB", (COLS * T, rows * T), (20, 20, 24))
for n, k in idx.items():
    im = Image.open(os.path.join(ROOT, paths[n])).convert("RGB")
    w, h = im.size; c = int(min(w, h) * 0.06)
    im = im.crop((c, c, w - c, h - c)).resize((T, T), Image.LANCZOS)
    atlas.paste(im, ((k % COLS) * T, (k // COLS) * T))
atlas.save("web/icons.jpg", quality=84, optimize=True)
q = idx.get("inv_misc_questionmark", 0)
exact = approx = 0
for m in items:
    n = icon_name(m); m.pop("icn", None); m.pop("icx", None)
    if n in idx: m["ic"] = idx[n]; exact += 1
    else:
        m["ic"] = idx.get(fbm.get((m["c"], m["t"], m["s"])), q); m["icx"] = 1; approx += 1
with open("web/items.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in items) + "\n]\n")
for c in tal["classes"].values():
    for tr in c["trees"]:
        for ta in tr["talents"]:
            ta["ic"] = idx.get(ta.pop("icon", "").lower(), q)
json.dump(tal, open("web/talents.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump({"cols": COLS, "t": T, "n": len(names)}, open("web/atlas.json", "w"))
print("iconos", len(names), "| exactos", exact, "| aproximados", approx, "| atlas", atlas.size)
