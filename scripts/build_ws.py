"""Aplica los datos en vivo de WoW Forever (wowsims/forever, caché de hotfixes del juego)
sobre items.json: corrige stats/calidad/nivel y añade los items que faltan."""
import json, sys, re
src_items, ws_path = sys.argv[1], sys.argv[2]
items = json.load(open(src_items))
db = json.load(open(ws_path))
ws = {i["id"]: i for i in db["items"]}
NPC = {n["id"]: n for n in db.get("npcs", [])}
ZONE = {z["id"]: z["name"] for z in db.get("zones", [])}
FAC = {f["id"]: f["name"] for f in db.get("factions", []) or []}
WSTAT = {0:"str",1:"agi",2:"sta",3:"int",13:"spi",14:"ap",15:"rap",17:"hit",18:"crit",19:"haste",21:"exp",
         22:"def",23:"block",24:"bv",25:"dodge",26:"parry",28:"barm",31:"mp5",12:"spen",
         32:"rarc",33:"rfire",34:"rfrost",35:"rnat",36:"rsha"}
CLS = {1:"Warrior",2:"Paladin",3:"Hunter",4:"Rogue",5:"Priest",7:"Shaman",8:"Mage",9:"Warlock",11:"Druid"}
SLOT = {1:"Head",2:"Neck",3:"Shoulder",4:"Back",5:"Chest",6:"Wrist",7:"Hands",8:"Waist",9:"Legs",10:"Feet",11:"Finger",12:"Trinket"}
ARM = {1:"Cloth",2:"Leather",3:"Mail",4:"Plate"}
HAND = {1:"Main Hand",2:"One-Hand",3:"Off Hand",4:"Two-Hand"}
REP = {4:"Neutral",5:"Amistoso",6:"Honorable",7:"Reverenciado",8:"Exaltado"}
SRCK = {"drop":"d","quest":"q","crafted":"c","soldBy":"v","rep":"v","pvp":"v"}

def stats_of(w):
    so = w["scalingOptions"]["0"]; st = {}
    for k, v in (so.get("stats") or {}).items():
        k = int(k)
        if k in WSTAT and v: st[WSTAT[k]] = v
    s = so.get("stats") or {}
    heal, sd = s.get("4", 0), s.get("5", 0)
    school = max([s.get(str(x), 0) for x in range(6, 12)] or [0])
    if heal and sd and heal == sd: st["sp"] = heal
    else:
        if heal: st["heal"] = heal
        if sd: st["sd"] = sd
    if school and "sd" not in st and "sp" not in st: st["sd"] = school
    return st, s.get("27", 0), so

def kind(w):
    t = w.get("type")
    if t in SLOT:
        return 0, ARM.get(w.get("armorType"), "Miscellaneous"), SLOT[t]
    if t == 13:
        wt, ht = w.get("weaponType"), w.get("handType")
        if wt == 7: return 0, "Shield", "Shield"
        if wt == 5: return 0, "Miscellaneous", "Held In Off-hand"
        two = ht == 4
        base = {1:"Axe",4:"Mace",9:"Sword"}.get(wt)
        sub = (("Two-Handed " if two else "One-Handed ") + base) if base else {2:"Dagger",3:"Fist Weapon",6:"Polearm",8:"Staff"}.get(wt, "Miscellaneous")
        return 1, sub, HAND.get(ht, "One-Hand")
    if t == 14:
        rt = w.get("rangedWeaponType")
        if rt in (6, 7, 8, 9): return 0, {6:"Idol",7:"Libram",8:"Totem",9:"Idol"}[rt], "Relic"
        return 1, {1:"Bow",2:"Crossbow",3:"Gun",4:"Thrown",5:"Wand"}.get(rt, "Gun"), "Thrown" if rt == 4 else "Ranged"
    return None

