from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.config import Base

class Contato(Base):
    __tablename__ = "tb_contatos"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    telefone: str = Column(String(50), nullable=False)
    email: str = Column(String(120), nullable=False)
    pais: str = Column(String(80), nullable=False)

class ContatoBase(BaseModel):
    nome: str
    telefone: str
    email: str
    pais: str

class ContatoRequest(ContatoBase):
    ...

class ContatoResponse(ContatoBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True