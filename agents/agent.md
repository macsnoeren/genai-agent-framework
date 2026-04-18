# Documentatie: Algemene Agent

Deze agent dient als basis voor algemene documentanalyse en rapportage.

## 4. Configuratie
```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input",
  "output_directory": "data/output",
  "collection_file_path": "data/output/master_db.jsonl"
}
```

# Verslag: {{ titel }}

## 1. Algemene Informatie
**Datum:** {{ datum }}  
**Locatie:** {{ locatie }}  
**Notulist:** {{ notulist }}

**Aanwezig:**  
{% for d in deelnemers %}- {{ d }}{% if not loop.last %}{% endif %}
{% endfor %}

**Afwezig:**  
{% if afwezig %}{% for a in afwezig %}- {{ a }}{% endfor %}{% else %}Geen afmeldingen geregistreerd.{% endif %}

---

## 2. Agendapunten
{% for punt in agendapunten %}
### {{ punt.nummer }}. {{ punt.onderwerp }}
{{ punt.bespreking }}

{% endfor %}

---

## 3. Genomen Besluiten
{% if besluiten %}{% for b in besluiten %}
- **Besluit {{ b.nummer }}:** {{ b.beschrijving }}
{% endfor %}{% else %}Er zijn geen specifieke besluiten vastgelegd.{% endif %}

---

## 4. Actiepunten
| Nr. | Verantwoordelijke | Omschrijving | Deadline |
|:---|:---|:---|:---|
{% for a in acties %}
| {{ a.nummer }} | {{ a.verantwoordelijke }} | {{ a.beschrijving }} | {{ a.deadline }} |
{% endfor %}

---
*Dit verslag is automatisch gegenereerd door de AI Notulist Agent.*