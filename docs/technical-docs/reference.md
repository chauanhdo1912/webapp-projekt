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

## **Post Handling**
### **Function:** `post()`
**Route:** `/post`

**Methods:** `GET`, `POST`

**Purpose:**  
- **POST:** Ermöglicht das Hochladen eines neuen Beitrags. Nutzer können ein Bild hochladen, eine Beschreibung hinzufügen, Hashtags angeben und einen Standort auswählen. Der Beitrag wird in der Datenbank gespeichert und im Feed angezeigt.
- **GET:** Zeigt die Eingabemaske für das Hochladen eines neuen Beitrags an.

**Sample output:**  
- **POST:**  
  Der Beitrag wird erfolgreich gespeichert und Nutzer wird zum Feed weitergeleitet.  
  ```json
  {
      "message": "Post created successfully!",
      "post_id": 5
  }
