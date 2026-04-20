# Documentatie: Risk Analysis Agent

De **Risk Analysis Agent** verwerkt een Excelbestand met een risicoassessment van een industriële installatie (procesautomatisering, HVAC, branddetectie/-bestrijding, DCS/HMI, etc.) en genereert hieruit een volledig, gestructureerd securityrapport in JSON-formaat. De agent herschrijft en optimaliseert de ruwe Excel-data naar zakelijk Nederlands en brengt het rapport in lijn met de RWE-securityrapportstijl.

> **Let op**: Deze agent gebruikt de **DocumentDialogue**-provider, omdat het uploaden van Excelbestanden vereist is. Ollama ondersteunt geen documentuploads.

## 1. Doelstelling

- **Analyse**: Risicoregels per domein (Excel-tabblad) extraheren, samenvatten en taalkundig verbeteren.
- **Structurering**: Output indelen in meta-informatie, executive summary, introductie, impactmatrix, domeinen met risico's en openstaande acties.
- **Redactie**: Spelling- en grammaticafouten corrigeren, terminologie consistent maken, dubbele informatie verwijderen.
- **Rapportage**: JSON-output renderen naar een Word-rapport via `data/templates/risk-analysis.docx`.

## 2. Verwachte Invoer

Een `.xlsx`-bestand waarbij:
- **Elk tabblad** één domein vertegenwoordigt (bijv. `HVAC`, `Fire Detection & Suppression`, `DCS HMI Honeywell`).
- **Elke rij** (na de koprij) één risico beschrijft.
- De volgende kolommen aanwezig zijn (namen mogen licht afwijken):

| Kolom | JSON-veld |
| :--- | :--- |
| Asset | `asset` |
| Wat kan een aanvaller doen | `attacker_actions` |
| Entry points | `entry_points` |
| Effect/consequentie | `effects` |
| Impact | `impact` |
| Huidige maatregelen genomen | `existing_measures` |

Extra kolommen worden verwerkt in bestaande velden als ze inhoudelijk iets toevoegen.

## 3. Prompt Logica

De agent volgt een vaste verwerkingsstrategie:

1. **Meta-informatie** — plant- of locatienaam en assessmentdatum worden opgezocht in het Excel (titelblad of metadata). Ontbrekende waarden worden leeg gelaten.
2. **Impactmatrix** — altijd gevuld met de vijf vaste RWE-niveaus: Minor, Limited, Serious, Very Serious, Disastrous.
3. **Introductie** — beschrijft doel, scope (domeinnamen uit de tabbladen) en gehanteerde risicomatrix.
4. **Executive Summary** — vat de belangrijkste bevindingen samen: veiligheid, beschikbaarheid, bedrijfscontinuïteit. Sluit af met een zakelijke conclusie over de noodzaak van opvolging.
5. **Domeinen** — elk tabblad wordt één domeinobject. Rijen met daadwerkelijke risico's worden opgenomen; lege of puur technische koprijen worden overgeslagen.
6. **Risicoteksten** — alle tekstvelden worden herschreven naar kort, zakelijk Nederlands (max. 1–2 zinnen), met correctie van spelfouten en consistent terminologiegebruik.
7. **Openstaande acties** — alleen acties die in het Excel als openstaand of nader te onderzoeken zijn gemarkeerd (bijv. "actie", "TODO", "nog uitzoeken"). Elk krijgt een uniek ID (bijv. `HVAC-01`).

Stijlregels:
- Schrijf formeel maar leesbaar, in de stijl van een RWE-securityrapport.
- Gebruik gangbare OT-terminologie: unit, tripconditie, veiligheidssysteem, back-upregime, DCS, HMI, HVAC.
- Verzin geen risico's of feiten die niet in het Excel staan.
- Lege kolommen → lege string `""` in de JSON.

## 4. JSON Output Schema

```json
{
  "document": {
    "meta": {
      "title": "Result Risk Assessment <Plantnaam> <Datum>",
      "date": "YYYY-MM-DD",
      "author": "",
      "version": "1.0"
    },
    "executive_summary": "string (1–3 alinea's, gescheiden door \\n\\n)",
    "introduction": "string (1–3 alinea's, gescheiden door \\n\\n)",
    "impact_matrix": [
      { "impact": "Minor",        "description": "string" },
      { "impact": "Limited",      "description": "string" },
      { "impact": "Serious",      "description": "string" },
      { "impact": "Very Serious", "description": "string" },
      { "impact": "Disastrous",   "description": "string" }
    ],
    "open_actions": [
      {
        "id": "string (bijv. HVAC-01)",
        "domain": "string",
        "description": "string (1 zin)"
      }
    ],
    "domains": [
      {
        "name": "string (tabbladnaam)",
        "description": "string (1–2 zinnen of \"\")",
        "risks": [
          {
            "asset": "string",
            "attacker_actions": "string",
            "entry_points": "string",
            "effects": "string",
            "impact": "Minor | Limited | Serious | Very Serious | Disastrous",
            "existing_measures": "string"
          }
        ]
      }
    ]
  }
}
```

## 5. Configuratie

```json
{
  "provider": "docdialog",
  "model": "",
  "input_directory": "data/input/risk-analysis",
  "output_directory": "data/output/risk-analysis",
  "done_directory": "data/done/risk-analysis",
  "template_path": "data/templates/risk-analysis.docx",
  "report_directory": "data/reports/risk-analysis"
}
```

> **Let op**: Geen `collection_file_path` — elk risicoassessment is een op zichzelf staand document en wordt niet geaggregeerd in een centrale verzamelbak.

> Het veld `model` is leeg; DocumentDialogue gebruikt dan het standaardmodel van de instantie.

## 6. Word Template (Jinja2-variabelen)

Het template `data/templates/risk-analysis.docx` is opgebouwd uit de volgende secties:

| Sectie | Variabelen |
| :--- | :--- |
| Titelpagina | `{{ document.meta.title }}`, `{{ document.meta.date }}`, `{{ document.meta.author }}`, `{{ document.meta.version }}` |
| Executive Summary | `{{ document.executive_summary }}` |
| Introductie | `{{ document.introduction }}` |
| Impactmatrix | `{% for row in document.impact_matrix %}` → `row.impact`, `row.description` |
| Domeinen | `{% for domain in document.domains %}` → `domain.name`, `domain.description` |
| Risicotabel per domein | `{% for risk in domain.risks %}` → `risk.asset`, `risk.attacker_actions`, `risk.entry_points`, `risk.effects`, `risk.impact`, `risk.existing_measures` |
| Openstaande acties | `{% for action in document.open_actions %}` → `action.id`, `action.domain`, `action.description` |
