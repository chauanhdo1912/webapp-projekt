---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Le Chau Anh Do]

{: .no_toc }
# Data model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## **Table of Contents**

1. **Überblick**
2. **Post-Modell**
3. **Nutzer-Modell (zukünftige Implementierung)**

---

## **1. Überblick**

Die Anwendung verwendet SQLite als Datenbank mit SQLAlchemy als ORM (Object Relational Mapper). Das derzeit implementierte Modell speichert Informationen über Beiträge (Posts) und Benutzer (User). Die Datenbankstruktur ist modular aufgebaut und kann erweitert werden, um zusätzliche Funktionen wie Nutzerkonten oder Interaktionen zu unterstützen.

---

## **2. Post-Modell**

Das **Post-Modell** speichert alle wesentlichen Informationen zu einem Beitrag, einschließlich Bilddatei, Beschreibung, Emotionen und Standortinformationen.

### **Tabellenstruktur**

| **Feld**        | **Typ**         | **Beschreibung**                             | **Einschränkungen**           |
|------------------|-----------------|---------------------------------------------|--------------------------------|
| `id`            | Integer         | Eindeutige Identifikation des Beitrags     | Primärschlüssel, Auto-Inkrement |
| `image_file`    | String (120)    | Dateiname des hochgeladenen Bildes         | Nicht null                   |
| `description`   | String (500)    | Beschreibung oder Text des Beitrags        | Nicht null                   |
| `emotion`       | String (500)    | Emotionale Beschreibung des Moments        | Nicht null                   |
| `latitude`      | Float           | Breitengrad des Standorts                  | Kann null sein               |
| `longitude`     | Float           | Längengrad des Standorts                   | Kann null sein               |

### **SQLAlchemy-Definition für das Post-Modell**

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    emotion = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=True)  
    longitude = db.Column(db.Float, nullable=True) 
    ...
    new_post = Post(image_file=filename, description=description, emotion=emotion, latitude=latitude, longitude=longitude)

``` 


## **3. Nutzer-Modell**

Das **User-Modell** verwaltet die Benutzerkonten und speichert persönliche Informationen, einschließlich Benutzername, Passwort, Geschlecht, Alter und Profilbild.

| **Feldname**       | **Datentyp**        | **Beschreibung**                                   | **Einschränkungen**               |
|--------------------|---------------------|--------------------------------------------------|------------------------------------|
| `id`              | Integer             | Eindeutige ID des Nutzers                      | Primärschlüssel, Auto-Inkrement      |
| `username`        | String (150)        | Eindeutiger Benutzername                        | Nicht null, einzigartig         |
| `password`        | String (150)        | Passwort des Nutzers (verschlüsselt gespeichert)  | Nicht null         |
| `gender`          | String (50)         | Geschlecht des Nutzers                          | Optional                    |
| `age`             | Integer             | Alter des Nutzers                            | Optional        |
| `email`           | String (150)        | E-Mail-Adresse des Nutzers                         | Optional                    |
| `profile_picture` | String (150)         | Profilbild des Nutzers                  | Standardwert: DEFAULT_PROFILE_PICTURE                   |
| `is_profile_complete` | Boolean             | Gibt an, ob das Profil vollständig ist   | Standardwert: False        |

### **SQLAlchemy-Definition für das User-Modell**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(150))
    profile_picture = db.Column(db.String(150), default=DEFAULT_PROFILE_PICTURE)
    is_profile_complete = db.Column(db.Boolean, default=False)
    ...
    new_user = User(username=username, password=hashed_password, profile_picture=DEFAULT_PROFILE_PICTURE)

``` 

Relation zwischen User und Post-Modell