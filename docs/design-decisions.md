---
title: Design Decisions
nav_order: 3
---

{: .label }
[Le Chau Anh Do]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: Datenbank - SQLite und Migration

### Meta

Status
: Work in progress - **Decided**

Updated
: 10-Jan-2025

### Problem statement

Unsere Anwendung verwendet eine SQLite-Datenbank für die Speicherung von Benutzern und Beiträgen. SQLite ist eine einfache und leichtgewichtige Lösung, aber es gibt Herausforderungen:
- Wir müssen Datenbankänderungen verwalten, wenn sich das Schema ändert.
- Möglicherweise müssen wir in Zukunft auf ein leistungsfähigeres Datenbankmanagementsystem (DBMS) umsteigen.

### Decision

Wir haben uns für SQLite mit Flask-Migrate entschieden, um Datenbankmigrationen effizient zu verwalten:
- SQLite bleibt als primäre Datenbank bestehen, solange die Anwendung klein ist
- Flask-Migrate wird genutzt, um Schemaänderungen zu verwalten
- Falls Skalierung erforderlich ist, können wir auf eine andere Datenbank umsteigen <br>
*Entscheidung getroffen von:* github.com/chauanhdo1912, github.com/Yasin Cherif

### Regarded options:

Wir haben drei Alternativen betrachtet:

+ SQL Lite
+ SQLite + Flask-Migrate
+ MySQL

| Kriterium            | Nur SQL Lite                          | SQLite + Flask-Migrate                     | MySQL                                      |
|----------------------|------------------------------------|-------------------------------------------|-------------------------------------------|
| **Know-how**        | ✔️ Direktes Arbeiten mit SQL       | ⚠️ Erfordert Kenntnisse in Flask-Migrate | ⚠️ Hat komplexeren DBMS und SQL-Dialekten |
| **Schema-Änderungen** | ❌ Manuelle Anpassungen nötig     | ✔️ Automatische Migrationen mit Flask-Migrate | ✔️ Bietet leistungsstarke Migrationswerkzeuge |
| **Skalierbarkeit**  | ❌ Nicht ideal für große Anwendungen | ✔️ Kann in begrenztem Maße skaliert werden | ✔️ Hoch skalierbar und geeignet für große Systeme |
| **Change DB schema** | ❌ SQL ist fest im Code verankert  | ✔️ Besser, aber nicht so flexibel wie größere DBMS | ✔️ Gut strukturiert mit ORM-Unterstützung und Tools wie Alembic (database migration) |
| **Performance**      | ⚠️ Gut für kleine Apps, begrenzte Parallelität | ✔️ Verbesserte Verwaltung von Änderungen | ✔️ Bessere Leistung bei vielen gleichzeitigen Anfragen |

---

## 02: Formularverarbeitung und Feed-Anzeige

### Meta

Status
: Work in progress - **Decided**

Updated
: 14-Jan-2025

### Problem statement

Benutzer sollen Beiträge über ein HTML-Formular hochladen können, die dann im Feed angezeigt werden. Die Herausforderungen:
+ Wie verarbeiten wir Formulardaten sicher in Flask?
+ Wie speichern wir Bilder und Text korrekt in der Datenbank?
+ Wie werden die Daten im Feed effizient geladen?

### Decision

+ Formularverarbeitung: Flask empfängt Daten mit request.form (Text) und request.files (Bilder)
+ Speicherung: Bilder werden auf dem Server gespeichert, Metadaten in der Post-Tabelle
+ Feed-Anzeige: Beiträge werden per Post.query.order_by(Post.id.desc()).all() geladen <br>

Entscheidung getroffen von: github.com/chauanhdo1912 

### Regarded options:

Wir haben zwei Alternativen analysiert:

| Kriterium            | Direkte Speicherung in der Datenbank | Speicherung als Datei mit Referenz in der Datenbank |
|----------------------|-----------------------------------|-------------------------------------------------|
| **Leicht zu implementieren** | ❌ Schwer (große Binärdateien) | ✔️ Einfach (nur Dateipfad speichern) |
| **Leistung**          | ❌ Langsam (hoher Speicherverbrauch) | ✔️ Schnell (Dateien direkt im Server abrufen) |
| **Skalierbarkeit**    | ❌ Nicht effizient für viele Bilder | ✔️ Skalierbar mit CDN oder Cloud-Speicher |

### Implementierungsdetails:

#### 1. Verarbeitung der Formularübermittlung

+ Das HTML-Formular verwendet die POST-Methode und multipart/form-data für den Datei-Upload
+ Das Flask-Backend verarbeitet die Formulardaten mit request.form (Textfelder) und request.files (Bilddatei)
+ Das Bild wird in static/uploads/ mit einem eindeutigen Dateinamen gespeichert
+ Der Dateipfad wird in der Datenbank gespeichert

```python
@app.route('/Post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        file = request.files.get('file')
        description = request.form.get('description')
        emotion = request.form.get('emotion')
        latitude = request.form.get('latitude')  
        longitude = request.form.get('longitude')

        if latitude == '':
            latitude = None
        if longitude == '':
            longitude = None

        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_post = Post(image_file=filename, description=description, emotion=emotion, latitude=latitude, longitude=longitude)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('feed'))

    return render_template('Post.html')
```
#### 2. Anzeige der Beiträge im Feed
Die Datenbank wird nach allen Beiträgen abgefragt, geordnet nach Zeitstempel. Jinja2 durchläuft die Beiträge und rendert dynamisch das Bild und die Beschreibung.

```python
@app.route('/Feed')
def feed():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('Feed.html', posts=posts)
```

```python
{% for post in posts %}
                    <div class="post">
                        <!-- Zeigt das hochgeladene Bild -->
                        <img src="{{ url_for('static', filename='images/' + post.image_file) }}" alt="Travel Photo" width="300"><br>
                        
                        <!-- Beschreibung des Beitrags -->
                        <p>{{ post.description }}</p>
                        
                        <!-- Emotion des Beitrags -->
                        <p><strong>Emotion:</strong>
                            {% if post.emotion == 'Happy' %}
                                😊 Happy
                            {% elif post.emotion == 'Adventurous' %}
                                🌍 Adventurous
                            {% elif post.emotion == 'Joyful' %}
                                ❤️ Joyful
                            {% endif %}
                        </p>
```
---
