import os
import pandas as pd

# Diretório onde os arquivos CSV foram baixados
download_dir = '../downloads'
processed_dir = '../downloads/processed'

# Garantir que o diretório de arquivos processados exista
os.makedirs(processed_dir, exist_ok=True)

# Função para processar arquivos CSV
def processar_csv(nome_arquivo):
    try:
        caminho_arquivo = os.path.join(download_dir, nome_arquivo)
        df = pd.read_csv(caminho_arquivo)
        
        # Exemplo de limpeza de dados (Remover linhas duplicadas e NaN)
        df = df.drop_duplicates().dropna()

        # Salvar o arquivo processado
        caminho_processado = os.path.join(processed_dir, f'processed_{nome_arquivo}')
        df.to_csv(caminho_processado, index=False)
        
        print(f'Arquivo processado com sucesso: {caminho_processado}')
    except Exception as e:
        print(f'Erro ao processar {nome_arquivo}: {e}')

# Processar todos os arquivos CSV na pasta de downloads
for arquivo in os.listdir(download_dir):
    if arquivo.endswith('.csv'):
        processar_csv(arquivo)
