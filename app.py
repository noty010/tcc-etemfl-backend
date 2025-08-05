from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


# Adiciona sua host (127.0.0.1 é o padrão)
app.config['MYSQL_HOST'] = '127.0.0.1'
# Adicione o seu nome do mysql
app.config['MYSQL_USER'] = 'root'
# Adicione a senha do seu mysql
app.config['MYSQL_PASSWORD'] = 'senha'
# Adicione o seu banco de dados
app.config['MYSQL_DB'] = 'bd123'

mysql = MySQL(app)

@app.route('/')
def index():
    return 'API funcionando!'

@app.route('/locais', methods=['GET'])
def get_locais():
    cur = mysql.connection.cursor()
    cur.execute('SELECT cod, descricao, resumo, endereco, latitude, longitude, image, dias_funcionamento,icone, horario_de_inicio, horario_de_fim FROM locais_de_Interesse')
    rows = cur.fetchall()
    cur.close()

    locais = []
    for row in rows:
        locais.append({
            'cod': row[0],
            'descricao': row[1],
            'resumo': row[2],
            'endereco': row[3],
            'latitude': float(row[4]),
            'longitude': float(row[5]),
            'image': row[6],
            'dias_funcionamento': row[7],
            'icone': row[8],
            'horario_de_inicio': str(row[9]),
            'horario_de_fim': str(row[10])
        })

    return jsonify(locais)

@app.route('/locais/<categoria>', methods=['GET'])
def get_locais_por_categoria(categoria):
    cur = mysql.connection.cursor()
    query = """
        SELECT l.cod, l.descricao, l.resumo, l.endereco, l.latitude, l.longitude,
               l.image, l.dias_funcionamento, l.icone, l.horario_de_inicio, l.horario_de_fim
        FROM locais_de_Interesse l
        JOIN classificacao_locais c ON c.fk_Locais_de_Interesse = l.cod
        WHERE LOWER(c.descricao) = %s
    """
    cur.execute(query, (categoria.lower(),))
    rows = cur.fetchall()
    cur.close()

    locais = []
    for row in rows:
        locais.append({
            'cod': row[0],
            'descricao': row[1],
            'resumo': row[2],
            'endereco': row[3],
            'latitude': float(row[4]),
            'longitude': float(row[5]),
            'image': row[6],
            'dias_funcionamento': row[7],
            'icone': row[8],
            'horario_de_inicio': str(row[9]),
            'horario_de_fim': str(row[10])
        })

    return jsonify(locais)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
