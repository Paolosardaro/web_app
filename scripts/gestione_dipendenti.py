import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Funzione per aprire il file Excel e caricare i dati nel DataFrame
def import_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if file_path:
        try:
            # Carica il file Excel in un DataFrame
            df = pd.read_excel(file_path)

            # Visualizza i dati nella console o fai qualcosa con questi dati
            print(df.head())  # Mostra le prime righe del DataFrame per il debug

            # Messaggio di conferma
            messagebox.showinfo("Successo", "Dati importati correttamente!")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante l'importazione del file: {e}")
    else:
        messagebox.showwarning("No File", "Non è stato selezionato alcun file.")

# Funzione per tornare al menu principale
def back_to_main_window(window):
    window.destroy()  # Chiudi la finestra corrente

# Funzione per la finestra della gestione dei dipendenti
def open_window():
    # Crea la finestra
    window = tk.Toplevel()
    window.title("Gestione Dipendenti")
    window.geometry("600x400")

    # Etichetta di benvenuto
    label = tk.Label(window, text="Gestione Dipendenti", font=("Arial", 16))
    label.pack(pady=20)

    # Pulsante per importare i dati da un file Excel
    import_button = tk.Button(window, text="Importa Dati da Excel", command=import_data)
    import_button.pack(pady=10)

    # Pulsante per tornare al menu principale
    back_button = tk.Button(window, text="Torna al Menu Principale", command=lambda: back_to_main_window(window))
    back_button.pack(pady=10)

    # Avvia la finestra
    window.mainloop()
