import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()
# Überprüfen ob die Verbindung zur Datenbank besteht:
try:
    conn = sqlite3.connect('database.db')
    print("Database connection established successfully.")
except sqlite3.Error as e:
    print("Error opening database connection:", e)

# Tabellennamen abrufen
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Durch jede Tabelle iterieren und eine Spalte hinzufügen
for table in tables:
    table_name = table[0]
    try:
        # SQL-Befehl zum Hinzufügen einer Spalte zur aktuellen Tabelle
        alter_sql = f"ALTER TABLE '{table_name}' ADD COLUMN Deleted Real"
        # SQL-Befehl ausführen
        cursor.execute(alter_sql)
        # Änderungen in der Datenbank bestätigen
        conn.commit()
        print(f"Added column to table {table_name}.")
    except sqlite3.Error as e:
        print(f"Error adding column to table {table_name}: {e}")

# Verbindung zur Datenbank schließen
conn.close()
