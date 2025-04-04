import os
import pandas as pd
import mysql.connector

# Função para conectar com o banco de dados MySQL
def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysql',
        database='teste_nivelamento'
    )

# Função para importar dados de um arquivo CSV para a tabela demonstracoes_contabeis
def importar_dados(arquivo_csv):
    print(f"📂 Lendo arquivo: {arquivo_csv}")
    try:
        # Lendo o arquivo CSV
        df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')
        
        # Renomear colunas para garantir compatibilidade
        df.columns = ['cd_operadora', 'nome_operadora', 'data_referencia', 'cd_conta_contabil', 'descricao_conta', 'vl_saldo_final']
        
        # Corrigir o formato da coluna data_referencia
        df['data_referencia'] = pd.to_datetime(df['data_referencia'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
        
        # Converter colunas para os tipos corretos
        df['cd_operadora'] = pd.to_numeric(df['cd_operadora'], errors='coerce').fillna(0).astype(int)
        df['cd_conta_contabil'] = pd.to_numeric(df['cd_conta_contabil'], errors='coerce').fillna(0).astype(int)
        df['vl_saldo_final'] = pd.to_numeric(df['vl_saldo_final'], errors='coerce').fillna(0)

        # Substituir NaN por None
        df = df.where(pd.notna(df), None)

        # Transformar o DataFrame em uma lista de tuplas para inserção em lote
        dados = df.values.tolist()
        
        # Conectar ao banco de dados
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            cursor.executemany("""
                INSERT INTO demonstracoes_contabeis (
                    cd_operadora, nome_operadora, data_referencia, cd_conta_contabil, descricao_conta, vl_saldo_final
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, dados)
            
            conexao.commit()
            print(f"✅ Dados importados com sucesso do arquivo: {arquivo_csv}")
        except mysql.connector.Error as e:
            print(f"❌ Erro ao inserir os dados: {e}")
        finally:
            cursor.close()
            conexao.close()

    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {arquivo_csv}: {e}")

# Diretório onde estão os arquivos CSV
download_dir = '../downloads/demonstracoes_contabeis'

# Lista dos arquivos CSV no diretório
arquivos = [arquivo for arquivo in os.listdir(download_dir) if arquivo.endswith('.csv')]

# Importar todos os arquivos CSV encontrados
for arquivo in arquivos:
    importar_dados(os.path.join(download_dir, arquivo))

print("🚀 Importação concluída com sucesso!")
