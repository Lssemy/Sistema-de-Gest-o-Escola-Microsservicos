from flask import Blueprint, request, jsonify
from controllers import reservas_controller as controller
import os
import requests
bp = Blueprint('reservas', __name__)
GER_URL = os.environ.get('GERENCIAMENTO_URL','http://gerenciamento:5000')

def json_error(message, code):
    return jsonify({'error': message}), code

@bp.route('/status', methods=['GET'])
def status():
    """Status do serviço de Reservas
    ---
    responses:
      200:
        description: Status do serviço
        schema:
          properties:
            service:
              type: string
              example: reservas
            status:
              type: string
              example: ok
    """
    return jsonify({'service':'reservas','status':'ok'}),200

@bp.route('/reservas', methods=['GET'])
def listar():
    """Lista todas as reservas de sala
    ---
    responses:
      200:
        description: Lista de reservas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              num_sala:
                type: string
              lab:
                type: boolean
              data:
                type: string
                format: date
              turma_id:
                type: integer
    """
    return jsonify([r.to_dict() for r in controller.listar_reservas()]),200

@bp.route('/reservas/<int:rid>', methods=['GET'])
def obter(rid):
    """Obter uma reserva específica pelo ID
    ---
    parameters:
      - name: rid
        in: path
        type: integer
        required: true
        description: ID da reserva
    responses:
      200:
        description: Detalhes da reserva
        schema:
          type: object
          properties:
            id:
              type: integer
            num_sala:
              type: string
            lab:
              type: boolean
            data:
              type: string
              format: date
            turma_id:
              type: integer
      404:
        description: Reserva não encontrada
    """
    r = controller.get_reserva_by_id(rid)
    if not r: return json_error('Reserva não encontrada', 404)
    return jsonify(r.to_dict()),200

@bp.route('/reservas', methods=['POST'])
def criar():
    """Criar uma nova reserva de sala
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - num_sala
            - data
            - turma_id
          properties:
            num_sala:
              type: string
              example: "101"
            lab:
              type: boolean
              default: false
            data:
              type: string
              format: date
              example: "2025-11-20"
            turma_id:
              type: integer
    responses:
      201:
        description: Reserva criada com sucesso
      400:
        description: Dados inválidos ou turma não encontrada
      503:
        description: Erro ao contactar serviço de gerenciamento
    """
    data = request.get_json() or {}
    turma_id = data.get('turma_id')
    if not turma_id: return json_error('turma_id obrigatório', 400)
    try:
        resp = requests.get(f"{GER_URL}/turmas/{turma_id}", timeout=3)
    except requests.RequestException:
        return json_error('Falha ao contactar gerenciamento', 503)
    if resp.status_code != 200: return json_error('Turma inexistente', 400)
    r = controller.criar_reserva(data)
    return jsonify(r.to_dict()),201

@bp.route('/reservas/<int:rid>', methods=['PUT'])
def atualizar(rid):
    """Atualizar uma reserva existente
    ---
    parameters:
      - name: rid
        in: path
        type: integer
        required: true
        description: ID da reserva
      - in: body
        name: body
        schema:
          type: object
          properties:
            num_sala:
              type: string
            lab:
              type: boolean
            data:
              type: string
              format: date
            turma_id:
              type: integer
    responses:
      200:
        description: Reserva atualizada com sucesso
      400:
        description: Dados inválidos ou turma não encontrada
      404:
        description: Reserva não encontrada
      503:
        description: Erro ao contactar serviço de gerenciamento
    """
    data = request.get_json() or {}
    turma_id = data.get('turma_id')
    if turma_id:
        try:
            resp = requests.get(f"{GER_URL}/turmas/{turma_id}", timeout=3)
        except requests.RequestException:
            return jsonify({'error':'Falha ao contactar gerenciamento'}),503
        if resp.status_code != 200: return jsonify({'error':'Turma inexistente'}),400
    r = controller.atualizar_reserva(rid, data)
    if not r: return json_error('Reserva não encontrada', 404)
    return jsonify(r.to_dict()),200

@bp.route('/reservas/<int:rid>', methods=['DELETE'])
def deletar(rid):
    """Excluir uma reserva
    ---
    parameters:
      - name: rid
        in: path
        type: integer
        required: true
        description: ID da reserva
    responses:
      204:
        description: Reserva excluída com sucesso
      404:
        description: Reserva não encontrada
    """
    ok = controller.deletar_reserva(rid)
    if not ok: return json_error('Reserva não encontrada', 404)
    return jsonify({}),204
