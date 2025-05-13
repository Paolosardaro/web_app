from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import os

from gestione_dipendenti import importa_dati_excel, cerca_dipendenti, ottieni_tutti_dipendenti

# Crea l'app FastAPI
app = FastAPI()

# Sessioni per login e progetto
app.add_middleware(SessionMiddleware, secret_key="una-chiave-segreta-casuale")

# Configura i template e i file statici
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ HOME CON CONTROLLO LOGIN
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    progetto = request.session.get("progetto", "Nessun progetto selezionato")
    return templates.TemplateResponse("home.html", {"request": request, "progetto": progetto})

# GESTIONE DIPENDENTI
@app.get("/gestione-dipendenti", response_class=HTMLResponse)
async def gestione_dipendenti(request: Request):
    dipendenti = ottieni_tutti_dipendenti()
    return templates.TemplateResponse("gestione_dipendenti.html", {"request": request, "dipendenti": dipendenti})

@app.post("/importa_dipendenti")
async def importa_dipendenti(request: Request):
    form = await request.form()
    file = form["file"]
    importa_dati_excel(file)
    return RedirectResponse("/gestione_dipendenti", status_code=303)

@app.post("/cerca_dipendenti")
async def cerca(request: Request, query: str = Form(...)):
    risultati = cerca_dipendenti(query)
    return templates.TemplateResponse("gestione_dipendenti.html", {"request": request, "dipendenti": risultati})

# ALTRE SEZIONI
@app.get("/gestione_fuorisede", response_class=HTMLResponse)
async def gestione_fuorisede(request: Request):
    return templates.TemplateResponse("gestione_fuorisede.html", {"request": request})

@app.get("/compliance", response_class=HTMLResponse)
async def compliance(request: Request):
    return templates.TemplateResponse("compliance.html", {"request": request})

@app.get("/sezione_analisi_dati", response_class=HTMLResponse)
async def sezione_analisi_dati(request: Request):
    return templates.TemplateResponse("sezione_analisi_dati.html", {"request": request})

@app.get("/sezione_ia", response_class=HTMLResponse)
async def sezione_ia(request: Request):
    return templates.TemplateResponse("sezione_ia.html", {"request": request})

@app.get("/sezione_dati_incrociati", response_class=HTMLResponse)
async def sezione_dati_incrociati(request: Request):
    return templates.TemplateResponse("sezione_dati_incrociati.html", {"request": request})

@app.get("/sezione_gestione_fatture", response_class=HTMLResponse)
async def sezione_gestione_fatture(request: Request):
    return templates.TemplateResponse("sezione_gestione_fatture.html", {"request": request})

@app.get("/sezione_gestione_trasferte", response_class=HTMLResponse)
async def sezione_gestione_trasferte(request: Request):
    return templates.TemplateResponse("sezione_gestione_trasferte.html", {"request": request})

# ✅ LOGIN
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse("/", status_code=303)  # Se l'utente è già loggato, reindirizza alla home
    return templates.TemplateResponse("login.html", {"request": request, "errore": None})  # Nessun errore per il login iniziale

@app.post("/login")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    if email == "admin@example.com" and password == "password123":
        request.session["user"] = email
        return RedirectResponse("/selezione-progetto", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "errore": "Credenziali errate"})

# ✅ SELEZIONE PROGETTO
@app.get("/selezione-progetto", response_class=HTMLResponse)
async def selezione_progetto_get(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)  # Se non è loggato, reindirizza alla pagina di login

    progetto = request.session.get("progetto")
    if progetto:
        return RedirectResponse("/", status_code=303)  # Se il progetto è già selezionato, reindirizza alla home

    return templates.TemplateResponse("selezione_progetto.html", {"request": request})

@app.post("/selezione-progetto")
async def selezione_progetto_post(request: Request, progetto: str = Form(...)):
    request.session["progetto"] = progetto
    return RedirectResponse("/", status_code=303)

# ✅ LOGOUT
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()  # Cancella la sessione
    return RedirectResponse("/login", status_code=303)  # Reindirizza alla pagina di login
