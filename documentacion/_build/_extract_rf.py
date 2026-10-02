# -*- coding: utf-8 -*-
import re, json, io
src = io.open('gen_srs.py', encoding='utf-8').read()
rows = re.findall(
    r'\["(RF-\d+)",\s*"([^"]+)",\s*"(Maxima|Máxima|Alta|Media|Baja)",\s*"(Completada|Parcial|Pendiente)"\]',
    src)
print(len(rows))
data = {c: {"nombre": n, "prioridad": pr, "estado": e} for c, n, pr, e in rows}
json.dump(data, io.open('rf_catalog.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
missing = ["RF-%03d" % i for i in range(1, 76) if "RF-%03d" % i not in data]
print("faltan:", missing)
for k in sorted(data):
    print(k, data[k]["nombre"], "|", data[k]["prioridad"], "|", data[k]["estado"])
