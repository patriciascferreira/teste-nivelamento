import camelot
import pandas as pd
import zipfile
import os

# Caminhos dos arquivos
input_pdf = '../downloads/processed/anexo_1.pdf'
output_csv = '../downloads/processed/Rol_de_Procedimentos.csv'
output_zip = f'../downloads/processed/Teste_Patricia.zip'

# Extrair tabelas do PDF
print('Extraindo tabelas do PDF...')
tables = camelot.read_pdf(input_pdf, pages='1-end', flavor='stream')

# Combinar todas as tabelas extraídas em um único DataFrame
print('Concatenando tabelas extraídas...')
df = pd.concat([table.df for table in tables], ignore_index=True)

# Substituir abreviações
print('Substituindo abreviações...')
df.replace({'OD': 'Órbita e Dentes', 'AMB': 'Ambulatorial'}, inplace=True)

# Salvar em CSV
print('Salvando CSV...')
df.to_csv(output_csv, index=False)

# Compactar o CSV em um arquivo ZIP
print('Compactando CSV...')
with zipfile.ZipFile(output_zip, 'w') as zipf:
    zipf.write(output_csv, os.path.basename(output_csv))

print(f'Processo concluído! Arquivo ZIP gerado em: {output_zip}')

