# Documentatie: Todo Agent

De **Todo Agent** is gespecialiseerd in het scannen van diverse documenten om specifieke taken, actiepunten en "to-do" items te identificeren. Het doel is om verspreide informatie te consolideren in zowel een overzichtelijk individueel rapport als een centrale verzamelbak (master-lijst).

## 1. Doelstelling
*   **Identificatie:** Het herkennen van expliciete en impliciete taken in ongestructureerde tekst.
*   **Consolidatie:** Het verzamelen van actiepunten uit verschillende bronnen naar één centrale plek.
*   **Overzicht:** Het bieden van een snelle analyse van de brontekst gekoppeld aan een duidelijke takenlijst.

## 2. Prompt Logica
De agent hanteert de instructies uit `todo.json` met de volgende logica:
1.  **Extractie:** Scannen op trefwoorden zoals "moet", "actie", "todo", "taak" of specifieke werkwoordsvormen die duiden op een opdracht.
2.  **Analytische Samenvatting:** Het genereren van een korte context (analyse) zodat de gebruiker weet waar de taken vandaan komen.
3.  **Database Integratie:** Het voorbereiden van een `database_file` object dat specifiek is ingericht voor de centrale verzamelbak (`todo_master_list.jsonl`).
4.  **Validatie:** Strikte outputcontrole om te garanderen dat de lijst met todos altijd een array van strings is.

## 3. JSON Output Schema
De agent levert data aan volgens dit schema:
*   `analyse`: Een korte samenvatting van de brontekst.
*   `todos`: Een lijst met objecten bevattende `taak` en `prioriteit`.
*   `database_file`: Gegevens voor de master-lijst (datum, bronvermelding en items).

## 4. Configuratie
De operationele parameters voor de Todo Agent:

```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input/todos",
  "output_directory": "data/output/todos",
  "done_directory": "data/done/todos",
  "collection_file_path": "data/output/todos/master/todo_master_list.jsonl"
}
```

---

## 5. Voorbeeld Invoer (Ruwe Tekst)
Invoer die deze agent effectief kan verwerken:

```text
Memo: Voorbereiding Kwartaalcijfers
We moeten de presentatie voor de stakeholders uiterlijk vrijdag af hebben. 
Sophie, kan jij de grafieken van de omzet trekken? 
Vergeet niet dat de audit-resultaten ook nog in de bijlage moeten. 
Mark gaat over de tekstuele toelichting bij de winst- en verliesrekening. 
Het is belangrijk dat we morgen even kort afstemmen over de voortgang.
```

---

## 6. Word Template (Jinja2)
*Dit gedeelte wordt gebruikt voor het genereren van het uiteindelijke Word-rapport via de `docxtpl` library.*

# Nieuwe Actiepunten Gevonden

## Bron Analyse
{{ analyse }}

---

## To-Do Lijst
{% if todos %}
{% for todo in todos %}
- [ ] {% if todo.prioriteit == 'hoog' %}**[PRIO]** {% endif %}{{ todo.taak }}
{% endfor %}
{% else %}
*Geen specifieke actiepunten gevonden.*
{% endif %}

---
### Informatie
**Bron:** {{ database_file.bron }}  
**Datum van verwerking:** {{ database_file.datum }}

---
*Dit document is gegenereerd door de Todo Agent en de taken zijn toegevoegd aan de master-lijst.*