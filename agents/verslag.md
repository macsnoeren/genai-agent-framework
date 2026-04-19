# Documentatie: Verslag Agent

De **Verslag Agent** analyseert uiteenlopende documenten (memo's, voortgangsrapportages, projectupdates) en synthetiseert de inhoud tot een helder verslag. Naast een narratieve samenvatting extraheert de agent actiepunten en werkt hij ideeën — herkenbaar aan de prefix `Idee:` — uit tot concrete vervolgstappen.

## 1. Doelstelling

- **Analytisch**: De essentie van complexe documenten identificeren.
- **Synthese**: Informatie herschrijven naar een gestructureerd, leesbaar narratief.
- **Taakextractie**: Verborgen actiepunten en opdrachten isoleren.
- **Idee-uitwerking**: `Idee:`-tags herkennen en uitwerken tot mogelijke vervolgstappen met een inschatting van uitvoering of impact.

## 2. Prompt Logica

1. **Begrijpend lezen** — de AI begrijpt de context van het brondocument.
2. **Narratieve opbouw** — focus op een vloeiende schrijfstijl, niet enkel opsommingen.
3. **Actiepunten** — worden gegroepeerd in een aparte lijst aan het einde.
4. **Idee-analyse** — bij de prefix `Idee:` denkt de agent proactief mee over uitwerking.
5. **Verzamelbak** — een `database_file`-object wordt voorbereid voor de centrale `.jsonl`-verzamelbak.

## 3. JSON Output Schema

```json
{
  "verslag": "string",
  "actiepunten": ["string"],
  "ideeen": [
    {
      "titel": "string",
      "uitwerking": "string"
    }
  ],
  "database_file": {}
}
```

Het veld `database_file` bevat een samenvatting voor de centrale verzamelbak (`verslagen_master.jsonl`).

## 4. Configuratie

```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input/verslagen",
  "output_directory": "data/output/verslagen",
  "done_directory": "data/done/verslagen",
  "template_path": "data/templates/verslag.docx",
  "report_directory": "data/reports/verslagen",
  "collection_file_path": "data/output/verslagen_master.jsonl"
}
```

Het Word-template staat op `data/templates/verslag.docx`.

## 5. Voorbeeld Invoer

```text
Projectstatus Update - Cloud Migratie
We zijn deze week begonnen met de voorbereidingen voor de migratie van de legacy servers.
Sophie heeft de inventarisatie afgerond, maar merkt op dat er nog onduidelijkheid is over
de database-rechten. Mark moet dit voor woensdag uitzoeken.

De algemene voortgang is goed. Erik is bezig met het inrichten van de testomgeving.
Sophie gaat volgende week de eerste tests runnen. Vergeet niet dat we voor de go-live
nog een security audit moeten aanvragen bij de IT-afdeling.

Idee: Stel een geautomatiseerde dagelijkse backup in voor de migratieperiode.
```

De `Idee:`-regel wordt door de agent herkend en uitgewerkt in het `ideeen`-veld.

## 6. Word Template (Jinja2-variabelen)

Het template `data/templates/verslag.docx` gebruikt de volgende variabelen:

| Variabele | Beschrijving |
| :--- | :--- |
| `{{ verslag }}` | De volledige tekstuele samenvatting |
| `{% for actie in actiepunten %}` | Loop over actiepunten (strings) |
| `{% if ideeen %}` | Conditioneel blok — alleen zichtbaar als er ideeën zijn |
| `{% for item in ideeen %}` | Loop over ideeën (`item.titel`, `item.uitwerking`) |
