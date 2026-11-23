"""Orígenes de los items (dónde caen) como datos estructurados + diccionarios por idioma."""
import json, re, urllib.parse, collections
APP = "web"
items = json.load(open(f"{APP}/items.json"))
ids = {r["i"] for r in items}
srcs = json.load(open("fuentes/dl/pages/api/item_sources.json"))
ws = json.load(open("fuentes/dl4/ws/assets/database/db.json"))
WSI = {i["id"]: i for i in ws["items"]}
WS_NPC = {n["id"]: n for n in ws.get("npcs", [])}
WS_ZONE = {z["id"]: z["name"] for z in ws.get("zones", [])}
WS_FAC = {f["id"]: f["name"] for f in ws.get("factions", []) or []}

ZONE_ES = {"Ahn'Qiraj":"Ahn'Qiraj","Ahn'Qiraj Temple (raid)":"Templo de Ahn'Qiraj (banda)","Ahn'Qiraj War":"Guerra de Ahn'Qiraj","Alcaz Prison":"Prisión de Alcaz","Alterac Mountains":"Montañas de Alterac","Alterac Valley":"Valle de Alterac","Arathi Basin":"Cuenca de Arathi","Arathi Highlands":"Tierras Altas de Arathi","Ashenvale":"Vallefresno","Azshara":"Azshara","Badlands":"Tierras Inhóspitas","Blackfathom Deeps":"Cavernas de Brazanegra","Blackrock Depths":"Profundidades de Roca Negra","Blackrock Mountain":"Montaña Roca Negra","Blackrock Spire":"Cumbre de Roca Negra","Blackwing Lair":"Guarida Alanegra","Blackwing Lair (raid)":"Guarida Alanegra (banda)","Blasted Lands":"Las Tierras Devastadas","Booty Bay":"Bahía del Botín","Burning Steppes":"Las Estepas Ardientes","Camp Narache":"Campamento Narache","Champions' Hall":"Sala de los Campeones","City of Dalaran":"Ciudad de Dalaran","Coldridge Valley":"Valle de Crestanevada","Dalaran":"Dalaran","Darkmoon Faire":"Feria de la Luna Negra","Darkshore":"Costa Oscura","Darkspear Islands":"Islas Lanza Negra","Darnassus":"Darnassus","Deadmines":"Minas de la Muerte","Deadwind Pass":"Paso de la Muerte","Deathknell":"Camposanto","Deeprun Tram":"Tranvía Subterráneo","Desolace":"Desolace","Dire Maul":"La Masacre","Dun Morogh":"Dun Morogh","Durotar":"Durotar","Duskwood":"Bosque del Ocaso","Dustwallow Marsh":"Marjal Revolcafango","Eastern Kingdoms":"Reinos del Este","Eastern Plaguelands":"Tierras de la Peste del Este","Elwynn Forest":"Bosque de Elwynn","Everlook":"Vista Eterna","Excavation Site: Wetlands":"Excavación: Los Humedales","Feathermoon Stronghold":"Bastión Plumaluna","Felwood":"Frondavil","Feralas":"Feralas","Gadgetzan":"Gadgetzan","Gates of Ahn'Qiraj":"Puertas de Ahn'Qiraj","Gilneas":"Gilneas","Gnomeregan":"Gnomeregan","Hall of Legends":"Sala de las Leyendas","Hillsbrad Foothills":"Laderas de Trabalomas","Ironforge":"Forjaz","Kalimdor":"Kalimdor","Loch Modan":"Loch Modan","Lunar Festival":"Festival Lunar","Maraudon":"Maraudon","Midsummer":"Festival de Fuego del Solsticio de Verano","Molten Core":"Núcleo de Magma","Molten Core (raid)":"Núcleo de Magma (banda)","Moonglade":"Claro de la Luna","Mount Hyjal":"Monte Hyjal","Mulgore":"Mulgore","Naxxramas":"Naxxramas","Naxxramas (raid)":"Naxxramas (banda)","Northshire Abbey":"Abadía de Villanorte","Northshire Valley":"Valle de Villanorte","Old Hillsbrad Foothills":"Antiguas Laderas de Trabalomas","Onyxia's Lair":"Guarida de Onyxia","Onyxia's Lair (raid)":"Guarida de Onyxia (banda)","Orgrimmar":"Orgrimmar","Ragefire Chasm":"Sima Ígnea","Razorfen Downs":"Zahúrda Rajacieno","Razorfen Kraul":"Horado Rajacieno","Red Cloud Mesa":"Mesa de la Nube Roja","Redridge Mountains":"Montañas Crestagrana","Ruins of Ahn'Qiraj":"Ruinas de Ahn'Qiraj","Ruins of Ahn'Qiraj (raid)":"Ruinas de Ahn'Qiraj (banda)","Ruins of Gilneas":"Ruinas de Gilneas","Ruins of Lordaeron":"Ruinas de Lordaeron","Scarlet Monastery":"Monasterio Escarlata","Scholomance":"Scholomance","Searing Gorge":"La Garganta de Fuego","Shadowfang Keep":"Castillo de Colmillo Oscuro","Shadowglen":"Cañada Umbría","Silithus":"Silithus","Silverpine Forest":"Bosque de Argénteos","Stonetalon Mountains":"Sierra Espolón","Stormwind City":"Ciudad de Ventormenta","Stormwind Stockade":"Mazmorras de Ventormenta","Stranglethorn Vale":"Vega de Tuercespina","Stratholme":"Stratholme","Sunken Temple":"Templo Sumergido","Swamp of Sorrows":"Pantano de las Penas","Tanaris":"Tanaris","Teldrassil":"Teldrassil","Temple of Ahn'Qiraj":"Templo de Ahn'Qiraj","Thalanaar":"Thalanaar","The Barrens":"Los Baldíos","The Black Morass":"La Ciénaga Negra","The Deadmines":"Minas de la Muerte","The Hall of Thanes":"La Sala de los Thanes","The Hinterlands":"Tierras del Interior","The Stockade":"Las Mazmorras","The Temple of Atal'Hakkar":"El Templo de Atal'Hakkar","Thousand Needles":"Las Mil Agujas","Thunder Bluff":"Cima del Trueno","Timbermaw Hold":"Bastión Fauces de Madera","Tirisfal Glades":"Claros de Tirisfal","Uldaman":"Uldaman","Un'Goro Crater":"Cráter de Un'Goro","Undercity":"Entrañas","Utgarde Keep":"Fortaleza de Utgarde","Utgarde Pinnacle":"Pináculo de Utgarde","Valley of Trials":"Valle de los Retos","Wailing Caverns":"Cuevas de los Lamentos","Warsong Gulch":"Garganta Grito de Guerra","Western Plaguelands":"Tierras de la Peste del Oeste","Westfall":"Páramos de Poniente","Wetlands":"Los Humedales","Winterspring":"Cuna del Invierno","Zul'Farrak":"Zul'Farrak","Zul'Gurub":"Zul'Gurub","Zul'Gurub (raid)":"Zul'Gurub (banda)",
 "Alchemy":"Alquimia","Blacksmithing":"Herrería","Cooking":"Cocina","Engineering":"Ingeniería","Fishing":"Pesca","Herbalism":"Herboristería","Leatherworking":"Peletería","Tailoring":"Sastrería","Enchanting":"Encantamiento","First Aid":"Primeros auxilios","Mining":"Minería","Skinning":"Desuello",
 "Druid":"Druida","Hunter":"Cazador","Mage":"Mago","Paladin":"Paladín","Priest":"Sacerdote","Rogue":"Pícaro","Shaman":"Chamán","Warlock":"Brujo","Warrior":"Guerrero",
 "Epic":"Épico","Legendary":"Legendario","Seasonal":"De temporada","Special":"Especial","Invasion":"Invasión","Treasure Map":"Mapa del tesoro","World Drop":"Botín mundial","Alliance":"Alianza","Horde":"Horda"}

