---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Le Chau Anh Do]

{: .no_toc }
# Architecture

{: .attention }
> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.
> 
> See [this blog post](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) for an explanation of the concept and these examples:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> For structural and behavioral illustration, you might want to leverage [Mermaid](../ui-components.md), e.g., by charting common [C4](https://c4model.com/) or [UML](https://www.omg.org/spec/UML) diagrams.
> 
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

 # Post-Seite (Le Chau Anh Do)
>Funktion: Nutzer können neue Inhalte erstellen.

>Ablauf:

>Nutzer lädt ein Bild von seinem Gerät hoch.

>Nutzer fügt eine kurze Beschreibung hinzu.

>Hashtags können eingegeben werden, um den Beitrag leichter auffindbar zu machen.

>Der Standort wird auf einer Karte ausgewählt.

>Nach dem Klick auf "Posten" wird der Beitrag veröffentlicht und automatisch im Feed angezeigt.

 # Feed-Seite (Le Chau Anh Do)
>Funktion: Zeigt alle veröffentlichten Beiträge an und ermöglicht Interaktionen.

>blauf:

>Alle Beiträge, einschließlich des neuesten, werden in einem scrollbaren Feed dargestellt.

>Nutzer können Beiträge mit "Gefällt mir" markieren, Kommentare hinzufügen und sie für später speichern.

 # Profil-Seite (Yasin Cherif)
>Funktion: Speichert und zeigt persönliche Informationen sowie die vom Nutzer erstellten oder gespeicherten Beiträge an.

>Ablauf:

>Nutzer können ihr Profilbild, ihren Namen und ihre Bio sehen oder bearbeiten.

>Eine Liste aller veröffentlichten Beiträge wird angezeigt.

>Ein separater Bereich zeigt die Beiträge, die der Nutzer gespeichert hat.

 # Login-Seite (Yasin Cherif)
>Funktion: Ermöglicht die Anmeldung und Registrierung.

>Ablauf:

> - Anmelden:

>Nutzer gibt seine registrierte E-Mail-Adresse und das Passwort ein, um sich anzumelden.

> - Registrieren:
Neue Nutzer können ein Konto erstellen, indem sie ihre E-Mail-Adresse, einen Namen und ein Passwort angeben.
Nach erfolgreicher Anmeldung wird der Nutzer zur Startseite weitergeleitet.

## Codemap

## **1. Aufbau der Anwendung**

- **Framework**: Flask 
- **Datenbank**: SQLite 
- **Statische Inhalte**: Bilder, die von Nutzern hochgeladen werden, werden im Ordner `static/images` gespeichert.

### Wichtige Konfigurationen
- `SQLALCHEMY_DATABASE_URI`: Pfad zur SQLite-Datenbank.
- `UPLOAD_FOLDER`: Verzeichnis für hochgeladene Bilder.
- `ALLOWED_EXTENSIONS`: Liste der erlaubten Dateiformate (`png`, `jpg`, `jpeg`, `gif`).

---

## **2. Hauptkomponenten**

### **Routen**
1. **Startseite (`/`)**:
   - Rendert die Hauptseite (`Hauptseite.html`).

2. **Post-Seite (`/post`)**:
   - Ermöglicht Nutzern das Hochladen von Bildern, Hinzufügen von Beschreibungen und Veröffentlichen von Beiträgen.
   - Validiert Dateitypen und speichert Bilder im Upload-Ordner.
   - Fügt neue Einträge zur Datenbank hinzu.

3. **Feed-Seite (`/feed`)**:
   - Zeigt alle Beiträge der Nutzer aus der Datenbank in einer scrollbaren Ansicht.
   - Ermöglicht Interaktionen wie „Gefällt mir“, Kommentare und das Speichern von Beiträgen.

4. **Login-Seite (`/Login`)**:
   - Platzhalter für Nutzeranmeldung und Registrierung.

### **Datenbank**
- **Post-Modell**:
  - `id`: Primärschlüssel zur Identifizierung der Beiträge.
  - `image_file`: Speichert den Dateinamen des hochgeladenen Bildes.
  - `description`: Speichert die Beschreibung, die der Nutzer angegeben hat.

### **Templates**
- `Hauptseite.html`: Landing-Page.
- `Post.html`: Upload-Interface für das Erstellen neuer Beiträge.
- `Feed.html`: Zeigt eine Liste aller Beiträge.
- `Login.html`: Interface für Nutzeranmeldung.

---

## **3. Hilfsfunktionen**

1. **Datei-Validierung**:
   - Funktion: `allowed_file(filename)`
   - Stellt sicher, dass hochgeladene Dateien den erlaubten Formaten entsprechen.

2. **Datenbankinitialisierung**:
   - `db.create_all()` wird verwendet, um das Datenbankschema zu initialisieren.

---

### **4. Ablauf der Anwendung**

1. **Startseite**: Nutzer landen auf der Hauptseite und navigieren zu anderen Funktionen.
2. **Post-Erstellung**: Nutzer laden Bilder hoch, geben Beschreibungen ein und veröffentlichen Beiträge.
3. **Feed-Anzeige**: Nutzer sehen ihre Beiträge zusammen mit anderen Beiträgen.
4. **Login**: Platzhalter für zukünftige Authentifizierungsfunktionen.


## Cross-cutting concerns

## **1. Datei- und Medienmanagement**

- **Funktionalität**:
  - Validiert hochgeladene Dateien basierend auf erlaubten Dateiformaten (`png`, `jpg`, etc.).
  - Speichert hochgeladene Bilder im Verzeichnis `static/images`.
- **Risiken**:
  - Große Dateien können die Leistung der Anwendung beeinträchtigen.
  - Nicht bereinigte Dateinamen könnten Sicherheitsrisiken darstellen.
- **Empfehlungen**:
  - Die Dateigröße begrenzen.
  - Dateien in eindeutige Bezeichner umbenennen, um Konflikte und Sicherheitsprobleme zu vermeiden.
  - Cloud-Speicher (z. B. AWS S3) für bessere Skalierbarkeit nutzen.

---

## **2. Datenbankkonsistenz**

- **Integrität**:
  - Das `Post`-Modell erzwingt erforderliche Felder (`nullable=False`).
  - SQLAlchemy stellt sicher, dass Transaktionen atomar sind.
- **Skalierbarkeit**:
  - SQLite eignet sich für kleine Anwendungen, könnte jedoch unter starker Last zum Engpass werden.
  - Wechseln Sie zu PostgreSQL für bessere Leistung in produktiven Umgebungen.

---

## **3. Sicherheit**

- **Dateisicherheit**:
  - Validieren und bereinigen Sie alle hochgeladenen Dateien.
  - Beschränken Sie den direkten Zugriff auf hochgeladene Dateien über Flask's `send_from_directory`.
- **Datensicherheit**:
  - Aktuell gibt es keine Nutzer-Authentifizierung. Fügen Sie eine sichere Anmeldung mit gehashten Passwörtern hinzu (z. B. mit `bcrypt` oder `Flask-Login`).

---

## **4. Skalierbarkeit und Leistung**

- **Aktuelle Einschränkungen**:
  - Die Leistung von SQLite nimmt bei gleichzeitigen Schreibvorgängen ab.
  - Die lokale Speicherung von Medien kann schnell zum Engpass werden.

---

## **5. Template-Rendering**

- Templates rendern Inhalte dynamisch mit Jinja2.
- Wiederverwendbare Komponenten (z. B. Header, Footer) vereinfachen das Design.
- Zukünftige Verbesserungen könnten Teil-Templates für Beiträge beinhalten, um die Rendering-Logik des Feeds zu optimieren.

---

## **6. Fehlerbehandlung**

- **Aktueller Stand**:
  - Grundlegende Überprüfungen auf fehlende Dateien beim Upload.

---

## **7. Design-Entscheidungen**

 - **Routenorganisation**:
   - Alle Routen befinden sich derzeit in einer einzigen Datei zur Vereinfachung.
   .

