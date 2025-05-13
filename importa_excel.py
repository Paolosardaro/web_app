import pandas as pd
import sqlite3
from datetime import datetime

# Funzione per importare i dati da Excel al database
def importa_excel_a_db(file_path):
    # Legge il file Excel
    df = pd.read_excel(file_path)

    # Connetti al database
    conn = sqlite3.connect("gestione_trasferte.db")
    c = conn.cursor()

    # Assicurati che la tabella 'trasferte' esista
    c.execute("""
    CREATE TABLE IF NOT EXISTS trasferte (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_dipendente TEXT,
        data_inizio TEXT,
        data_fine TEXT,
        inquadramento TEXT,
        costo_orario REAL,
        path_fatture TEXT
    )
    """)

    # Cicla su ogni riga del DataFrame e inserisce nel database
    for _, row in df.iterrows():
        nome_dipendente = row['Cognome Nome']  # Usa la colonna corretta
        # Gestisci la data di inizio (Data Trasferta su Bari)
        try:
            # Converti la data in formato datetime, gestendo il timestamp
            data_inizio = pd.to_datetime(row['Data Trasferta su Bari'], errors='coerce').strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Errore durante la conversione della data: {e}")
            data_inizio = None  # Imposta a None se la data non può essere convertita

        # Altre colonne che potresti voler aggiungere (modifica in base alle tue necessità)
        inquadramento = row.get('ODS', 'N/A')  # Modifica se necessario
        costo_orario = None  # Se hai una colonna per il costo orario, mettila qui

        # Inserisci nel database
        c.execute("""
        INSERT INTO trasferte (nome_dipendente, data_inizio, inquadramento, costo_orario, path_fatture)
        VALUES (?, ?, ?, ?, ?)
        """, (nome_dipendente, data_inizio, inquadramento, costo_orario, ""))

    # Commit e chiudi la connessione
    conn.commit()
    conn.close()

# Specifica il percorso del tuo file Excel
file_excel = "trasferte.xlsx"
importa_excel_a_db(file_excel)
