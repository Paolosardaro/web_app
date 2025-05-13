import pandas as pd

# Funzione che gestisce i dati dei dipendenti
def gestione_dipendenti_function():
    try:
        # Esempio di percorso file Excel
        file_path = 'path_to_your_file.xlsx'  # Sostituisci con il percorso reale del file

        # Carica il file Excel in un DataFrame
        df = pd.read_excel(file_path)

        # Esegui operazioni sui dati: ad esempio, analizzare lo stato dei dipendenti
        num_dipendenti = len(df)  # Conta il numero totale di dipendenti
        dipendenti_attivi = df[df['Stato'] == 'Attivo']  # Filtra i dipendenti attivi
        
        # A titolo di esempio, calcoliamo il numero di dipendenti attivi
        num_dipendenti_attivi = len(dipendenti_attivi)

        # Puoi restituire un risultato significativo da visualizzare nella web app
        result = {
            'total_dipendenti': num_dipendenti,
            'dipendenti_attivi': num_dipendenti_attivi
        }

        # Restituisce il risultato come dizionario
        return result
    
    except Exception as e:
        # Se si verifica un errore, restituisce un messaggio di errore
        return {"error": f"Si è verificato un errore durante l'elaborazione dei dipendenti: {str(e)}"}
