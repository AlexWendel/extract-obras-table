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

current_obra = None
for index, row in df.iterrows():
    head_col = str(row.iloc[0])
    if head_col.lower() == "obras em andamento" or head_col.lower() == "objeto contratual" or head_col.lower() == "modalidade":
        continue
    
    if not pd.isna(row.iloc[0]):
        current_obra = head_col
        last_valid_porcentagem = None
        
        data[current_obra] = {
            "Objeto": row.iloc[1], 
            "Contrato": row.iloc[2],
            "Secretaria": row.iloc[3],
            "Situação": row.iloc[4],
            "Contratada": row.iloc[5],
            "Ordem de Serviço": row.iloc[6].strftime("%d/%m/%Y") if not pd.isna(row.iloc[6]) else "-",
            "Valor do Contrato": f"R${row.iloc[7]:.2f}",
            "Medições": []
        }
        
    if current_obra:
        medicao = extrair_medicao(row)
        data[current_obra]["Medições"].append(medicao)

with open("obrinhas.json", "r+", encoding="utf-8") as f:
    f.write(json.dumps(data))
    
