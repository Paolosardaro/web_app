import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
import fitz  # PyMuPDF

# Funzione per aprire la finestra di analisi dati
def open_analisi_dati_window():
    # Finestra per la selezione dei dati
    analysis_window = tk.Toplevel()
    analysis_window.title("Analisi Dati")
    analysis_window.geometry("600x400")

    # Etichette e caselle di input
    label = tk.Label(analysis_window, text="Seleziona il dipendente e altre opzioni", font=("Arial", 14))
    label.pack(pady=10)

    # Selezione del dipendente
    label_dipendente = tk.Label(analysis_window, text="Nome dipendente:")
    label_dipendente.pack(pady=5)
    entry_dipendente = tk.Entry(analysis_window)
    entry_dipendente.pack(pady=5)

    # Selezione inquadramento
    label_inquadramento = tk.Label(analysis_window, text="Seleziona inquadramento:")
    label_inquadramento.pack(pady=5)
    
    inquadramento_options = ["Quadro", "Dirigente", "Impiegato"]
    combo_inquadramento = ttk.Combobox(analysis_window, values=inquadramento_options)
    combo_inquadramento.pack(pady=5)
    
    # Valore monetario
    label_valore = tk.Label(analysis_window, text="Valore Monetario:")
    label_valore.pack(pady=5)
    entry_valore = tk.Entry(analysis_window)
    entry_valore.pack(pady=5)

    # Pulsante per generare i grafici e le tabelle
    def generate_analysis():
        dipendente = entry_dipendente.get()
        inquadramento = combo_inquadramento.get()
        valore = entry_valore.get()

        # Verifica che i campi siano stati riempiti
        if not dipendente or not inquadramento or not valore:
            tk.messagebox.showerror("Errore", "Per favore, compila tutti i campi.")
            return

        # Logica per l'analisi dei dati
        try:
            # Esegui l'analisi sul database, ad esempio una query
            conn = sqlite3.connect("azienda.db")
            cursor = conn.cursor()
            
            # Qui aggiungi la logica per analizzare i dati, ad esempio una query sui dati
            query = f"SELECT * FROM trasferte WHERE dipendente = ? AND inquadramento = ?"
            cursor.execute(query, (dipendente, inquadramento))
            rows = cursor.fetchall()
            
            # Mostra i risultati in una tabella (o un grafico)
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Dipendente", "Inquadramento", "Data Trasferta", "Fattura", "Importo"])
                print(df)

                # Visualizza un grafico
                df.plot(kind="bar", x="Dipendente", y="Importo", title="Importo Trasferta per Dipendente")
                plt.show()
            else:
                tk.messagebox.showinfo("Nessun risultato", "Nessun dato trovato per i criteri selezionati.")
            
            conn.close()
        except Exception as e:
            tk.messagebox.showerror("Errore", f"Si è verificato un errore durante l'analisi dei dati: {e}")

    btn_generate = tk.Button(analysis_window, text="Genera Grafico e Tabella", command=generate_analysis)
    btn_generate.pack(pady=20)

    analysis_window.mainloop()

# Funzione per analizzare i dati locali, come nel primo script
def analizza_dati_domanda(domanda):
    risposta = ""
    folder = "allegati"
    domanda = domanda.lower()

    if not os.path.exists(folder):
        return "⚠️ Cartella 'allegati' non trovata."

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        # Lettura file .txt
        if file.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                contenuto = f.read().lower()
                if domanda in contenuto:
                    risposta += f"\n🔹 Trovato in '{file}':\n{contenuto[:300]}...\n"

        # Lettura file .csv
        elif file.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                for col in df.columns:
                    if df[col].astype(str).str.contains(domanda, case=False).any():
                        risposta += f"\n🔹 Valore trovato in '{file}' nella colonna '{col}'\n"
            except Exception as e:
                risposta += f"\n⚠️ Errore con '{file}': {e}\n"

        # Lettura file .pdf
        elif file.endswith(".pdf"):
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                text = text.lower()
                if domanda in text:
                    risposta += f"\n🔹 Trovato in '{file}':\n{text[:300]}...\n"
            except Exception as e:
                risposta += f"\n⚠️ Errore nella lettura di '{file}': {e}\n"

    return risposta if risposta else "Nessuna informazione trovata nei dati locali."
