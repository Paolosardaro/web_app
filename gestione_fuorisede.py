import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
import PyPDF2
from PIL import Image
import zipfile

# Funzione per la sezione Gestione Trasferte
def gestione_trasferte():
    window = tk.Toplevel()
    window.title("Gestione Trasferte")
    window.geometry("600x400")

    def importa_dati():
        file_path = filedialog.askopenfilename(title="Seleziona un file Excel", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                trasferte_df = pd.read_excel(file_path)
                messagebox.showinfo("Successo", f"Dati importati da {file_path}")
                # Logica per mostrare o elaborare i dati può essere aggiunta qui
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'importazione: {e}")

    def ricerca_dati():
        search_query = search_entry.get()
        if search_query:
            # Logica di ricerca da implementare
            pass

    def aggiungi_record():
        # Aggiunta record manuale placeholder
        pass

    search_label = tk.Label(window, text="Cerca Trasferte:")
    search_label.pack(pady=10)

    search_entry = tk.Entry(window)
    search_entry.pack(pady=5)

    search_button = tk.Button(window, text="Ricerca", command=ricerca_dati)
    search_button.pack(pady=10)

    import_button = tk.Button(window, text="Importa Dati Excel", command=importa_dati)
    import_button.pack(pady=10)

    add_button = tk.Button(window, text="Aggiungi Record", command=aggiungi_record)
    add_button.pack(pady=10)


# Funzione per la sezione Gestione Fatture
def gestione_fatture(percorso_allegati=None):
    window = tk.Toplevel()
    window.title("Gestione Fatture")
    window.geometry("600x400")

    def importa_pdf():
        file_path = filedialog.askopenfilename(title="Seleziona un PDF", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                messagebox.showinfo("Successo", f"PDF importato da {file_path}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'importazione del PDF: {e}")

    def unisci_pdf():
        files = filedialog.askopenfilenames(title="Seleziona PDF da unire", filetypes=[("PDF Files", "*.pdf")])
        if files:
            output = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            try:
                pdf_writer = PyPDF2.PdfWriter()
                for file in files:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page])
                with open(output, 'wb') as f_out:
                    pdf_writer.write(f_out)
                messagebox.showinfo("Successo", f"PDF uniti in {output}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'unione dei PDF: {e}")

    def importa_foto():
        file_path = filedialog.askopenfilename(title="Seleziona una Foto", filetypes=[("Image Files", "*.jpg;*.png")])
        if file_path:
            try:
                img = Image.open(file_path)
                img.show()
                messagebox.showinfo("Successo", f"Immagine importata da {file_path}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'importazione immagine: {e}")

    def importa_zip():
        zip_path = filedialog.askopenfilename(title="Seleziona un file ZIP", filetypes=[("ZIP Files", "*.zip")])
        if zip_path:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    extract_folder = filedialog.askdirectory(title="Seleziona cartella destinazione")
                    zip_ref.extractall(extract_folder)
                messagebox.showinfo("Successo", f"File ZIP estratti in {extract_folder}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'estrazione: {e}")

    def importa_da_cartella_allegati():
        if percorso_allegati and os.path.isdir(percorso_allegati):
            pdf_files = [f for f in os.listdir(percorso_allegati) if f.lower().endswith('.pdf')]
            if pdf_files:
                for file in pdf_files:
                    full_path = os.path.join(percorso_allegati, file)
                    messagebox.showinfo("Importato", f"PDF trovato: {full_path}")
            else:
                messagebox.showwarning("Nessun PDF", "Nessun file PDF trovato nella cartella allegati.")

    tk.Label(window, text="Gestione Fatture", font=("Arial", 16)).pack(pady=10)

    if percorso_allegati:
        importa_da_cartella_allegati()

    tk.Button(window, text="Importa PDF Manuale", command=importa_pdf).pack(pady=5)
    tk.Button(window, text="Unisci PDF", command=unisci_pdf).pack(pady=5)
    tk.Button(window, text="Importa Foto", command=importa_foto).pack(pady=5)
    tk.Button(window, text="Importa ZIP", command=importa_zip).pack(pady=5)


# Funzione per la sezione Dati Incrociati
def dati_incrociati():
    window = tk.Toplevel()
    window.title("Dati Incrociati")
    window.geometry("600x400")
    tk.Label(window, text="Dati Incrociati", font=("Arial", 16)).pack(pady=20)


# Funzione per aprire la finestra principale
def open_window():
    window = tk.Toplevel()
    window.title("Gestione Fuorisede")
    window.geometry("600x400")

    tk.Label(window, text="Gestione Fuorisede", font=("Arial", 16)).pack(pady=20)

    tk.Button(window, text="Gestione Trasferte", command=gestione_trasferte).pack(pady=10)
    tk.Button(window, text="Gestione Fatture", command=lambda: gestione_fatture()).pack(pady=10)
    tk.Button(window, text="Dati Incrociati", command=dati_incrociati).pack(pady=10)

    window.mainloop()