# --- nombres oficiales de polestar
def polestar(loc, kind):
    txt = open(f"fuentes/dl3/ps/addon/Polestar_{loc}/Names.lua", encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'R\("%s",\s*\d+,\s*\d+,\s*\[\[(.*?)\]\]\)' % kind, txt, re.S):
        for line in m.group(1).split("\n"):
            if "\t" in line:
                a, b = line.split("\t", 1)
                if a.isdigit(): out[a] = urllib.parse.unquote(b.strip())
    return out

KORD = {"quest": 0, "drop": 1, "vendor": 2, "object": 3, "container": 4, "crafted": 5}
K = {"quest": "q", "drop": "d", "vendor": "v", "object": "o", "container": "k", "crafted": "c"}
EN = {"n": {}, "q": {}, "o": {}, "k": {}, "f": {}}
per = collections.defaultdict(list)
for s in srcs:
    if s["item_id"] not in ids: continue
    per[s["item_id"]].append(s)
def zone(z): return z or ""
out_count = 0
for r in items:
    lst = per.get(r["i"])
    S = []
    if lst:
        lst.sort(key=lambda s: (KORD.get(s["kind"], 9), -(s.get("chance") or 0)))
        seen = set()
        for s in lst:
            k = K.get(s["kind"])
            if not k: continue
            sig = (k, s.get("source_id"))
            if sig in seen: continue
            seen.add(sig)
            if k == "c":
                rec = 1 if "recipe" in (s.get("extra") or "") else 0
                S.append(["c", s["name"], s.get("min_level") or 0, rec])
            else:
                sid = str(s["source_id"])
                EN[{"d": "n", "v": "n"}.get(k, k)][sid] = s["name"]
                e = [k, sid, zone(s.get("zone"))]
                if k == "d": e += [s.get("min_level") or 0, s.get("max_level") or 0, round(s.get("chance") or 0, 2)]
                if k == "o": e += [0, 0, round(s.get("chance") or 0, 2)]
                if k == "q": e += [s.get("extra") or ""]
                S.append(e)
            if len(S) >= 4: break
    elif r["i"] in WSI and WSI[r["i"]].get("sources"):
        for s in WSI[r["i"]]["sources"]:
            if "drop" in s:
                d = s["drop"]; sid = str(d.get("npcId") or "")
                if sid:
                    EN["n"][sid] = WS_NPC.get(d.get("npcId"), {}).get("name", d.get("otherName", ""))
                    S.append(["d", sid, WS_ZONE.get(d.get("zoneId"), ""), 0, 0, 0])
                else: S.append(["w", d.get("otherName", "World Drop"), WS_ZONE.get(d.get("zoneId"), "")])
            elif "quest" in s:
                sid = str(s["quest"].get("id")); EN["q"][sid] = s["quest"].get("name", ""); S.append(["q", sid, "", ""])
            elif "soldBy" in s:
                v = s["soldBy"]; sid = str(v.get("npcId")); EN["n"][sid] = v.get("npcName", ""); S.append(["v", sid, WS_ZONE.get(v.get("zoneId"), "")])
            elif "rep" in s:
                fr = s["rep"]; fid = str(fr.get("repFactionId")); EN["f"][fid] = WS_FAC.get(fr.get("repFactionId"), ""); S.append(["r", fid, fr.get("repLevel", 0)])
            elif "crafted" in s: S.append(["c", "", 0, 0])
            elif "pvp" in s: S.append(["p"])
            if len(S) >= 4: break
    if S:
        r["S"] = S; out_count += 1
        r.pop("src", None)
with open(f"{APP}/items.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in items) + "\n]\n")
json.dump(EN, open(f"{APP}/src_en.json", "w"), ensure_ascii=False, separators=(",", ":"))
used = {k: set(v) for k, v in EN.items()}
for loc in ("esMX", "esES"):
    D = {"n": polestar(loc, "npc"), "q": polestar(loc, "quest"), "o": polestar(loc, "object"), "f": polestar(loc, "faction"), "k": polestar(loc, "item")}
    o = {k: {i: D[k][i] for i in used[k] if i in D[k]} for k in D}
    o["z"] = ZONE_ES
    json.dump(o, open(f"{APP}/src_{loc}.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(loc, {k: f"{len(o[k])}/{len(used.get(k, []))}" for k in ("n", "q", "o", "f", "k")})
print("items con origen estructurado:", out_count)
