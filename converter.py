import json

obras = {
    "draw": None,
    "recordsTotal": None,
    "recordsFiltered": None,
}

with open("obrinhas.json", "r", encoding="utf-8") as f:
    obrinhas = json.loads(f.read())
    obras["data"] = obrinhas

with open("obronas.json", "w+", encoding="utf-8") as f:
    f.write(json.dumps(obras, ensure_ascii=False))