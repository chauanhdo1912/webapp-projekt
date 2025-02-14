**WanderWise** ist eine Webanwendung, mit der Benutzer Reiseerfahrungen teilen, Fotos hochladen und mit einer interaktiven Karte ihre Erlebnisse anzeigen lassen können.

## Features**

- Benutzerregistrierung und -anmeldung

- Profilerstellung mit individuellem Profilbild

- Hochladen von Reiseposts mit Bildern, Beschreibungen und Standortangaben

- Emotionale Tagging-Funktion für Posts

- Feed-Seite zur Anzeige der neuesten Posts

##Voraussetzungen:

- Python 3.x

- pip (Python-Paketmanager)

- SQLite (standardmäßig mit Python enthalten)

### Schritt 1: Repository klonen

```python
git clone https://github.com/chauanhdo1912/webapp-projekt.git
cd WanderWise
```
### Schritt 2: Virtuelle Umgebung erstellen (optional, aber empfohlen)

```python
python -m venv venv
source venv/bin/activate   # für macOS/Linux
venv\Scripts\activate      # für Windows
```
### Schritt 3: Abhängigkeiten installieren

pip install -r requirements.txt

### Schritt 4: Datenbank einrichten

flask db init  
flask db migrate -m "Initial migration"  
flask db upgrade  

### Schritt 5: Anwendung starten

flask run

Die Anwendung ist standardmäßig unter folgender Adresse erreichbar:http://127.0.0.1:5000

## Lizenz:
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/