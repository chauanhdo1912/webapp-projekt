---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Le Chau Anh Do]

{: .no_toc }
# Reference documentation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# **Table of Contents**

---

## **Überblick über die Daten in der Anwendung** ##

Die Anwendung hat zwei Haupttabellen in der SQLite-Datenbank:

- **User:** Enthält Benutzerinformationen wie username, password, email, profile_picture usw.

- **Post:** Enthält Beiträge mit Informationen zu image_file, description, emotion, latitude, longitude

Diese Daten werden in der SQLite-Datenbank (users.db) gespeichert, und Flask SQLAlchemy hilft bei der Verwaltung

Die Daten in der Anwendung funktioniert, indem: 

- Benutzer sendet Informationen über ein HTML-Formular

- Flask verarbeitet die Daten mit request.form oder request.files

- Die Daten werden mit SQLAlchemy in der Datenbank gespeichert

- Wenn Benutzer Seiten wie Feed aufrufen, fragt Flask die Datenbank ab und zeigt die Inhalte in der Benutzeroberfläche an

## **API-Endpunkte** ##

### **Benutzerverwaltung** ###

## 1. Anmeldung (/Login) ##

Methode: GET, POST

GET: Zeigt das Anmeldeformular an

POST: Erhält username und password, prüft die Datenbank und erstellt eine Session, wenn die Anmeldeinformationen korrekt sind

Datenquelle: request.form aus dem HTML-Formular

Datenspeicherung: Benutzer-Session wird gespeichert

### 2. Registrierung (/Registrieren) ###

Methode: GET, POST

GET: Zeigt das Registrierungsformular an

POST: Erhält Registrierungsdaten, verschlüsselt das Passwort und speichert die Daten in der Datenbank

Datenquelle: request.form

Datenspeicherung: Tabelle User in der Datenbank

3. Benutzerprofil (/Profil)

Methode: GET, POST

GET: Zeigt Benutzerinformationen aus der Datenbank an

POST: Aktualisiert persönliche Informationen und Profilbild

Datenquelle: request.form, request.files

Datenspeicherung: Aktualisierung der User-Tabelle

4. Abmeldung (/Logout)

Methode: GET

Funktion: Löscht die Benutzer-Session

5. Profilbild löschen (/Profil/Löschen)

Methode: POST

Funktion: Löscht das aktuelle Profilbild und setzt das Standardbild zurück

Datenspeicherung: Aktualisierung von profile_picture in der User-Tabelle

### **Beitragsverwaltung** ###

1. Beitrag erstellen (/Post)##

Methode: GET, POST

GET: Zeigt das Formular zum Erstellen eines Beitrags an

POST: Erhält Daten aus dem Formular (file, description, emotion, latitude, longitude) und speichert sie in der Datenbank

Datenquelle: request.form, request.files

Datenspeicherung: Tabelle Post in der Datenbank

2. Beiträge anzeigen (/Feed)

Methode: GET

Funktion: Ruft alle Beiträge aus der Post-Tabelle ab, sortiert sie nach ID (neueste zuerst) und zeigt sie in der Benutzeroberfläche an

Datenquelle: Datenbankabfrage (Post.query.all())

## **Verbindung zwischen Post und Feed** ##

Wenn ein Benutzer über /Post einen Beitrag erstellt, werden die Daten aus dem HTML-Formular gesendet und in der Post-Tabelle gespeichert

Wenn der Benutzer /Feed aufruft, ruft Flask alle Beiträge aus der Post-Tabelle ab und zeigt sie im Feed an

Benutzer können alle Beiträge im Feed anzeigen, einschließlich Bilder, Beschreibung, Emotionen und Standortinformationen

