"""
Este é o arquivo principal da API. Aqui vivem as ROTAS: os endereços
que o Bubble vai chamar para criar,
listar, atualizar e deletar salas.

Como rodar:
#    1. source venv/bin/activate (ou venv(barra invertida)Scripts(barra invertida)activate no Windows) para ativar o ambiente virtual
    1. pip install -r requirements.txt caso ainda não tenha instalado as dependências
    2. uvicorn app.main:app --reload
    3. Abra http://127.0.0.1:8000/docs no navegador

Esse /docs é uma tela AUTOMÁTICA que o FastAPI gera, onde dá pra testar cada rota clicando em botões
"""
from fastapi import FastAPI  
from app.routers import user_router, sala_router
from app.database import criar_banco_e_tabelas


# "app" é a instância principal da nossa API. É nela que penduramos todas as rotas abaixo.
app = FastAPI()

app.include_router(user_router.router)
app.include_router(sala_router.router)


@app.on_event("startup")
def ao_iniciar():
    criar_banco_e_tabelas()
