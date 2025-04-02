import requests
import os
import zipfile
from bs4 import BeautifulSoup

# URL da página
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script
download_dir = os.path.join(base_dir, '..', 'downloads', 'processed')

# Criar a pasta de destino se não existir
os.makedirs(download_dir, exist_ok=True)


# Função para baixar arquivos PDF
def baixar_pdf(url_pdf, pasta, nome_arquivo):
    response = requests.get(url_pdf)
    if response.status_code == 200:
        caminho_arquivo = os.path.join(pasta, nome_arquivo)
        with open(caminho_arquivo, "wb") as file:
            file.write(response.content)
        print(f"Baixado: {nome_arquivo}")
        return caminho_arquivo
    else:
        print(f"Erro ao baixar {nome_arquivo}: {response.status_code}")
        return None

# Função para compactar arquivos em um ZIP
def compactar_em_zip(arquivos, arquivo_zip):
    with zipfile.ZipFile(arquivo_zip, 'w') as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))
    print(f"Arquivos compactados em: {arquivo_zip}")

# Acessando o site e buscando os links dos PDFs
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Procurar por links de PDFs na página com o nome "ANEXO I" e "ANEXO II"
    links_pdfs = []
    for a_tag in soup.find_all('a', href=True):
        texto = a_tag.get_text()
        href = a_tag['href']
        
        # Verifica se o link é um PDF e contém "ANEXO I" ou "ANEXO II"
        if href.endswith('.pdf') and ("Anexo I" in texto or "Anexo II" in texto):
            links_pdfs.append(href)
    
    # Imprimir os links encontrados para depuração
    print("Links encontrados:")
    for link in links_pdfs:
        print(link)
    
    # Baixar os arquivos PDF encontrados
    arquivos_baixados = []
    for idx, pdf_link in enumerate(links_pdfs):
        if pdf_link.startswith('/'):
            pdf_link = "https://www.gov.br" + pdf_link
        
        nome_pdf = f"anexo_{idx + 1}.pdf"
        caminho_pdf = baixar_pdf(pdf_link, download_dir, nome_pdf)
        if caminho_pdf:
            arquivos_baixados.append(caminho_pdf)
    
    # Compactar os arquivos em um arquivo ZIP
    if arquivos_baixados:
        zip_path = os.path.join(download_dir, "anexos_compactados.zip")
        compactar_em_zip(arquivos_baixados, zip_path)
else:
    print(f"Erro ao acessar o site: {response.status_code}")
