from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
#selected_table_name= None #globale Variable

# #Überprüfen ob die Verbindung zur Datenbank besteht:
# try:
#     conn = sqlite3.connect('database.db')
#     print("Database connection established successfully.")
# except sqlite3.Error as e:
#     print("Error opening database connection:", e)

@app.route('/')
def index():
    # Weiterleitung zur Seite "view_inventory"
    return redirect(url_for('view_inventory'))

@app.route('/view_inventory.html', methods=['GET','POST'])
def view_inventory():
    # Holen Sie sich die Liste der Tabellennamen
    table_names_list = get_table_names_list()   
    inventory = get_all_inventory()
    #print("Table names list:", table_names_list)  # Debugging-Ausgabe   
    return render_template('view_inventory.html', table_names_list=table_names_list, inventory=inventory)

@app.route('/update_inventory_table', methods=['GET'])
def update_inventory_table():
    selected_table_name = request.args.get('table_name')
    if selected_table_name is None or selected_table_name == '':
        inventory = get_all_inventory()
    else:
        inventory = get_inventory(selected_table_name)
    print("Selected table name:", selected_table_name)  # Debugging-Ausgabe
    return render_template('inventory_table.html', inventory=inventory, selected_table_name=selected_table_name)



def get_inventory(table_name):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{table_name}'")
    items = cursor.fetchall()
    conn.close()
    return items

def get_all_inventory():
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    # Liste zum Speichern aller Datensätze aus allen Tabellen
    all_inventory = []
    # Alle Tabellennamen abrufen
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # Daten aus jeder Tabelle abrufen und zur Liste hinzufügen
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM [{table_name}]")
        inventory = cursor.fetchall()
        all_inventory.extend(inventory)
    # Verbindung schließen
    conn.close()
    return all_inventory



@app.route('/add_product.html', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Daten aus dem Formular abrufen
        selected_table_name = request.form.get('table_name')
        print(selected_table_name)
        p_id = generate_p_id(selected_table_name)
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        unit_price = request.form.get('unit_price')
        size = request.form.get('size')
        wbw = request.form.get('WbW')
        
        
        # Überprüfen, ob alle Daten vorhanden sind
        if not p_id or not name or not quantity or not unit_price or not size or not wbw:
            return 'Missing data. Please fill out all fields.'
        
        message= False
        
        try:
            # SQL-Befehl zum Einfügen eines neuen Produkts
            insert_sql = "INSERT INTO '{}' (p_id, name, quantity, unit_price, size, WbW) VALUES (?, ?, ?, ?, ?, ?)".format(selected_table_name)
            
            # Parameter für den SQL-Befehl
            params = (p_id, name, quantity, unit_price, size, wbw)
            
            # SQL-Befehl ausführen
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute(insert_sql, params)
            
            # Änderungen in der Datenbank bestätigen
            conn.commit()
            
            # Verbindung zur Datenbank schließen
            conn.close()

            # Zurück zur (aktuellen Seite) umleiten
            return redirect(url_for('add_product', message=True))
        except Exception as e:
            # Fehlermeldung ausgeben, wenn ein Fehler auftritt
            return f'An error occurred: {str(e)}'
    else:
        # GET-Anforderung: Tabellennamen abrufen und Formular rendern
        table_names_list = get_table_names_list()
        selected_table_name = request.args.get('table_name')  # Ausgewählten Tabellennamen abrufen
        p_id = "Wähl eine Kategorie aus!"  # p_id initialisieren
        if selected_table_name:
            p_id = generate_p_id(selected_table_name)
        message=request.args.get('message')
        print(message)
        return render_template('add_product.html', table_names_list=table_names_list, p_id=p_id, selected_table_name=selected_table_name, message=message)

    
@app.route('/generate_p_id')
def get_generated_p_id():
    table_name = request.args.get('table_name')
    p_id = generate_p_id(table_name)
    print(request)
    return str(p_id)


def generate_p_id(table_name):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Extrahiere die ersten zwei Ziffern des Tabellennamens
    print(table_name)
    prefix = ''.join(filter(str.isdigit, table_name))[:2]
    
    # Zähle die Anzahl der vorhandenen Produkte in der Tabelle
    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")  # Backticks um den Tabellennamen
    count = cursor.fetchone()[0]
    
    # Generiere die P_ID basierend auf dem Muster
    p_id = int(prefix) * 100 + count + 1
    
    conn.close()
    
    return p_id


@app.route('/create_offer.html')
def create_offer():
    return render_template('create_offer.html')

def get_table_names_list():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_product_%' Order by name")
    table_names_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    return table_names_list

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000 ,debug=True)
