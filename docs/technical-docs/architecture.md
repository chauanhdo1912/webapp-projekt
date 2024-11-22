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

[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

## Cross-cutting concerns

[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]
