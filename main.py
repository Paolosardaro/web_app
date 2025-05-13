from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import os
import shutil

from gestione_dipendenti import importa_dati_excel, cerca_dipendenti, ottieni_tutti_dipendenti
from gestione_compliance import verifica_documenti_compliance  # Funzione corretta importata

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="una-chiave-segreta-casuale")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    progetto = request.session.get("progetto", "Nessun progetto selezionato")
    return templates.TemplateResponse("home.html", {"request": request, "progetto": progetto})

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "errore": None})

@app.post("/login")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    if email == "admin@example.com" and password == "password123":
        request.session["user"] = email
        return RedirectResponse("/selezione-progetto", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "errore": "Credenziali errate"})

@app.get("/selezione-progetto", response_class=HTMLResponse)
async def selezione_progetto_get(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    progetto = request.session.get("progetto")
    if progetto:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("selezione_progetto.html", {"request": request})

@app.post("/selezione-progetto")
async def selezione_progetto_post(request: Request, progetto: str = Form(...)):
    request.session["progetto"] = progetto
    return RedirectResponse("/", status_code=303)

@app.get("/gestione-dipendenti", response_class=HTMLResponse)
async def gestione_dipendenti(request: Request):
    dipendenti = ottieni_tutti_dipendenti()
    return templates.TemplateResponse("gestione_dipendenti.html", {"request": request, "dipendenti": dipendenti})

@app.post("/importa_dipendenti")
async def importa_dipendenti(request: Request):
    form = await request.form()
    file = form["file"]
    importa_dati_excel(file)
    return RedirectResponse("/gestione-dipendenti", status_code=303)

@app.post("/cerca_dipendenti")
async def cerca(request: Request, query: str = Form(...)):
    risultati = cerca_dipendenti(query)
    return templates.TemplateResponse("gestione_dipendenti.html", {"request": request, "dipendenti": risultati})

@app.get("/gestione-fuorisede", response_class=HTMLResponse)
async def gestione_fuorisede(request: Request):
    return templates.TemplateResponse("gestione_fuorisede.html", {"request": request})

@app.get("/compliance", response_class=HTMLResponse)
async def compliance(request: Request):
    return templates.TemplateResponse("compliance.html", {"request": request})

@app.post("/verifica-documenti", response_class=HTMLResponse)
async def verifica_documenti(
    request: Request,
    nome_dipendente: str = Form(...),
    inquadramento: str = Form(...),
    periodo: str = Form(None),
    file: UploadFile = Form(...)
):
    # Assicurati che la funzione ritorni due liste: documenti trovati e documenti mancanti
    documenti_trovati, documenti_mancanti = verifica_documenti_compliance(nome_dipendente, inquadramento, periodo)

    return templates.TemplateResponse("compliance_results.html", {
        "request": request,
        "documenti_trovati": documenti_trovati,
        "documenti_mancanti": documenti_mancanti
    })

@app.get("/gestione-trasferte", response_class=HTMLResponse)
async def gestione_trasferte(request: Request):
    conn = sqlite3.connect("gestione_trasferte.db")
    c = conn.cursor()
    c.execute("SELECT * FROM trasferte")
    trasferte = c.fetchall()
    conn.close()
    return templates.TemplateResponse("gestione_trasferte.html", {"request": request, "trasferte": trasferte})

@app.get("/aggiungi-trasferta", response_class=HTMLResponse)
async def aggiungi_trasferta_get(request: Request):
    return templates.TemplateResponse("aggiungi_trasferta.html", {"request": request})

@app.post("/aggiungi-trasferta")
async def aggiungi_trasferta_post(
    request: Request,
    nome_dipendente: str = Form(...),
    data_inizio: str = Form(...),
    data_fine: str = Form(...),
    inquadramento: str = Form(...),
    costo_orario: float = Form(...)
):
    conn = sqlite3.connect("gestione_trasferte.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO trasferte (nome_dipendente, data_inizio, data_fine, inquadramento, costo_orario, path_fatture) VALUES (?, ?, ?, ?, ?, ?)",
        (nome_dipendente, data_inizio, data_fine, inquadramento, costo_orario, "")
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/gestione-trasferte", status_code=303)

@app.get("/gestione-fatture", response_class=HTMLResponse)
async def gestione_fatture(request: Request):
    return templates.TemplateResponse("gestione_fatture.html", {"request": request})

@app.post("/importa-documento")
async def importa_documento(
    request: Request,
    file: UploadFile,
    nome_dipendente: str = Form(...),
    data_inizio: str = Form(...),
    data_fine: str = Form(...)
):
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    conn = sqlite3.connect("gestione_trasferte.db")
    c = conn.cursor()
    c.execute(
        """
        UPDATE trasferte
        SET path_fatture = ?
        WHERE nome_dipendente = ? AND data_inizio = ? AND data_fine = ?
        """,
        (file_path, nome_dipendente, data_inizio, data_fine)
    )
    conn.commit()
    conn.close()

    return RedirectResponse("/gestione-fatture", status_code=303)
