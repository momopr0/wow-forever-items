import re, json, sys, urllib.parse
ids = {r["i"] for r in json.load(open("web/items.json"))}
for loc in ("esMX", "esES"):
    txt = open(f"fuentes/dl3/ps/addon/Polestar_{loc}/Names.lua", encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'R\("item",\s*\d+,\s*\d+,\s*\[\[(.*?)\]\]\)', txt, re.S):
        for line in m.group(1).split("\n"):
            if "\t" not in line: continue
            a, b = line.split("\t", 1)
            if a.isdigit() and int(a) in ids:
                out[int(a)] = urllib.parse.unquote(b.strip())
    json.dump(out, open(f"web/names_{loc}.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(loc, len(out), "de", len(ids), list(out.items())[:4])
