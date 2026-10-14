"""
Rotas de usuário. Cada função aqui só recebe a requisição, chama o
service correspondente, e devolve o resultado -- sem decidir nada
de negócio sozinha.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import obter_sessao
from app.models import User, UserCreate, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


#response_model é um jeito de dizer ao fastAPI que o retorno da função deve ser convertido para o modelo especificado
@router.post("/", response_model=User)
def criar_usuario(dados: UserCreate, sessao: Session = Depends(obter_sessao)):
    return user_service.criar_usuario(dados, sessao)


@router.get("/", response_model=List[User])
def listar_usuarios(sessao: Session = Depends(obter_sessao)):
    return user_service.listar_usuarios(sessao)


@router.get("/{usuario_id}", response_model=User)
def buscar_usuario(usuario_id: int, sessao: Session = Depends(obter_sessao)):
    return user_service.buscar_usuario(usuario_id, sessao)


@router.put("/{usuario_id}", response_model=User)
def atualizar_usuario(usuario_id: int, dados: UserUpdate, sessao: Session = Depends(obter_sessao)):
    return user_service.atualizar_usuario(usuario_id, dados, sessao)


# Sem response_model de propósito: essa rota devolve uma mensagem,
@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, sessao: Session = Depends(obter_sessao)):
    return user_service.deletar_usuario(usuario_id, sessao)