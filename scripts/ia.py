import os
import shutil
import pandas as pd
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import messagebox, filedialog
from gestione_analisi_dati import analizza_dati_domanda  # Importiamo la funzione di analisi dei dati

# Funzione di analisi dei dati (già fornita nel primo script)
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

# Funzione per caricare un documento nella cartella 'allegati'
def carica_documento():
    # Apri una finestra di dialogo per selezionare il file
    file_path = filedialog.askopenfilename(title="Seleziona un documento", filetypes=[("Tutti i file", "*.*"), ("PDF", "*.pdf"), ("CSV", "*.csv"), ("Testo", "*.txt")])
    
    if file_path:
        # Verifica se la cartella 'allegati' esiste, altrimenti la crea
        folder = "allegati"
        if not os.path.exists(folder):
            os.makedirs(folder)  # Crea la cartella se non esiste

        # Copia il file nella cartella 'allegati'
        try:
            shutil.copy(file_path, folder)
            messagebox.showinfo("Successo", f"Il file {os.path.basename(file_path)} è stato caricato correttamente.")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore nel caricare il file: {e}")

# Funzione per aprire la finestra IA
def open_IA_window():
    # Crea una finestra separata per la sezione IA
    window_IA = tk.Toplevel()
    window_IA.title("Analisi Dati con IA")
    window_IA.geometry("600x400")

    # Aggiungiamo una label di istruzione
    label = tk.Label(window_IA, text="Inserisci la domanda per l'analisi dei dati:", font=("Arial", 14))
    label.pack(pady=20)

    # Aggiungiamo un campo di input per la domanda
    domanda_entry = tk.Entry(window_IA, font=("Arial", 12))
    domanda_entry.pack(pady=10)

    # Funzione per cercare la risposta
    def on_search():
        domanda = domanda_entry.get()  # Prendi la domanda inserita
        if domanda:
            # Chiama la funzione che analizza i dati
            risultato = analizza_dati_domanda(domanda)
            messagebox.showinfo("Risultato Analisi", risultato)  # Mostra il risultato in una finestra di info
        else:
            messagebox.showwarning("Attenzione", "Inserisci una domanda valida!")  # Se la domanda è vuota, avvisa

    # Pulsante per avviare la ricerca
    search_btn = tk.Button(window_IA, text="Cerca", command=on_search)
    search_btn.pack(pady=10)

    # Pulsante per caricare un documento
    carica_btn = tk.Button(window_IA, text="Carica Documento", command=carica_documento)
    carica_btn.pack(pady=10)

    # Avvia la finestra
    window_IA.mainloop()
