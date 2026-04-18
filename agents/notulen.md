# Documentatie: Notulen Agent

De **Notulen Agent** is een gespecialiseerde AI-configuratie binnen het framework die is ontwikkeld om ongestructureerde vergaderaantekeningen om te zetten in professionele, actiegerichte notulen. Het systeem lost het probleem op van inconsistente verslaglegging en versnelt het proces van actie-opvolging door automatisch metadata, besluiten en taken te extraheren uit ruwe tekst.

## 1. Doelstelling
*   **Synthese:** Het omzetten van telegramstijl aantekeningen naar vloeiend, zakelijk Nederlands.
*   **Extractie:** Automatisch identificeren van deelnemers, actiehouders en deadlines.
*   **Structurering:** Informatie groeperen in logische agendapunten en formele besluitenlijsten.

## 2. Prompt Logica
De agent maakt gebruik van een gestructureerde prompt (gedefinieerd in `notulen.json`) die de AI de rol geeft van een ervaren secretaris. De prompt is opgebouwd uit:
1.  **Persona:** Een professionele notulist die objectief en helder rapporteert.
2.  **Extractie-instructies:** Specifieke regels voor het herkennen van patronen (zoals "Actie (Naam):").
3.  **Huisstijl-richtlijnen:** Gebruik van zakelijk Nederlands, vermijden van bullets in doorlopende tekst, en het hanteren van een vast datumformaat (DD-MM-JJJJ). Ook worden onduidelijke actiegegevens gemarkeerd met 'Vraagteken'.
4.  **Validatie:** De output wordt gedwongen in een strikt JSON-formaat voor foutloze verwerking door de document-generator.

## 3. JSON Output Schema
De agent levert gegevens aan volgens een vast schema, wat zorgt voor consistentie in de rapportage. Belangrijke velden zijn onder meer metadata (titel, datum, locatie), genummerde agendapunten, een besluitenlijst en een tabel-georiënteerde lijst met acties.

## 4. Configuratie
De operationele instellingen voor deze agent zijn als volgt:

```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input/notulen",
  "output_directory": "data/output",
  "done_directory": "data/done",
  "report_directory": "data/reports"
}
```

---

## 5. Voorbeeld Invoer (Ruwe Aantekeningen)
Onderstaand een voorbeeld van hoe een invoerbestand (`.txt` of geëxtraheerde tekst uit Word/Excel) eruit kan zien voor deze agent:

```text
Vergadering: Update Agent Framework
Datum: 24-05-2024
Locatie: Vergaderruimte 2
Deelnemers: Sophie, Mark, Erik
Afwezig: Linda (ziek)
Notulist: Sophie

Aantekeningen:
- We hebben de nieuwe Ollama integratie besproken. Mark geeft aan dat het lokaal goed draait.
- Erik stelt voor om ook een Excel extractie toe te voegen. Iedereen is het hiermee eens. actie (Erik): Maak een voorbeeld Excel bestand voor testen.
- Besloten is om vanaf volgende week alle notulen via dit framework te laten lopen.
- Sophie merkt op dat de templates nog wat finetuning nodig hebben. Actie - Sophie: Word template updaten met bedrijfslogo (deadline: aanstaande vrijdag).

Acties:
- actie (Mark): Push de laatste wijzigingen naar de 'main' branch (deadline: morgen)
```

---

## 6. Word Template (Jinja2)
*Dit gedeelte wordt gebruikt voor het genereren van het uiteindelijke Word-rapport via de `docxtpl` library.*

# Verslag: {{ titel }}

### 1. Algemene Informatie
**Datum:** {{ datum }}  
**Locatie:** {{ locatie }}  
**Notulist:** {{ notulist }}

**Aanwezig:**  
{% for d in deelnemers %}- {{ d }}{% if not loop.last %}{% endif %}
{% endfor %}

**Afwezig:**  
{% if afwezig %}{% for a in afwezig %}- {{ a }}{% endfor %}{% else %}Geen afmeldingen geregistreerd.{% endif %}

---

### 2. Agendapunten
{% for punt in agendapunten %}
**{{ punt.nummer }}. {{ punt.onderwerp }}**  
{{ punt.bespreking }}

{% endfor %}

---

### 3. Genomen Besluiten
{% if besluiten %}{% for b in besluiten %}
- **Besluit {{ b.nummer }}:** {{ b.beschrijving }}
{% endfor %}{% else %}Er zijn geen specifieke besluiten vastgelegd.{% endif %}

---

### 4. Actiepunten
| Nr. | Verantwoordelijke | Omschrijving | Deadline |
|:---|:---|:---|:---|
{% for a in acties %}
| {{ a.nummer }} | {{ a.verantwoordelijke }} | {{ a.beschrijving }} | {{ a.deadline }} |
{% endfor %}

---
*Dit verslag is automatisch gegenereerd door de AI Notulist Agent.*