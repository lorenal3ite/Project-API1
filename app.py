from flask import Flask, request, jsonify
from dateutil.relativedelta import relativedelta
from flask_pydantic_spec import FlaskPydanticSpec
from datetime import datetime

app = Flask(__name__)
spec = FlaskPydanticSpec ('flask',
                            title = 'Flask API',
                            version = '1.0.0',)
spec.register(app)

@app.route('/validade', methods=['POST'])
def calcular_validade():

    def validade(data_fabricacao, validade_valor, validade_unidade):
        """
        :param data_fabricacao:
        :param validade_valor:
        :param validade_unidade:
        :return: a validade conforme a data de fabricacao
        """

    try:
        # recebe os dados enviados na requisição, resposta json
        dados = request.json
        data_fabricacao = dados.get("data_fabricacao") # data de fabricacao
        validade_valor = dados.get("validade_valor") # numr da validade
        validade_unidade = dados.get("validade_unidade") # unidade: "dias", "semanas", "meses", "anos"

        # verifica se todos os dados foram confirm
        if not data_fabricacao or not validade_valor or not validade_unidade:
            return jsonify({"erro": "os campos 'data_fabricacao', 'validade_valor' e 'validade_unidade' são obrigatórios"}), 400

        # converte a data de fabricação para formato date time
        data_fabricacao = datetime.strptime(data_fabricacao, "%Y-%m-%d")

        # calcula a data da validade com base na unidd informada
        if validade_unidade == "dias":
            data_validade = data_fabricacao + relativedelta(days=+validade_valor)
        elif validade_unidade == "semanas":
            data_validade = data_fabricacao + relativedelta(weeks=+validade_valor)
        elif validade_unidade == "meses":
            data_validade = data_fabricacao + relativedelta(months=+validade_valor)
        elif validade_unidade == "anos":
            data_validade = data_fabricacao + relativedelta(years=+validade_valor)
        else:
            return jsonify({"erro": "unidade ou validad invalida. Use 'dias', 'semanas', 'meses' ou 'anos'"}), 400

        # resultado json
        return jsonify({
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_fabricacao": data_fabricacao.strftime("%Y-%m-%d"),
            "validade_valor": validade_valor,
            "validade_unidade": validade_unidade,
            "data_validade": data_validade.strftime("%Y-%m-%d")
        })

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500

if __name__ == '__main__':
    app.run(debug=True)




