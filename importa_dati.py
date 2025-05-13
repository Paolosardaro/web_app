import pandas as pd
import sqlite3

# Percorso del file Excel e del database
file_excel = "dipendenti.xlsx"
DB_PATH = "dipendenti.db"

# Funzione per importare i dati da un file Excel
def importa_dati_excel(file):
    try:
        # Leggi il file Excel
        df = pd.read_excel(file)

        # Connessione al database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Pulisce la tabella prima di importare (opzionale)
        cursor.execute("DELETE FROM dipendenti")

        # Inserisce i dati nel database
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO dipendenti (nome, cognome, ruolo, stato)
                VALUES (?, ?, ?, ?)
            ''', (row['Nome'], row['Cognome'], row['Ruolo'], row['Stato']))

        # Conferma le modifiche e chiudi la connessione
        conn.commit()
        conn.close()

        print("Dati importati correttamente.")
    except Exception as e:
        print(f"Errore: {str(e)}")

# Chiamata alla funzione per importare i dati
importa_dati_excel(file_excel)