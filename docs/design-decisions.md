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
- Falls Skalierung erforderlich ist, können wir auf eine andere Datenbank umsteigen
*Entscheidung getroffen von:* github.com/chauanhdo1912, github.com/Yasin Cherif
### Regarded options

| Kriterium | Nur SQL Lite | SQLite + Flask-Migrate | MySQL |
| --- | --- | --- | ---- 
| **Know-how** | ✔️ Direktes Arbeiten mit SQL | ⚠️ Erfordert Kenntnisse in Flask-Migrate | ⚠️ Hat komplexeren DBMS und SQL-Dialekten
| **Schema-Änderungen** | ❌ Manuelle Anpassungen nötig | ✔️ Automatische Migrationen mit Flask-Migrate | ✔️ Bietet leistungsstarke Migrationswerkzeuge
| **Skalierbarkeit** | ❌ Nicht ideal für große Anwendungen | ✔️ Kann in begrenztem Maße skaliert werden | ✔️ Hoch skalierbar und geeignet für große Systeme
| **Change DB schema** | ❌ SQL ist fest im Code verankert | ✔️ Besser, aber nicht so flexibel wie größere DBMS | ✔️ Gut strukturiert mit ORM-Unterstützung und Tools wie Alembic (database migration)
| **Performance** | ⚠️ Gut für kleine Apps, begrenzte Parallelität | ✔️ Verbesserte Verwaltung von Änderungen | ✔️ ✔️ Bessere Leistung bei vielen gleichzeitigen Anfragen
---

## [Example, delete this section] 01: How to access the database - SQL or SQLAlchemy 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-Jun-2024

### Problem statement

Should we perform database CRUD (create, read, update, delete) operations by writing plain SQL or by using SQLAlchemy as object-relational mapper?

Our web application is written in Python with Flask and connects to an SQLite database. To complete the current project, this setup is sufficient.

We intend to scale up the application later on, since we see substantial business value in it.



Therefore, we will likely:
Therefore, we will likely:
Therefore, we will likely:

+ Change the database schema multiple times along the way, and
+ Switch to a more capable database system at some point.

### Decision

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

---
