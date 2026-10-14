"""
sala_service.py
----------------
Regras de negócio relacionadas a sala. Segue exatamente o mesmo
padrão do user_service.py -- se você entendeu um, entendeu o outro.
"""

from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Sala, SalaCreate, SalaUpdate


def _buscar_por_nome(nome: str, sessao: Session) -> Optional[Sala]:
    return sessao.exec(select(Sala).where(Sala.nome == nome)).first()


def criar_sala(dados: SalaCreate, sessao: Session) -> Sala:
    if _buscar_por_nome(dados.nome, sessao):
        raise HTTPException(
            status_code=400,
            detail="Já existe uma sala cadastrada com esse nome.",
        )

    nova_sala = Sala.model_validate(dados)
    sessao.add(nova_sala)
    sessao.commit()
    sessao.refresh(nova_sala)
    return nova_sala


def listar_salas(sessao: Session) -> List[Sala]:
    return sessao.exec(select(Sala)).all()


def buscar_sala(sala_id: int, sessao: Session) -> Sala:
    sala = sessao.get(Sala, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")
    return sala


def atualizar_sala(sala_id: int, dados: SalaUpdate, sessao: Session) -> Sala:
    sala = buscar_sala(sala_id, sessao)

    dados_para_atualizar = dados.model_dump(exclude_unset=True)

    novo_nome = dados_para_atualizar.get("nome")
    if novo_nome and novo_nome != sala.nome:
        sala_com_esse_nome = _buscar_por_nome(novo_nome, sessao)
        if sala_com_esse_nome:
            raise HTTPException(
                status_code=400,
                detail="Já existe uma sala cadastrada com esse nome.",
            )

    for campo, valor in dados_para_atualizar.items():
        setattr(sala, campo, valor)

    sessao.add(sala)
    sessao.commit()
    sessao.refresh(sala)
    return sala


def deletar_sala(sala_id: int, sessao: Session) -> dict:
    sala = buscar_sala(sala_id, sessao)
    sessao.delete(sala)
    sessao.commit()
    return {"mensagem": "Sala deletada com sucesso."}