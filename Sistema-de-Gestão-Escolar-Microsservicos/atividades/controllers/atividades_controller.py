from models.models import Atividade, Nota
from database import db

def _commit():
    db.session.commit()

def listar_atividades():
    return Atividade.query.all()

def get_atividade_by_id(aid):
    return Atividade.query.get(aid)

def criar_atividade(data):
    a = Atividade(titulo=data.get('titulo'), descricao=data.get('descricao'), peso_porcento=data.get('peso_porcento'), data_entrega=data.get('data_entrega'), turma_id=data.get('turma_id'), professor_id=data.get('professor_id'))
    db.session.add(a)
    _commit()
    return a

def atualizar_atividade(aid, data):
    a = Atividade.query.get(aid)
    if not a: return None
    a.titulo = data.get('titulo', a.titulo)
    a.descricao = data.get('descricao', a.descricao)
    a.peso_porcento = data.get('peso_porcento', a.peso_porcento)
    a.data_entrega = data.get('data_entrega', a.data_entrega)
    a.turma_id = data.get('turma_id', a.turma_id)
    a.professor_id = data.get('professor_id', a.professor_id)
    _commit()
    return a

def deletar_atividade(aid):
    a = Atividade.query.get(aid)
    if not a: return False
    db.session.delete(a)
    _commit()
    return True

# Notas
def listar_notas():
    return Nota.query.all()
def criar_nota(data):
    n = Nota(nota=data.get('nota'), aluno_id=data.get('aluno_id'), atividade_id=data.get('atividade_id'))
    db.session.add(n)
    _commit()
    return n
