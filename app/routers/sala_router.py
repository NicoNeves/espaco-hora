
"""
sala_router.py
---------------
Rotas de Sala. Mesmo padrão do user_router.py.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import obter_sessao
from app.models import Sala, SalaCreate, SalaUpdate
from app.services import sala_service

router = APIRouter(prefix="/salas", tags=["salas"])


@router.post("/", response_model=Sala)
def criar_sala(dados: SalaCreate, sessao: Session = Depends(obter_sessao)):
    return sala_service.criar_sala(dados, sessao)


@router.get("/", response_model=List[Sala])
def listar_salas(sessao: Session = Depends(obter_sessao)):
    return sala_service.listar_salas(sessao)


@router.get("/{sala_id}", response_model=Sala)
def buscar_sala(sala_id: int, sessao: Session = Depends(obter_sessao)):
    return sala_service.buscar_sala(sala_id, sessao)


@router.put("/{sala_id}", response_model=Sala)
def atualizar_sala(sala_id: int, dados: SalaUpdate, sessao: Session = Depends(obter_sessao)):
    return sala_service.atualizar_sala(sala_id, dados, sessao)


@router.delete("/{sala_id}")
def deletar_sala(sala_id: int, sessao: Session = Depends(obter_sessao)):
    return sala_service.deletar_sala(sala_id, sessao)