import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.ans.gov.br/visualizador/index.php?area=935"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Encontrar os links para download
links = soup.find_all("a", href=True)
csv_links = [link["href"] for link in links if ".csv" in link["href"]]

# Criar pasta de downloads se não existir
if not os.path.exists('../downloads'):
    os.makedirs('../downloads')

# Baixar os arquivos CSV
for link in csv_links:
    file_name = link.split("/")[-1]
    response = requests.get(link)
    with open(f"../downloads/{file_name}", "wb") as file:
        file.write(response.content)
        
print("Arquivos CSV baixados")