def src_text(w):
    out = []
    for s in w.get("sources", []):
        if "drop" in s:
            d = s["drop"]; n = NPC.get(d.get("npcId"), {}).get("name") or d.get("otherName") or "botín"
            z = ZONE.get(d.get("zoneId")); out.append(f"Drop: {n}" + (f" ({z})" if z else ""))
        elif "quest" in s: out.append(f'Quest: {s["quest"].get("name","")}')
        elif "soldBy" in s:
            v = s["soldBy"]; z = ZONE.get(v.get("zoneId")); out.append(f'Vendor: {v.get("npcName","")}' + (f" ({z})" if z else ""))
        elif "rep" in s:
            r = s["rep"]; out.append(f'Rep: {FAC.get(r.get("repFactionId"), "facción")} ({REP.get(r.get("repLevel"), "")})')
        elif "crafted" in s: out.append("Crafted")
        elif "pvp" in s: out.append("PvP")
    seen = []; [seen.append(x) for x in out if x not in seen]
    return "; ".join(seen[:3]), "".join(sorted({SRCK[k] for s in w.get("sources", []) for k in s if k in SRCK}))

def setdmg(r, w, so):
    sp = w.get("weaponSpeed") or r.get("sp_")
    mn, mx = so.get("weaponDamageMin"), so.get("weaponDamageMax")
    if mn and mx and sp:
        r["dmg"] = [round(mn), round(mx)]; r["sp_"] = sp; r["dps"] = round((mn + mx) / 2 / sp, 1)
    elif so.get("unroundedDps"):
        r["dps"] = round(so["unroundedDps"], 1); r["sp_"] = sp

byid = {r["i"]: r for r in items}
upd = add = 0
fixed_barm = [0]
for wid, w in ws.items():
    k = kind(w)
    if not k: continue
    st, armor, so = stats_of(w)
    if wid in byid:
        r = byid[wid]
        if r.get("x") and r.get("e"): r["eo"] = 1  # texto del efecto todavía viene de Classic
        r.pop("x", None)
        # "armadura adicional" de wowsims: solo fiable sin armadura base o si el cliente también la tiene
        if "barm" in st and armor:
            if r["st"].get("barm"): st["barm"] = r["st"]["barm"]
            else: st.pop("barm"); fixed_barm[0] += 1
        r.update(q=w.get("quality", r["q"]), l=so.get("ilvl", r["l"]), r=w.get("reqLvl") or 0, st=st)
        if armor: r["a"] = armor
        else: r.pop("a", None)
        setdmg(r, w, so)
        if w.get("setName"): r["set"] = w["setName"]
        if w.get("classAllowlist"): r["cl"] = ", ".join(CLS[c] for c in w["classAllowlist"] if c in CLS)
        if not r.get("src") and w.get("sources"):
            t, so_ = src_text(w)
            if t: r["src"] = t; r["so"] = so_
        r["v"] = 1; r["icn"] = w.get("icon"); upd += 1
    else:
        if re.search(r"\[PH\]|^Monster - |test|^OLD", w["name"], re.I): continue
        c, t, s = k
        if "barm" in st and armor: st.pop("barm"); fixed_barm[0] += 1
        r = {"i": wid, "n": w["name"], "q": w.get("quality", 1), "l": so.get("ilvl", 1), "r": w.get("reqLvl") or 0,
             "c": c, "t": t, "s": s, "st": st, "v": 1, "nw": 1, "icn": w.get("icon")}
        if armor: r["a"] = armor
        setdmg(r, w, so)
        if w.get("setName"): r["set"] = w["setName"]
        if w.get("classAllowlist"): r["cl"] = ", ".join(CLS[x] for x in w["classAllowlist"] if x in CLS)
        if w.get("itemEffects"): r["e"] = " | ".join("Efecto: " + re.sub(r"\s*\(\d+\)$", "", e.get("buffName", "")) for e in w["itemEffects"] if e.get("buffName"))
        t2, so_ = src_text(w)
        if t2: r["src"] = t2; r["so"] = so_
        items.append(r); add += 1
items.sort(key=lambda r: r["i"])
with open(src_items, "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in items) + "\n]\n")
print("corregidos con datos en vivo:", upd, "| añadidos:", add, "| total:", len(items),
      "| armadura extra falsa quitada:", fixed_barm[0], "| aún con datos de Classic:", sum(1 for r in items if r.get("x")))
