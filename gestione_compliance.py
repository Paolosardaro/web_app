import os

def verifica_documenti_compliance(nome, inquadramento, periodo=None):
    folder = "allegati"
    documenti_richiesti_in_sede = ["ODS", "TS", "Rapportino"]
    documenti_richiesti_fuorisede = ["ODS", "TS", "Rapportino", "Foglio Missione", "Fatture"]
    
    if inquadramento == "In sede":
        documenti_richiesti = documenti_richiesti_in_sede
    elif inquadramento == "Fuorisede":
        documenti_richiesti = documenti_richiesti_fuorisede
    else:
        return [], []  # Inquadramento non valido

    documenti_trovati = []
    documenti_mancanti = []

    if not os.path.exists(folder):
        return [], documenti_richiesti  # Nessuna cartella = tutti mancanti

    for file in os.listdir(folder):
        if file.startswith(nome):
            for doc in documenti_richiesti:
                if doc in file and doc not in documenti_trovati:
                    documenti_trovati.append(doc)

    for doc in documenti_richiesti:
        if doc not in documenti_trovati:
            documenti_mancanti.append(doc)

    return documenti_trovati, documenti_mancanti
