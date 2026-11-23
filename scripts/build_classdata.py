"""Stats base por clase/nivel, raciales, combinaciones raza-clase y proficiencias -> web/classdata.json"""
import json, sqlite3
d = json.load(open("fuentes/dl2/ag/data/forever/class-stats.json"))
c = sqlite3.connect("fuentes/dl/pages/wow_forever.db")
out = {"classes": {v["name"]: {"id": int(k), "levels": [{x: l[x] for x in ("hp","mana","agi","str","int","spi","sta","critPerAgi","critPerInt")} for l in v["levels"]]} for k, v in d["classes"].items()},
       "races": d["raceOffsets"], "combos": d["combos"], "rating": d["ratingPerPercentAt60"],
       "armor": [list(r) for r in c.execute("select class,armor,from_level from armor_proficiency")],
       "weap": [list(r) for r in c.execute("select class,subclass from proficiency")]}
json.dump(out, open("web/classdata.json", "w"), separators=(",", ":"))
print("classdata.json:", len(out["classes"]), "clases")
