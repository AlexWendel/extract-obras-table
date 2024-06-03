import sys
import pandas as pd
import json

# Carregar o arquivo Excel
df = pd.read_excel(sys.argv[1])

data = {}

global last_valid_porcentagem

last_valid_porcentagem = None
def extrair_medicao(row):
    global last_valid_porcentagem


    contrato_medicao = f"{round(row.iloc[8]*100, 2) if not pd.isna(row.iloc[8]) else '-'}%"
    saldo_a_medir = f"{round(row.iloc[9]*100, 2) if not pd.isna(row.iloc[9]) else '-'}%"

    if not pd.isna(row.iloc[10]):
        porcentagem = row.iloc[10] * 100  
        last_valid_porcentagem = porcentagem
    else:
        porcentagem = last_valid_porcentagem

    total_medido = f"{porcentagem:.2f}%" if porcentagem is not None else "-"
    valor = f"R$ {round(row.iloc[11], 2) if not pd.isna(row.iloc[11]) else '-'}"
    saldo = f"R$ {round(row.iloc[12], 2) if not pd.isna(row.iloc[12]) else '-'}"
    periodo = row.iloc[13] if not pd.isna(row.iloc[13]) else '-'

    return {periodo: [contrato_medicao, saldo_a_medir, total_medido, valor, saldo]}

columns_names = df.columns
for index, row in df.iterrows():
    obra_code = row.iloc[0]
    obra_medicoes = {}
    obra_data = {}
    
    for i, v in enumerate(row): # Index, Column data
        k = columns_names[i] # Column name 

        if k == "Medições":
            medicoes_data = json.loads(v.replace("'", '"'))
            for periodo, medicao in medicoes_data.items():
                obra_medicoes[periodo] = medicao
        else:
            if type(v) == pd.Timestamp:
                v = v.to_pydatetime().strftime("%d/%m/%Y")

            obra_data[k] = v
        data[obra_code] = obra_data
    data[obra_code]["Medições"] = obra_medicoes

with open("obrinhas.json", "r+", encoding="utf-8") as f:
    f.write(json.dumps(data))   
