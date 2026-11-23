import json, sys, re
BAD=re.compile(r"^(OLD|TestBoots|Ring of Critical Testing|QATest|90 Epic |Monster - )|\bQA\b|Deprecated|\[PH\]|\bDEBUG\b",re.I)
CLS=re.compile(r"((?:Warrior|Paladin|Hunter|Rogue|Priest|Shaman|Mage|Warlock|Druid)(?:(?:, | and | or |/)(?:Warrior|Paladin|Hunter|Rogue|Priest|Shaman|Mage|Warlock|Druid))*) only")
src, out = sys.argv[1], sys.argv[2]
items = json.load(open(src))
STAT_KEYS = {"stamina":"sta","agility":"agi","intellect":"int","strength":"str","spirit":"spi",
  "crit":"crit","hit":"hit","haste":"haste","attack_power":"ap","ranged_attack_power":"rap",
  "spell_power":"sp","spell_damage":"sd","healing":"heal","mp5":"mp5","defense":"def",
  "dodge":"dodge","parry":"parry","block":"block","block_value":"bv","bonus_armor":"barm",
  "fire_res":"rfire","frost_res":"rfrost","nature_res":"rnat","shadow_res":"rsha","arcane_res":"rarc"}
OTHER = {"expertise":"exp","hp5":"hp5","spell_penetration":"spen"}
SRC = {"drop":"d","quest":"q","crafted":"c","vendor":"v","container":"k","object":"o"}
AG = {a["id"]: a for a in json.load(open("fuentes/dl2/ag/data/forever/items.json"))["items"]}
SID = {7:"sta",3:"agi",5:"int",4:"str",6:"spi",32:"crit",31:"hit",36:"haste",38:"ap",45:"sp",43:"mp5",12:"def",13:"dodge",14:"parry",37:"exp"}
upd = 0
res = []
for i in items:
    if i["item_class"] not in ("Armor","Weapon"): continue
    if BAD.search(i["name"]): continue
    if i["junk"] or i["quality"] >= 6 or i["slot"] == "Non-equippable": continue
    st = {}
    for k, s in STAT_KEYS.items():
        if i.get(k): st[s] = i[k]
    for o in (i.get("other_stats") or "").split(", "):
        if " +" in o:
            n, v = o.split(" +", 1)
            if n in OTHER:
                try: st[OTHER[n]] = int(v)
                except ValueError: pass
    a = AG.get(i["id"])
    if a and a.get("s"):
        sa = {SID[x]: v for x, v in a["s"] if x in SID}
        sm = {k: v for k, v in st.items() if k in SID.values()}
        if sa and sa != sm:
            for k in sm: st.pop(k, None)
            st.update(sa); upd += 1
    r = {"i":i["id"],"n":i["name"],"q":i["quality"],"l":i["item_level"],"r":i["required_level"],
         "c":0 if i["item_class"]=="Armor" else 1,"t":i.get("subclass") or "","s":i["slot"],"st":st}
    if i.get("armor"): r["a"] = i["armor"]
    if i.get("dps"): r["dps"] = i["dps"]; r["sp_"] = i.get("speed")
    if i.get("effects"): r["e"] = i["effects"]
    if i.get("item_set"): r["set"] = i["item_set"]
    if i.get("classes"): r["cl"] = i["classes"]
    if i.get("source_summary"): r["src"] = i["source_summary"]
    if not r.get("cl") and r.get("src"):
        m = CLS.search(r["src"])
        if m: r["cl"] = ", ".join(re.split(r", | and | or |/", m[1]))
    if i.get("source_types"): r["so"] = "".join(SRC.get(x,"") for x in i["source_types"].split(","))
    if i.get("bonding"): r["b"] = {"Binds when picked up":1,"Binds when equipped":2,"Binds when used":3}.get(i["bonding"],0)
    if i["estimated"]: r["x"] = 1
    if i.get("level_hint") and i["level_hint"] != i["required_level"]: r["h"] = i["level_hint"]
    res.append(r)
with open(out, "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",",":")) for r in res) + "\n]\n")
print(len(res), "stats actualizadas al build nuevo:", upd)
