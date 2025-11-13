from models.models import Aluno, Professor, Turma
from database import db

def _commit():
    db.session.commit()
# Alunos
def listar_alunos():
    return Aluno.query.all()
def get_aluno_by_id(aid):
    return Aluno.query.get(aid)
def criar_aluno(data):
    a = Aluno(nome=data.get('nome'), idade=data.get('idade'), turma_id=data.get('turma_id'))
    db.session.add(a)
    _commit()
    return a
def atualizar_aluno(aid, data):
    a = Aluno.query.get(aid)
    if not a: return None
    a.nome = data.get('nome', a.nome)
    a.idade = data.get('idade', a.idade)
    a.turma_id = data.get('turma_id', a.turma_id)
    _commit()
    return a
def deletar_aluno(aid):
    a = Aluno.query.get(aid)
    if not a: return False
    db.session.delete(a)
    _commit()
    return True
# Professores
def listar_professores():
    return Professor.query.all()
def get_professor_by_id(pid):
    return Professor.query.get(pid)
def criar_professor(data):
    p = Professor(nome=data.get('nome'), idade=data.get('idade'), materia=data.get('materia'))
    db.session.add(p)
    _commit()
    return p
def atualizar_professor(pid, data):
    p = Professor.query.get(pid)
    if not p: return None
    p.nome = data.get('nome', p.nome)
    p.idade = data.get('idade', p.idade)
    p.materia = data.get('materia', p.materia)
    _commit()
    return p
def deletar_professor(pid):
    p = Professor.query.get(pid)
    if not p: return False
    db.session.delete(p)
    _commit()
    return True
# Turmas
def listar_turmas():
    return Turma.query.all()
def get_turma_by_id(tid):
    return Turma.query.get(tid)
def criar_turma(data):
    t = Turma(descricao=data.get('descricao'), professor_id=data.get('professor_id'), ativo=data.get('ativo', True))
    db.session.add(t)
    _commit()
    return t
def atualizar_turma(tid, data):
    t = Turma.query.get(tid)
    if not t: return None
    t.descricao = data.get('descricao', t.descricao)
    t.professor_id = data.get('professor_id', t.professor_id)
    t.ativo = data.get('ativo', t.ativo)
    _commit()
    return t
def deletar_turma(tid):
    t = Turma.query.get(tid)
    if not t: return False
    db.session.delete(t)
    _commit()
    return True
