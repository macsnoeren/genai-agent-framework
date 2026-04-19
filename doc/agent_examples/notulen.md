# Documentatie: Notulen Agent

De **Notulen Agent** zet ongestructureerde vergaderaantekeningen automatisch om naar professionele, actiegerichte notulen. Het systeem extraheert metadata, agendapunten, besluiten en actiepunten en slaat het resultaat op als JSON, als Word-rapport en in een centrale verzamelbak.

## 1. Doelstelling

- **Synthese**: Telegramstijl aantekeningen omzetten naar vloeiend, zakelijk Nederlands.
- **Extractie**: Automatisch identificeren van deelnemers, besluiten, actiehouders en deadlines.
- **Structurering**: Informatie groeperen in logische agendapunten en formele lijsten.

## 2. Prompt Logica

De agent krijgt de rol van een ervaren notulist en werkt volgens vier stappen:

1. **Metadata extraheren** — titel, datum, locatie, deelnemers, afwezigen en notulist.
2. **Agendapunten opstellen** — losse notities worden gegroepeerd in genummerde punten met een uitgeschreven bespreking (geen telegramstijl).
3. **Actiepunten isoleren** — het volledige document wordt gescand op patronen zoals `actie (Naam):`, `Actie - Naam:` en `Actiepunt:`, ook als ze midden in de lopende tekst staan.
4. **Besluiten vastleggen** — expliciet genomen besluiten (bijv. "besloten is...") worden apart genoteerd.

Aanvullende richtlijnen:
- Ontbrekende velden worden gevuld met `"Niet vermeld"` (of een lege array).
- Onduidelijke actiegegevens worden gemarkeerd met `"Vraagteken"`.
- Datumformaat: `DD-MM-JJJJ`.
- Namen worden consistent weergegeven zoals bij de deelnemerslijst.

## 3. JSON Output Schema

```json
{
  "titel": "string",
  "datum": "string (DD-MM-JJJJ)",
  "locatie": "string",
  "notulist": "string",
  "deelnemers": ["string"],
  "afwezig": ["string"],
  "agendapunten": [
    {
      "nummer": 1,
      "onderwerp": "string",
      "bespreking": "string"
    }
  ],
  "besluiten": [
    {
      "nummer": 1,
      "beschrijving": "string"
    }
  ],
  "acties": [
    {
      "nummer": 1,
      "verantwoordelijke": "string",
      "beschrijving": "string",
      "deadline": "string"
    }
  ],
  "database_file": {}
}
```

Het veld `database_file` bevat een samengevatte versie van de vergadering voor de centrale verzamelbak (`vergaderingen_master.jsonl`).

## 4. Configuratie

```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input/notulen",
  "output_directory": "data/output/notulen",
  "done_directory": "data/done/notulen",
  "template_path": "data/templates/notulen.docx",
  "report_directory": "data/reports/notulen",
  "collection_file_path": "data/output/vergaderingen_master.jsonl"
}
```

Het Word-template staat op `data/templates/notulen.docx` en bevat een informatietabel, agendapunten, een besluitenlijst en een actiepuntentabel.

## 5. Voorbeeld Invoer

```text
Vergadering: Update Agent Framework
Datum: 24-05-2024
Locatie: Vergaderruimte 2
Deelnemers: Sophie, Mark, Erik
Afwezig: Linda (ziek)
Notulist: Sophie

Aantekeningen:
- We hebben de nieuwe Ollama integratie besproken. Mark geeft aan dat het lokaal goed draait.
- Erik stelt voor om ook een Excel extractie toe te voegen. Iedereen is het hiermee eens.
  actie (Erik): Maak een voorbeeld Excel bestand voor testen.
- Besloten is om vanaf volgende week alle notulen via dit framework te laten lopen.
- Sophie merkt op dat de templates nog wat finetuning nodig hebben.
  Actie - Sophie: Word template updaten met bedrijfslogo (deadline: aanstaande vrijdag).

Acties:
- actie (Mark): Push de laatste wijzigingen naar de 'main' branch (deadline: morgen)
```

## 6. Word Template (Jinja2-variabelen)

Het template `data/templates/notulen.docx` gebruikt de volgende variabelen:

| Variabele | Beschrijving |
| :--- | :--- |
| `{{ titel }}` | Titel van de vergadering |
| `{{ datum }}` | Datum in DD-MM-JJJJ |
| `{{ locatie }}` | Locatienaam |
| `{{ notulist }}` | Naam van de notulist |
| `{% for d in deelnemers %}` | Loop over aanwezige deelnemers |
| `{% for a in afwezig %}` | Loop over afwezigen |
| `{% for punt in agendapunten %}` | Loop over agendapunten (`punt.nummer`, `punt.onderwerp`, `punt.bespreking`) |
| `{% for b in besluiten %}` | Loop over besluiten (`b.nummer`, `b.beschrijving`) |
| `{% for a in acties %}` | Loop over acties (`a.nummer`, `a.verantwoordelijke`, `a.beschrijving`, `a.deadline`) |
