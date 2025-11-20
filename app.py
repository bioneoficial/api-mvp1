from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from model import Base, Comissao

app = Flask(__name__)
CORS(app)

DATABASE_URL = "sqlite:///comissoes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

app.config['SWAGGER'] = {
    'title': 'API de Gestão de Comissões',
    'uiversion': 3
}
swagger = Swagger(app)

@app.route('/')
def home():
    """
    Redireciona para a documentação do Swagger
    """
    return redirect('/apidocs/')

@app.route('/comissao', methods=['POST'])
def add_comissao():
    """
    Adiciona uma nova venda/comissão
    ---
    tags:
      - Comissões
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - vendedor
            - produto
            - valor_venda
          properties:
            vendedor:
              type: string
              example: "Carlos Silva"
            produto:
              type: string
              example: "Notebook Gamer"
            valor_venda:
              type: number
              example: 5000.00
    responses:
      201:
        description: Comissão criada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            comissao:
              type: object
      400:
        description: Erro na requisição
    """
    data = request.json
    
    if not data or 'vendedor' not in data or 'produto' not in data or 'valor_venda' not in data:
        return jsonify({"message": "Dados inválidos. Certifique-se de enviar vendedor, produto e valor_venda."}), 400
    
    try:
        valor = float(data['valor_venda'])
        comissao_valor = valor * 0.05
        
        nova_comissao = Comissao(
            vendedor=data['vendedor'],
            produto=data['produto'],
            valor_venda=valor,
            comissao_calculada=comissao_valor
        )
        
        session.add(nova_comissao)
        session.commit()
        
        return jsonify({
            "message": "Venda registrada com sucesso!",
            "comissao": nova_comissao.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Erro ao salvar: {str(e)}"}), 500

@app.route('/comissoes', methods=['GET'])
def get_comissoes():
    """
    Lista todas as comissões registradas
    ---
    tags:
      - Comissões
    responses:
      200:
        description: Lista de comissões
        schema:
          type: object
          properties:
            comissoes:
              type: array
              items:
                type: object
    """
    comissoes = session.query(Comissao).all()
    result = [c.to_dict() for c in comissoes]
    
    return jsonify({"comissoes": result}), 200

@app.route('/comissao', methods=['DELETE'])
def delete_comissao():
    """
    Remove uma comissão pelo ID
    ---
    tags:
      - Comissões
    parameters:
      - in: query
        name: id
        type: integer
        required: true
        description: ID da comissão a ser deletada
    responses:
      200:
        description: Comissão removida
      404:
        description: Comissão não encontrada
    """
    comissao_id = request.args.get('id')
    
    if not comissao_id:
        return jsonify({"message": "ID é obrigatório"}), 400
        
    comissao = session.query(Comissao).filter(Comissao.id == comissao_id).first()
    
    if not comissao:
        return jsonify({"message": "Comissão não encontrada"}), 404
        
    session.delete(comissao)
    session.commit()
    
    return jsonify({"message": "Comissão removida com sucesso!"}), 200

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    Retorna totais para o dashboard (Inovação)
    ---
    tags:
      - Dashboard
    responses:
      200:
        description: Dados sumarizados
        schema:
          type: object
          properties:
            total_vendas:
              type: number
            total_comissoes:
              type: number
            quantidade_vendas:
              type: integer
    """
    total_vendas = session.query(func.sum(Comissao.valor_venda)).scalar() or 0
    total_comissoes = session.query(func.sum(Comissao.comissao_calculada)).scalar() or 0
    qtd_vendas = session.query(func.count(Comissao.id)).scalar() or 0
    
    return jsonify({
        "total_vendas": float(total_vendas),
        "total_comissoes": float(total_comissoes),
        "quantidade_vendas": int(qtd_vendas)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
