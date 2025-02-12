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

Das Post-Modell speichert alle wesentlichen Informationen zu einem Beitrag, einschließlich Bilddatei, Beschreibung, Emotionen und Standortinformationen.

### **Tabellenstruktur**

| **Feld**        | **Typ**         | **Beschreibung**                             | **Einschränkungen**           |
|------------------|-----------------|---------------------------------------------|--------------------------------|
| `id`            | Integer         | Eindeutige Identifikation des Beitrags.     | Primärschlüssel, Auto-Inkrement |
| `image_file`    | String (120)    | Dateiname des hochgeladenen Bildes.         | Nicht null                   |
| `description`   | String (500)    | Beschreibung oder Text des Beitrags.        | Nicht null                   |
| `emotion`       | String (500)    | Emotionale Beschreibung des Moments.        | Nicht null                   |
| `latitude`      | Float           | Breitengrad des Standorts.                  | Kann null sein               |
| `longitude`     | Float           | Längengrad des Standorts.                   | Kann null sein               |

### **SQLAlchemy-Definition für das Post-Modell**

```json
{
  "cell_type": "code",
  "execution_count": null,
  "metadata": {},
  "outputs": [],
  "source": [
    "print(\"Hello, World\")\n"
  ]
}


## **3. Nutzer-Modell (zukünftige Implementierung)**

Ein zukünftiges Update könnte ein **User-Modell** einführen, um Nutzerkonten zu verwalten. Dieses Modell könnte folgendermaßen strukturiert sein:

| **Feldname**       | **Datentyp**        | **Beschreibung**                                   | **Einschränkungen**               |
|--------------------|---------------------|--------------------------------------------------|------------------------------------|
| `id`              | Integer             | Eindeutige ID des Nutzers.                        | Primärschlüssel, Auto-Inkrement    |
| `username`        | String (80)         | Benutzername des Nutzers.                         | Nicht null, einzigartig           |
| `email`           | String (120)        | E-Mail-Adresse des Nutzers.                       | Nicht null, einzigartig           |
| `password_hash`   | String (128)        | Gehashte Version des Passworts zur Sicherheit.    | Nicht null                        |
