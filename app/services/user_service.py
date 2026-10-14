from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import User, UserCreate, UserUpdate


def _buscar_por_email(email: str, sessao: Session) -> Optional[User]:
    """
    é uma função privada (começa com _, que diz ao python que é para ser usada apenas internamente) que busca um usuário pelo email no banco de dados.
    """
    return sessao.exec(select(User).where(User.email == email)).first()

def criar_usuario(dados: UserCreate, sessao: Session) -> User:
    if _buscar_por_email(dados.email, sessao):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    novo_usuario = User.model_validate(dados)
    sessao.add(novo_usuario)
    sessao.commit()
    sessao.refresh(novo_usuario)
    return novo_usuario


def listar_usuarios(sessao: Session) -> List[User]:
    return sessao.exec(select(User)).all()


def buscar_usuario(usuario_id: int, sessao: Session) -> User:
    usuario = sessao.get(User, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

def atualizar_usuario(usuario_id: int, dados: UserUpdate, sessao: Session) -> User:
    usuario = sessao.get(User, usuario_id)

    dados_para_atualizar = dados.model_dump(exclude_unset=True)

    #chegando email ignorando o proprio usuario, pois senão ele nunca conseguiria manter o proprio email ao atualizar outros dados
    novo_email = dados_para_atualizar.get("email")
    if novo_email and novo_email != usuario.email:
        usuario_com_esse_email = _buscar_por_email(novo_email, sessao)
        if usuario_com_esse_email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    for campo, valor in dados_para_atualizar.items():
        setattr(usuario, campo, valor)
    #glossário: setattr é uma função que recebe um objeto, o nome de um atributo e um valor, e define o atributo do objeto com o valor. Ex: setattr(usuario, "nome", "Novo Nome") é equivalente a usuario.nome = "Novo Nome"
    # model_dump(exclude_unset=True) é uma função do Pydantic que retorna um dicionário com os campos que foram definidos no objeto, ignorando os campos que não foram definidos (ou seja, que estão com valor None). Ex: se eu criar um objeto UserUpdate com apenas o campo nome definido, model_dump(exclude_unset=True) vai retornar {"nome": "Novo Nome"} e não vai incluir os campos numero, email, cpf e tipousuario.

    sessao.add(usuario)
    sessao.commit()
    sessao.refresh(usuario)
    return usuario

def deletar_usuario(usuario_id: int, sessao: Session) -> dict:
    usuario = buscar_usuario(usuario_id, sessao)
    sessao.delete(usuario)
    sessao.commit()
    return {"detail": "Usuário deletado com sucesso"}