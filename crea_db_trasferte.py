import sqlite3

conn = sqlite3.connect("gestione_trasferte.db")
c = conn.cursor()

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

conn.commit()
conn.close()
