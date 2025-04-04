from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="teste_nivelamento"
    )

# Rota para buscar operadoras por nome
@app.route('/buscar_operadoras', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('termo', '')
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    consulta = """
    SELECT * FROM operadoras_ativas
    WHERE nome_operadora LIKE %s
    LIMIT 20;
    """
    cursor.execute(consulta, (f'%{termo}%',))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
