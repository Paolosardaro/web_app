import os
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

# Funzione per verificare la presenza dei documenti necessari
def verifica_documenti_compliance(nome, inquadramento, periodo=None):
    folder = "allegati"
    documenti_richiesti_in_sede = ["ODS", "TS", "Rapportino"]
    documenti_richiesti_fuorisede = ["ODS", "TS", "Rapportino", "Foglio Missione", "Fatture"]
    
    if inquadramento == "In sede":
        documenti_richiesti = documenti_richiesti_in_sede
    elif inquadramento == "Fuorisede":
        documenti_richiesti = documenti_richiesti_fuorisede
    else:
        return "Inquadramento non valido."
    
    documenti_trovati = []
    documenti_mancanti = []
    
    # Verifica i documenti nella cartella allegati
    if not os.path.exists(folder):
        return "⚠️ La cartella 'allegati' non esiste."
    
    for file in os.listdir(folder):
        if file.startswith(nome):  # Verifica che il documento appartenga al dipendente
            if any(doc in file for doc in documenti_richiesti):
                documenti_trovati.append(file)
            else:
                documenti_mancanti.extend([doc for doc in documenti_richiesti if doc not in file])

    # Aggiungi documenti mancanti
    for doc in documenti_richiesti:
        if not any(doc in file for file in documenti_trovati):
            documenti_mancanti.append(doc)
    
    if not documenti_trovati:
        documenti_trovati = "Nessun documento trovato."

    if not documenti_mancanti:
        documenti_mancanti = "Tutti i documenti sono presenti."
    
    return documenti_trovati, documenti_mancanti

# Funzione per aprire la finestra di gestione compliance
def open_compliance_window():
    # Crea una finestra separata per la sezione compliance
    window_compliance = tk.Toplevel()
    window_compliance.title("Compliance Dipendente")
    window_compliance.geometry("600x400")
    
    # Etichetta per titolo
    label = tk.Label(window_compliance, text="Verifica Documenti Dipendente", font=("Arial", 14))
    label.pack(pady=20)
    
    # Nome dipendente
    label_nome = tk.Label(window_compliance, text="Nome Dipendente:", font=("Arial", 12))
    label_nome.pack(pady=5)
    entry_nome = tk.Entry(window_compliance, font=("Arial", 12))
    entry_nome.pack(pady=5)
    
    # Inquadramento
    label_inquadramento = tk.Label(window_compliance, text="Inquadramento (In sede/Fuorisede):", font=("Arial", 12))
    label_inquadramento.pack(pady=5)
    entry_inquadramento = tk.Entry(window_compliance, font=("Arial", 12))
    entry_inquadramento.pack(pady=5)
    
    # Periodo
    label_periodo = tk.Label(window_compliance, text="Periodo (opzionale):", font=("Arial", 12))
    label_periodo.pack(pady=5)
    entry_periodo = tk.Entry(window_compliance, font=("Arial", 12))
    entry_periodo.pack(pady=5)
    
    # Funzione per avviare la verifica dei documenti
    def verifica_compliance():
        nome = entry_nome.get()
        inquadramento = entry_inquadramento.get()
        periodo = entry_periodo.get() if entry_periodo.get() else None
        
        if not nome or not inquadramento:
            messagebox.showwarning("Attenzione", "Compila tutti i campi obbligatori!")
            return
        
        documenti_trovati, documenti_mancanti = verifica_documenti_compliance(nome, inquadramento, periodo)
        
        # Mostra il risultato
        result_text = f"Documenti trovati: {documenti_trovati}\n\nDocumenti mancanti: {documenti_mancanti}"
        messagebox.showinfo("Risultato Verifica", result_text)

    # Pulsante per avviare la verifica
    btn_verifica = tk.Button(window_compliance, text="Verifica Documenti", command=verifica_compliance)
    btn_verifica.pack(pady=20)
    
    window_compliance.mainloop()
