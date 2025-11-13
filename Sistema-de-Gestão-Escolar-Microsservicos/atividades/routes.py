from flask import Blueprint, request, jsonify
from controllers import atividades_controller as controller
import os
import requests
bp = Blueprint('atividades', __name__)
GER_URL = os.environ.get('GERENCIAMENTO_URL','http://gerenciamento:5000')

def json_error(message, code):
    return jsonify({'error': message}), code

@bp.route('/status', methods=['GET'])
def status():
    """Status do serviço de Atividades
    ---
    responses:
      200:
        description: Status do serviço
        schema:
          properties:
            service:
              type: string
              example: atividades
            status:
              type: string
              example: ok
    """
    return jsonify({'service':'atividades','status':'ok'}),200

@bp.route('/atividades', methods=['GET'])
def listar():
    """Lista todas as atividades cadastradas
    ---
    responses:
      200:
        description: Lista de atividades
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              titulo:
                type: string
              descricao:
                type: string
              peso_porcento:
                type: integer
              data_entrega:
                type: string
              turma_id:
                type: integer
              professor_id:
                type: integer
    """
    return jsonify([a.to_dict() for a in controller.listar_atividades()]),200

@bp.route('/atividades/<int:aid>', methods=['GET'])
def obter(aid):
    """Obter uma atividade específica pelo ID
    ---
    parameters:
      - name: aid
        in: path
        type: integer
        required: true
        description: ID da atividade
    responses:
      200:
        description: Detalhes da atividade
        schema:
          type: object
          properties:
            id:
              type: integer
            titulo:
              type: string
            descricao:
              type: string
            peso_porcento:
              type: integer
            data_entrega:
              type: string
            turma_id:
              type: integer
            professor_id:
              type: integer
      404:
        description: Atividade não encontrada
    """
    a = controller.get_atividade_by_id(aid)
    if not a: return json_error('Atividade não encontrada', 404)
    return jsonify(a.to_dict()),200

@bp.route('/atividades', methods=['POST'])
def criar():
    """Criar uma nova atividade
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - titulo
            - turma_id
            - professor_id
          properties:
            titulo:
              type: string
            descricao:
              type: string
            peso_porcento:
              type: integer
            data_entrega:
              type: string
            turma_id:
              type: integer
            professor_id:
              type: integer
    responses:
      201:
        description: Atividade criada com sucesso
      400:
        description: Dados inválidos
      503:
        description: Erro ao contactar serviço de gerenciamento
    """
    data = request.get_json() or {}
    turma_id = data.get('turma_id'); professor_id = data.get('professor_id')
    if not turma_id or not professor_id: return json_error('turma_id e professor_id obrigatórios', 400)
    try:
        resp_t = requests.get(f"{GER_URL}/turmas/{turma_id}", timeout=3)
        resp_p = requests.get(f"{GER_URL}/professores/{professor_id}", timeout=3)
    except requests.RequestException:
        return json_error('Falha ao contactar gerenciamento', 503)
    if resp_t.status_code != 200: return jsonify({'error':'Turma inexistente'}),400
    if resp_p.status_code != 200: return jsonify({'error':'Professor inexistente'}),400
    a = controller.criar_atividade(data)
    return jsonify(a.to_dict()),201

@bp.route('/atividades/<int:aid>', methods=['PUT'])
def atualizar(aid):
    """Atualizar uma atividade existente
    ---
    parameters:
      - name: aid
        in: path
        type: integer
        required: true
        description: ID da atividade
      - in: body
        name: body
        schema:
          type: object
          properties:
            titulo:
              type: string
            descricao:
              type: string
            peso_porcento:
              type: integer
            data_entrega:
              type: string
            turma_id:
              type: integer
            professor_id:
              type: integer
    responses:
      200:
        description: Atividade atualizada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Atividade não encontrada
      503:
        description: Erro ao contactar serviço de gerenciamento
    """
    data = request.get_json() or {}
    turma_id = data.get('turma_id'); professor_id = data.get('professor_id')
    if turma_id:
        try:
            resp_t = requests.get(f"{GER_URL}/turmas/{turma_id}", timeout=3)
        except requests.RequestException:
            return json_error('Falha ao contactar gerenciamento', 503)
        if resp_t.status_code != 200: return json_error('Turma inexistente', 400)
    if professor_id:
        try:
            resp_p = requests.get(f"{GER_URL}/professores/{professor_id}", timeout=3)
        except requests.RequestException:
            return json_error('Falha ao contactar gerenciamento', 503)
        if resp_p.status_code != 200: return json_error('Professor inexistente', 400)
    a = controller.atualizar_atividade(aid, data)
    if not a: return json_error('Atividade não encontrada', 404)
    return jsonify(a.to_dict()),200

@bp.route('/notas', methods=['GET'])
def listar_notas_route():
    """Lista todas as notas cadastradas
    ---
    responses:
      200:
        description: Lista de notas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nota:
                type: number
                format: float
              aluno_id:
                type: integer
              atividade_id:
                type: integer
    """
    return jsonify([n.to_dict() for n in controller.listar_notas()]),200

@bp.route('/notas', methods=['POST'])
def criar_nota_route():
    """Criar uma nova nota
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nota
            - aluno_id
            - atividade_id
          properties:
            nota:
              type: number
              format: float
              minimum: 0
              maximum: 10
            aluno_id:
              type: integer
            atividade_id:
              type: integer
    responses:
      201:
        description: Nota criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nota:
              type: number
            aluno_id:
              type: integer
            atividade_id:
              type: integer
      400:
        description: Dados inválidos
    """
    data = request.get_json() or {}
    n = controller.criar_nota(data)
    return jsonify(n.to_dict()),201
