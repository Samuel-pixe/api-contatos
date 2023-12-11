from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models.contato import Contato, ContatoRequest, ContatoResponse
from data.config import engine, Base, get_db
from repositorio.contato_repositorio import ContatoRepository


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    '''
        Esta API tem como objetivo implementar uma solução para
        gerenciamento de Contatos
    '''
    return {"mensagem": "API Contatos"}


@app.post("/api/contatos", response_model=ContatoResponse, status_code=status.HTTP_201_CREATED)
def create(request: ContatoRequest, db: Session = Depends(get_db)):
    '''
        Adicionar novos contatos.
    '''
    contato = ContatoRepository.salvar(db, Contato(**request.dict()))
    return ContatoResponse.from_orm(contato)

@app.get("/api/contatos/{id}", response_model=ContatoResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    '''
        Retornar as informações de um Contato a partir do ID
    '''
    contato = ContatoRepository.get_by_id(db, id)
    if not contato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado"
        )
    return ContatoResponse.from_orm(contato)
 
@app.delete("/api/contatos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: int, db: Session = Depends(get_db)):
    '''
        Apagar todas as informações de um contato
    '''
    if not ContatoRepository.existe_by_id(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    ContatoRepository.deletar(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/contatos/{id}", response_model=ContatoResponse)
def update(id: int, request: ContatoRequest, db: Session = Depends(get_db)):
    '''
        Atualizar as informações de um contato a partir do ID
    '''
    if not ContatoRepository.existe_by_id(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato não encontrado")
    contato = ContatoRepository.salvar(db, Contato(id=id, **request.dict()))
    return ContatoResponse.from_orm(contato)


@app.get("/api/contatos")
def get_all(db: Session = Depends(get_db)):
    '''
        Listar todos os contatos
    '''
    contatos = ContatoRepository.get_all(db)
    return [ContatoResponse.from_orm(contato) for contato in contatos]