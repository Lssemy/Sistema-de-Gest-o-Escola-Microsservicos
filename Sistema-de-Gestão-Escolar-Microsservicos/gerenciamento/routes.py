from flask import Blueprint, request, jsonify
from controllers import gerenciamento_controller as controller
import os
bp = Blueprint('gerenciamento', __name__)

def json_error(message, code):
    return jsonify({'error': message}), code

@bp.route('/status', methods=['GET'])
def status():
    """Status do serviço de Gerenciamento
    ---
    responses:
      200:
        description: Serviço ativo
    """
    return jsonify({'service':'gerenciamento','status':'ok'}), 200

# Alunos CRUD
@bp.route('/alunos', methods=['GET'])
def listar_alunos_route():
    """Lista todos os alunos
    ---
    responses:
      200:
        description: Lista de alunos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              idade:
                type: integer
              turma_id:
                type: integer
    """
    result = [a.to_dict() for a in controller.listar_alunos()]
    return jsonify(result), 200

@bp.route('/alunos/<int:aid>', methods=['GET'])
def get_aluno_route(aid):
    """Obter um aluno específico pelo ID
    ---
    parameters:
      - name: aid
        in: path
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Detalhes do aluno
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
      404:
        description: Aluno não encontrado
    """
    a = controller.get_aluno_by_id(aid)
    if not a: return json_error('Aluno não encontrado', 404)
    return jsonify(a.to_dict()), 200

@bp.route('/alunos', methods=['POST'])
def criar_aluno_route():
    """Criar um novo aluno
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
    responses:
      201:
        description: Aluno criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
      400:
        description: Dados inválidos
    """
    data = request.get_json() or {}
    a = controller.criar_aluno(data)
    return jsonify(a.to_dict()), 201

@bp.route('/alunos/<int:aid>', methods=['PUT'])
def atualizar_aluno_route(aid):
    """Atualizar um aluno existente
    ---
    parameters:
      - name: aid
        in: path
        type: integer
        required: true
        description: ID do aluno
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
    responses:
      200:
        description: Aluno atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
      404:
        description: Aluno não encontrado
    """
    data = request.get_json() or {}
    a = controller.atualizar_aluno(aid, data)
    if not a: return json_error('Aluno não encontrado', 404)
    return jsonify(a.to_dict()), 200

@bp.route('/alunos/<int:aid>', methods=['DELETE'])
def deletar_aluno_route(aid):
    """Excluir um aluno
    ---
    parameters:
      - name: aid
        in: path
        type: integer
        required: true
        description: ID do aluno
    responses:
      204:
        description: Aluno excluído com sucesso
      404:
        description: Aluno não encontrado
    """
    ok = controller.deletar_aluno(aid)
    if not ok: return json_error('Aluno não encontrado', 404)
    return jsonify({}), 204

# Professores CRUD
@bp.route('/professores', methods=['GET'])
def listar_professores_route():
    """Lista todos os professores
    ---
    responses:
      200:
        description: Lista de professores
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              idade:
                type: integer
              materia:
                type: string
    """
    result = [p.to_dict() for p in controller.listar_professores()]
    return jsonify(result), 200

@bp.route('/professores/<int:pid>', methods=['GET'])
def get_professor_route(pid):
    """Obter um professor específico pelo ID
    ---
    parameters:
      - name: pid
        in: path
        type: integer
        required: true
        description: ID do professor
    responses:
      200:
        description: Detalhes do professor
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
      404:
        description: Professor não encontrado
    """
    p = controller.get_professor_by_id(pid)
    if not p: return json_error('Professor não encontrado', 404)
    return jsonify(p.to_dict()), 200

@bp.route('/professores', methods=['POST'])
def criar_professor_route():
    """Criar um novo professor
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
    responses:
      201:
        description: Professor criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
      400:
        description: Dados inválidos
    """
    data = request.get_json() or {}
    p = controller.criar_professor(data)
    return jsonify(p.to_dict()), 201

@bp.route('/professores/<int:pid>', methods=['PUT'])
def atualizar_professor_route(pid):
    """Atualizar um professor existente
    ---
    parameters:
      - name: pid
        in: path
        type: integer
        required: true
        description: ID do professor
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
    responses:
      200:
        description: Professor atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
      404:
        description: Professor não encontrado
    """
    data = request.get_json() or {}
    p = controller.atualizar_professor(pid, data)
    if not p: return json_error('Professor não encontrado', 404)
    return jsonify(p.to_dict()), 200

@bp.route('/professores/<int:pid>', methods=['DELETE'])
def deletar_professor_route(pid):
    """Excluir um professor
    ---
    parameters:
      - name: pid
        in: path
        type: integer
        required: true
        description: ID do professor
    responses:
      204:
        description: Professor excluído com sucesso
      404:
        description: Professor não encontrado
    """
    ok = controller.deletar_professor(pid)
    if not ok: return json_error('Professor não encontrado', 404)
    return jsonify({}), 204

# Turmas CRUD
@bp.route('/turmas', methods=['GET'])
def listar_turmas_route():
    """Lista todas as turmas
    ---
    responses:
      200:
        description: Lista de turmas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              descricao:
                type: string
              professor_id:
                type: integer
              ativo:
                type: boolean
    """
    result = [t.to_dict() for t in controller.listar_turmas()]
    return jsonify(result), 200

@bp.route('/turmas/<int:tid>', methods=['GET'])
def get_turma_route(tid):
    """Obter uma turma específica pelo ID
    ---
    parameters:
      - name: tid
        in: path
        type: integer
        required: true
        description: ID da turma
    responses:
      200:
        description: Detalhes da turma
        schema:
          type: object
          properties:
            id:
              type: integer
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
      404:
        description: Turma não encontrada
    """
    t = controller.get_turma_by_id(tid)
    if not t: return json_error('Turma não encontrada', 404)
    return jsonify(t.to_dict()), 200

@bp.route('/turmas', methods=['POST'])
def criar_turma_route():
    """Criar uma nova turma
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - descricao
            - professor_id
          properties:
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
              default: true
    responses:
      201:
        description: Turma criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
      400:
        description: Dados inválidos
    """
    data = request.get_json() or {}
    t = controller.criar_turma(data)
    return jsonify(t.to_dict()), 201

@bp.route('/turmas/<int:tid>', methods=['PUT'])
def atualizar_turma_route(tid):
    """Atualizar uma turma existente
    ---
    parameters:
      - name: tid
        in: path
        type: integer
        required: true
        description: ID da turma
      - in: body
        name: body
        schema:
          type: object
          properties:
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
    responses:
      200:
        description: Turma atualizada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
      404:
        description: Turma não encontrada
    """
    data = request.get_json() or {}
    t = controller.atualizar_turma(tid, data)
    if not t: return json_error('Turma não encontrada', 404)
    return jsonify(t.to_dict()), 200

@bp.route('/turmas/<int:tid>', methods=['DELETE'])
def deletar_turma_route(tid):
    """Excluir uma turma
    ---
    parameters:
      - name: tid
        in: path
        type: integer
        required: true
        description: ID da turma
    responses:
      204:
        description: Turma excluída com sucesso
      404:
        description: Turma não encontrada
    """
    ok = controller.deletar_turma(tid)
    if not ok: return jsonify({'error':'Turma não encontrada'}), 404
    return jsonify({}), 204