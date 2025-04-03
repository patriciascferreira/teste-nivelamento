import pandas as pd
import mysql.connector
import os
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime
import numpy as np


def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Verificar se há conexão com a internet
if not check_internet_connection():
    print("❌ Sem conexão com a internet. Verifique sua rede e tente novamente.")
    exit()

# Configurações de conexão MySQL (substitua com seus dados)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="teste_nivelamento"
)
cursor = conn.cursor()

# Criar pastas downloads e demonstracoes_contabeis se não existirem
downloads_dir = os.path.join("..", "downloads")
demonstracoes_dir = os.path.join(downloads_dir, "demonstracoes_contabeis")
os.makedirs(demonstracoes_dir, exist_ok=True)

# 3.2 - Baixar arquivo CSV das Operadoras Ativas
url_operadoras = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
operadoras_path = os.path.join(downloads_dir, "operadoras_ativas.csv")

try:
    response = requests.get(url_operadoras, timeout=10)
    if response.status_code == 200:
        with open(operadoras_path, "wb") as file:
            file.write(response.content)
        print("✅ Arquivo '/Relatorio_cadop.csv' baixado com sucesso!")
    else:
        print(f"❌ Erro ao baixar o arquivo '/Relatorio_cadop.csv'. Status Code: {response.status_code}")
except Exception as e:
    print(f"❌ Erro ao tentar baixar o arquivo '/Relatorio_cadop.csv': {e}")

# 3.1 - Baixar arquivos ZIP trimestrais dos últimos 2 anos (2024 e 2023)
anos = [2024, 2023]
trimestres = ['1T', '2T', '3T', '4T']

for ano in anos:
    for trimestre in trimestres:
        url_demonstracoes = f"https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/{ano}/{trimestre}{ano}.zip"
        try:
            response = requests.get(url_demonstracoes, timeout=10)
            
            if response.status_code == 200:
                with ZipFile(BytesIO(response.content)) as zfile:
                    zfile.extractall(demonstracoes_dir)
                print(f"✅ Arquivos de demonstrações contábeis {trimestre} de {ano} baixados e extraídos com sucesso!")
            else:
                print(f"❌ Arquivo não encontrado: {trimestre}{ano}.zip")
        except Exception as e:
            print(f"❌ Erro ao tentar baixar o arquivo {trimestre}{ano}.zip: {e}")
# Caminho do arquivo CSV
csv_path = "../downloads/Relatorio_cadop.csv"

# Ler o arquivo CSV com codificação apropriada
df_operadoras = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str)

print("📋 Colunas encontradas no arquivo CSV:")
print(df_operadoras.columns)

# Renomear colunas do DataFrame para coincidir com o esquema da tabela MySQL
df_operadoras.columns = [
    'registro_ans', 'cnpj', 'razao_social', 'nome_fantasia', 'modalidade',
    'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep',
    'ddd', 'telefone', 'fax', 'email', 'representante',
    'cargo_representante', 'regiao_de_comercializacao', 'data_registro'
]

# Garantir que CNPJ e CEP sejam tratados como strings
df_operadoras['cnpj'] = df_operadoras['cnpj'].astype(str)
df_operadoras['cep'] = df_operadoras['cep'].astype(str)

# Substituir valores NaN por None para compatibilidade com o MySQL
df_operadoras = df_operadoras.replace({np.nan: None})

# Conferir se as colunas foram renomeadas corretamente
print("📋 Nomes das colunas renomeadas do DataFrame:")
print(df_operadoras.columns)

cursor.execute("""
    DROP TABLE IF EXISTS operadoras_ativas;
""")
conn.commit()

cursor.execute("""
    CREATE TABLE operadoras_ativas (
        registro_ans INT PRIMARY KEY,
        cnpj VARCHAR(20),
        razao_social VARCHAR(255),
        nome_fantasia VARCHAR(255),
        modalidade VARCHAR(50),
        logradouro VARCHAR(255),
        numero VARCHAR(20),
        complemento VARCHAR(255),
        bairro VARCHAR(100),
        cidade VARCHAR(100),
        uf VARCHAR(2),
        cep VARCHAR(10),
        ddd VARCHAR(4),
        telefone VARCHAR(20),
        fax VARCHAR(20),
        email VARCHAR(100),
        representante VARCHAR(255),
        cargo_representante VARCHAR(100),
        regiao_de_comercializacao VARCHAR(255),
        data_registro DATE
    )
""")
conn.commit()
print("✅ Tabela 'operadoras_ativas' criada com sucesso!")

# Inserir dados no banco de dados
for index, row in df_operadoras.iterrows():
    try:
        cursor.execute("""
            INSERT INTO operadoras_ativas (
                registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
                logradouro, numero, complemento, bairro, cidade, uf, cep,
                ddd, telefone, fax, email, representante,
                cargo_representante, regiao_de_comercializacao, data_registro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    except Exception as e:
        print(f"❌ Erro ao inserir linha {index}: {e}")
        
conn.commit()
print("✅ Dados das operadoras ativas importados com sucesso!")
        
# Confirmar as inserções
conn.commit()
print("✅ Dados das operadoras ativas importados com sucesso!")

# Fechar a conexão com o banco de dados
conn.close()