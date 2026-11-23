import json
p="web/items.json"
d=json.load(open(p))
ag={i['id']:i for i in json.load(open('fuentes/dl2/ag/data/forever/items.json'))['items']}
fill=unk=free=0
for i in d:
    if i.get('b') is None:
        a=ag.get(i['i'])
        if a and a.get('b') in (1,2,3): i['b']=a['b']; fill+=1
        elif i.get('nw'): i['bu']=1; unk+=1
        else: i['b']=0; free+=1
with open(p,'w') as f:
    f.write("[\n"+",\n".join(json.dumps(r,ensure_ascii=False,separators=(",",":")) for r in d)+"\n]\n")
print("ligado completado:",fill,"| sin ligar:",free,"| desconocido:",unk)
