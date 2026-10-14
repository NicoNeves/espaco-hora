"""
models.py
---------
Aqui definimos como a tabela "Sala" vai existir dentro do banco de dados.

Estamos usando a biblioteca SQLModel, que junta duas coisas em uma só classe:

1) Validação de dados (o que o Pydantic faz) -> garante que "capacidade"
   seja um número, que "nome" seja um texto, etc.
2) Mapeamento para o banco (o que o SQLAlchemy faz) -> transforma essa
   classe Python em uma tabela SQL de verdade.

Ou seja: uma classe só = o "formato" dos dados E a tabela do banco.
"""

from pydantic import EmailStr
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field

class TipoUsuario(str, Enum):
    CLIENTE ="cliente"
    ADMIN_LOCADORA = "admin_locadora"
    ADMIN_PLATAFORMA = "admin_plataforma"

class StatusSala(str, Enum):
    LIVRE = "livre"
    OCUPADA = "ocupada"

# USER

#table=True indica que essa classe vai virar uma tabela no banco de dados

#field(default=None, primary_key=True) indica que o campo é a chave primária da tabela e que o valor padrão é None (ou seja, o banco vai gerar o valor automaticamente)

class User(SQLModel, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   nome: str
   numero: str
   email: str
   senha: str
   cpf: str
   tipousuario: TipoUsuario

class UserCreate(SQLModel):
    nome: str
    numero: str
    email: EmailStr
    senha: str
    cpf: str
    tipousuario: TipoUsuario

class UserUpdate(SQLModel):
    nome: Optional[str] = None
    numero: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    cpf: Optional[str] = None
    tipousuario: Optional[TipoUsuario] = None

# SALAS

class Sala(SQLModel, table =True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    status: StatusSala = Field(default=StatusSala.LIVRE)

class SalaCreate(SQLModel):
    nome: str
    descricao: str

class SalaUpdate(SQLModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusSala] = None