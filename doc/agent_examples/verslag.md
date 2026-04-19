# Documentatie: Verslag Agent

De **Verslag Agent** is een veelzijdige AI-configuratie binnen het framework die is ontwikkeld om uiteenlopende documenten (zoals memo's, voortgangsrapportages of projectupdates) te analyseren. De agent synthetiseert de kerninhoud tot een helder verslag en extraheert relevante actiepunten voor verdere opvolging.

## 1. Doelstelling
*   **Analytisch:** Het identificeren van de essentie in complexe documenten.
*   **Synthese:** Het herschrijven van informatie naar een gestructureerd en leesbaar narratief.
*   **Taakextractie:** Het isoleren van actiepunten en opdrachten die in de tekst verborgen zijn.
*   **Idee-uitwerking:** Het herkennen van 'Idee:' tags en deze uitwerken tot mogelijke vervolgstappen.

## 2. Prompt Logica
De agent hanteert de instructies uit `verslag.json` om een kwalitatieve samenvatting te genereren:
1.  **Begrijpend Lezen:** De AI fungeert als een assistent die de context van het brondocument begrijpt.
2.  **Narratieve Opbouw:** De focus ligt op het creëren van een "mooi verslag", wat duidt op een vloeiende schrijfstijl in plaats van enkel opsommingen.
3.  **Lijstvorming:** Specifieke aandacht voor actiepunten die aan het einde van het verslag worden gegroepeerd.
4.  **Idee-analyse:** Bij het herkennen van de prefix 'Idee:' zal de agent dit punt niet alleen samenvatten, maar proactief meedenken over de uitwerking.
5.  **Validatie:** De output wordt strikt beperkt tot een JSON-object inclusief de nieuwe `ideeen` array.

## 3. JSON Output Schema
De agent levert de data aan volgens dit schema:
*   `verslag`: Een string bevattende de volledige tekstuele analyse/samenvatting.
*   `actiepunten`: Een array van strings, waarbij elk item een uniek actiepunt vertegenwoordigt.
*   `ideeen`: Een lijst met objecten bevattende de `titel` van het idee en een gedetailleerde `uitwerking`.

## 4. Configuratie
De operationele parameters voor de Verslag Agent:

```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input",
  "output_directory": "data/output",
  "done_directory": "data/done",
  "report_directory": "data/reports",
  "collection_file_path": "data/output/verslagen_master.jsonl"
}
```

---

## 5. Voorbeeld Invoer (Ruwe Tekst)
Een voorbeeld van invoer die deze agent effectief kan verwerken:

```text
Projectstatus Update - Cloud Migratie
We zijn deze week begonnen met de voorbereidingen voor de migratie van de legacy servers. Sophie heeft de inventarisatie afgerond, maar merkt op dat er nog onduidelijkheid is over de database-rechten. Mark moet dit voor woensdag uitzoeken. 

De algemene voortgang is goed. Erik is bezig met het inrichten van de testomgeving. Sophie gaat volgende week de eerste tests runnen. Vergeet niet dat we voor de go-live nog een security audit moeten aanvragen bij de IT-afdeling.
```

---

## 6. Word Template (Jinja2)
*Dit gedeelte wordt gebruikt voor het genereren van het uiteindelijke Word-rapport via de `docxtpl` library.*

# Documentanalyse & Verslag

## Verslag
{{ verslag }}

---

## Actiepunten
{% if actiepunten %}
{% for actie in actiepunten %}
- {{ actie }}
{% endfor %}
{% else %}
*Geen expliciete actiepunten gevonden in het brondocument.*
{% endif %}

---

{% if ideeen %}
## Mogelijke Vervolgstappen
{% for item in ideeen %}
### Idee: {{ item.titel }}
**Uitwerking:** {{ item.uitwerking }}

{% endfor %}
{% endif %}

---
*Dit document is gegenereerd door de Verslag Agent op basis van automatische tekstanalyse.*