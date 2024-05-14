import subprocess
import webbrowser
import time
import os

# Funktion zum Aktivieren der virtuellen Umgebung
def activate_virtualenv():
    activate_script = os.path.join('.venv', 'Scripts', 'python.exe')  # Pfad zur Batch-Datei zum Aktivieren der virtuellen Umgebung
    subprocess.Popen([activate_script, 'app.py'], creationflags=subprocess.CREATE_NO_WINDOW)

# Funktion zum Öffnen des Standard-Webbrowsers
def open_browser():
    time.sleep(2)  # Kurze Verzögerung, um sicherzustellen, dass der Server gestartet ist
    webbrowser.open_new_tab('http://localhost:5000')  # Hier die Adresse anpassen, falls der Port abweicht

# Hauptfunktion
def main():
    activate_virtualenv()
    open_browser()

if __name__ == "__main__":
    main()
