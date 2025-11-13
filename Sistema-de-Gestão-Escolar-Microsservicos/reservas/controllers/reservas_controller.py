from models.models import Reserva
from database import db

def _commit():
    db.session.commit()

def listar_reservas():
    return Reserva.query.all()

def get_reserva_by_id(rid):
    return Reserva.query.get(rid)

def criar_reserva(data):
    r = Reserva(num_sala=data.get('num_sala'), lab=data.get('lab', False), data=data.get('data'), turma_id=data.get('turma_id'))
    db.session.add(r)
    _commit()
    return r

def atualizar_reserva(rid, data):
    r = Reserva.query.get(rid)
    if not r: return None
    r.num_sala = data.get('num_sala', r.num_sala)
    r.lab = data.get('lab', r.lab)
    r.data = data.get('data', r.data)
    r.turma_id = data.get('turma_id', r.turma_id)
    _commit()
    return r

def deletar_reserva(rid):
    r = Reserva.query.get(rid)
    if not r: return False
    db.session.delete(r)
    _commit()
    return True
