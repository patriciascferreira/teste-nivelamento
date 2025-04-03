import mysql.connector

# Configurações de conexão MySQL
conn = mysql.connector.connect(
    host="localhost",           # Normalmente é localhost
    user="root",                 # Substitua pelo seu usuário MySQL
    password="mysql",   # Substitua pela sua senha MySQL
    database="teste_nivelamento" # Nome do banco que você criou
)

# Testar conexão
try:
    if conn.is_connected():
        print("Conexão bem-sucedida com o banco de dados!")
except Exception as e:
    print(f"Erro ao conectar: {e}")
finally:
    conn.close()
