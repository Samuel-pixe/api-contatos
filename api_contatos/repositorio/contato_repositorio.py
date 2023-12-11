from __future__ import annotations 
from sqlalchemy.orm import Session
from models.contato import Contato

class ContatoRepository:

    @staticmethod
    def get_all(db:Session) -> list([Contato]):
        return db.query(Contato).all()

    @staticmethod
    def salvar(db: Session, Contato: Contato) -> Contato:
        if Contato.id:
            db.merge(Contato)
        else:
            db.add(Contato)
        db.commit()
        return Contato

    @staticmethod
    def get_by_id(db: Session, id: int) -> Contato:
        return db.query(Contato).filter(Contato.id == id).first()

    @staticmethod
    def existe_by_id(db: Session, id: int) -> bool:
        return db.query(Contato).filter(Contato.id == id).first() is not None

    @staticmethod
    def deletar(db: Session, id: int) -> None:
        contato = db.query(Contato).filter(Contato.id == id).first()
        if contato is not None:
            db.delete(contato)
            db.commit()
