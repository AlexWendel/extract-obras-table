import json


obras = []
with open("obrinhas.json", "r") as f:
    obrinhas = json.loads(f.read())

    for obra, dados in obrinhas.items():
        obras.append([
            obra, 
            dados["Objeto"], 
            dados["Contrato"], 
            dados["Secretaria"], 
            dados["Situação"], 
            dados["Contratada"], 
            dados["Ordem de Serviço"], 
            dados["Valor do Contrato"],
            dados["Medições"]
        ])

with open("obronas.json", "w+", encoding="utf-8") as f:
    f.write(json.dumps(obras))