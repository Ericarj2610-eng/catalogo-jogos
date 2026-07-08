from contextlib import asynccontextmanager
from datetime import date
from decimal import Decimal

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


templates = Jinja2Templates(
    directory="templates"
)


@app.get("/")
def home():
    return RedirectResponse(
        url="/jogos"
    )


# LISTAR JOGOS

@app.get("/jogos")
def listar(
    request: Request,
    session: Session = Depends(get_session)
):

    jogos = session.scalars(
        select(models.Jogo)
    ).all()


    return templates.TemplateResponse(
        request,
        "lista.html",
        {
            "jogos": jogos
        }
    )



# FORMULÁRIO NOVO

@app.get("/jogos/novo")
def form_novo(
    request: Request,
    session: Session = Depends(get_session)
):

    generos = session.scalars(
        select(models.Genero)
    ).all()


    return templates.TemplateResponse(
        request,
        "form.html",
        {
            "jogo": None,
            "generos": generos
        }
    )



# CRIAR JOGO

@app.post("/jogos")
def criar(
    titulo: str = Form(...),
    desenvolvedora: str = Form(...),
    data_lancamento: date = Form(...),
    genero_id: int = Form(...),
    preco: Decimal = Form(...),
    session: Session = Depends(get_session)
):

    jogo = models.Jogo(
        titulo=titulo,
        desenvolvedora=desenvolvedora,
        data_lancamento=data_lancamento,
        genero_id=genero_id,
        preco=preco
    )


    session.add(jogo)
    session.commit()


    return RedirectResponse(
        "/jogos",
        status_code=303
    )



# FORMULÁRIO EDITAR

@app.get("/jogos/{jogo_id}/editar")
def editar_form(
    jogo_id: int,
    request: Request,
    session: Session = Depends(get_session)
):

    jogo = session.get(
        models.Jogo,
        jogo_id
    )


    generos = session.scalars(
        select(models.Genero)
    ).all()


    return templates.TemplateResponse(
        request,
        "form.html",
        {
            "jogo": jogo,
            "generos": generos
        }
    )



# ATUALIZAR

@app.post("/jogos/{jogo_id}/editar")
def atualizar(
    jogo_id: int,
    titulo: str = Form(...),
    desenvolvedora: str = Form(...),
    data_lancamento: date = Form(...),
    genero_id: int = Form(...),
    preco: Decimal = Form(...),
    session: Session = Depends(get_session)
):

    jogo = session.get(
        models.Jogo,
        jogo_id
    )


    jogo.titulo = titulo
    jogo.desenvolvedora = desenvolvedora
    jogo.data_lancamento = data_lancamento
    jogo.genero_id = genero_id
    jogo.preco = preco


    session.commit()


    return RedirectResponse(
        "/jogos",
        status_code=303
    )



# EXCLUIR

@app.post("/jogos/{jogo_id}/excluir")
def excluir(
    jogo_id: int,
    session: Session = Depends(get_session)
):

    jogo = session.get(
        models.Jogo,
        jogo_id
    )


    session.delete(jogo)
    session.commit()


    return RedirectResponse(
        "/jogos",
        status_code=303
    )