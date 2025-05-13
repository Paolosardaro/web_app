import pandas as pd
import sqlite3
import os

DB_PATH = "dipendenti.db"

# Crea il database e la tabella se non esiste
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dipendenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cognome TEXT,
            ruolo TEXT,
            stato TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Funzione per ottenere una connessione al database
def get_db_connection():
    return sqlite3.connect(DB_PATH)

# Funzione per importare i dati da un file Excel
def importa_dati_excel(file):
    try:
        # Usa il file che viene passato come parametro
        df = pd.read_excel(file)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Pulisce la tabella prima di importare (opzionale)
        cursor.execute("DELETE FROM dipendenti")

        # Inserisce i dati nel database
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO dipendenti (nome, cognome, ruolo, stato)
                VALUES (?, ?, ?, ?)
            ''', (row['Nome'], row['Cognome'], row['Ruolo'], row['Stato']))

        conn.commit()
        conn.close()

        return {"message": "Dati importati correttamente"}
    except Exception as e:
        return {"error": str(e)}

# Funzione di ricerca nel database
def cerca_dipendenti(nome: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if nome:
        cursor.execute("SELECT * FROM dipendenti WHERE nome LIKE ?", ('%' + nome + '%',))
    else:
        cursor.execute("SELECT * FROM dipendenti")

    risultati = cursor.fetchall()
    conn.close()
    return risultati

# Funzione per ottenere tutti i dipendenti
def ottieni_tutti_dipendenti():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dipendenti")
    dipendenti = cursor.fetchall()

    conn.close()
    return dipendenti

# Funzione per ottenere statistiche sui dipendenti
def gestione_dipendenti_function():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM dipendenti")
        total_dipendenti = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dipendenti WHERE stato = 'Attivo'")
        dipendenti_attivi = cursor.fetchone()[0]

        conn.close()

        return {
            "total_dipendenti": total_dipendenti,
            "dipendenti_attivi": dipendenti_attivi
        }
    except Exception as e:
        return {"error": f"Errore nella gestione dipendenti: {str(e)}"}

# Inizializza il database all’avvio
init_db()
