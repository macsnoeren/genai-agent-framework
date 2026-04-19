# genai-agent-framework

Een modulair en uitbreidbaar framework voor het bouwen van AI-agents die taken uitvoeren via een **Plan → Execute → Verify** workflow. Het framework ondersteunt meerdere LLM-providers (zoals Ollama en DocumentDialogue) en verwerkt automatisch batches van bestanden op basis van eenvoudige JSON-configuratiebestanden.

## Kernfuncties

- **Plan-Execute-Verify Loop**: De agent maakt eerst een plan, voert dit uit en verifieert daarna of het resultaat voldoet. Bij falen past hij het plan aan en probeert opnieuw (configureerbaar aantal iteraties).
- **Multi-Provider Support**: Abstracte basisklasse voor LLM-clients — eenvoudig wisselen tussen lokale modellen (Ollama) en enterprise API's (DocumentDialogue).
- **Batch Verwerking**: Verwerkt automatisch alle bestanden in een inputmap op basis van een JSON-configuratie.
- **Bestandsextractie**: Automatische tekstextractie uit `.txt`, `.docx` (Word) en `.xlsx` (Excel, inclusief tabblad-conversie).
- **Rapportage**: Genereer automatisch Word-documenten via Jinja2-templates (`docxtpl`).
- **Verzamelbak**: Aggregeer resultaten uit meerdere sessies naar één centraal `.jsonl`-bestand.

## Projectstructuur

```text
├── agents/                     # Agent-configuraties (JSON) en documentatie (Markdown)
│   ├── notulen.json / .md      # Agent voor vergadernotulen
│   ├── todo.json / .md         # Agent voor taakextractie
│   └── verslag.json / .md      # Agent voor verslaggeving
├── data/
│   ├── input/                  # Bronbestanden per agent-submap
│   ├── output/                 # Gegenereerde JSON-resultaten
│   ├── done/                   # Gearchiveerde bronbestanden (na verwerking)
│   ├── reports/                # Gegenereerde Word-rapporten
│   └── templates/              # Word-templates (.docx) voor rapportage
├── lib/
│   ├── ai_agent.py             # Hoofd-agent met de PEV-loop
│   ├── base_client.py          # Abstracte interface voor LLM-providers
│   ├── ollama_client.py        # Provider voor lokale Ollama LLM's
│   └── docdialog_client.py     # Provider voor DocumentDialogue enterprise API
├── agent.py                    # Entrypoint voor batch-verwerking
├── chat-test.py                # Interactief test-script voor de chatverbinding
├── config.json                 # API-tokens (niet in Git)
├── config.json.example         # Voorbeeld configuratiebestand
├── setup.bat / setup.sh        # Scripts voor mappenstructuur-initialisatie
└── agent.bat                   # Windows runner
```

## Installatie

1. **Mappen aanmaken** — voer het setup-script uit:
   ```bash
   # Windows
   setup.bat
   # Linux/macOS
   ./setup.sh
   ```

2. **Afhankelijkheden installeren**:
   ```bash
   pip install requests python-docx openpyxl docxtpl
   ```

3. **Configuratie** — maak `config.json` aan vanuit het voorbeeld:
   ```json
   {
     "ACCESS_TOKEN": "jouw_token_hier",
     "OLLAMA_BASE_URL": "http://localhost:11434"
   }
   ```
   `OLLAMA_BASE_URL` is optioneel en standaard `http://localhost:11434`.

## Gebruik

### Alle agents uitvoeren
Zonder argument verwerkt het script alle `.json`-bestanden in de `agents/`-map:
```bash
agent.bat
```

### Specifieke agent uitvoeren
```bash
agent.bat agents/notulen.json
```

Het script doorloopt per bestand de volgende stappen:
1. Tekst extraheren uit het bronbestand (`.txt`, `.docx` of `.xlsx`).
2. De Plan-Execute-Verify loop uitvoeren.
3. Het resultaat opslaan als JSON in `output_directory`.
4. Optioneel een Word-rapport genereren via een `.docx`-template.
5. Optioneel het `database_file`-object toevoegen aan de verzamelbak (`collection_file_path`).
6. Het bronbestand verplaatsen naar `done_directory` met tijdstempel.

### Interactief testen
Test de verbinding met je LLM-provider zonder batch-verwerking:
```bash
python chat-test.py
```

## Agent Configuratie

Elke agent wordt gedefinieerd door een JSON-bestand in de `agents/`-map.

| Veld | Verplicht | Beschrijving |
| :--- | :---: | :--- |
| `provider` | ✓ | LLM-provider: `ollama` of `docdialog` |
| `model` | | Model-ID (bijv. `llama3`). Zonder waarde wordt het eerste beschikbare model gekozen. |
| `instructions` | ✓ | Taakomschrijving voor de agent (de systeemprompt). |
| `output_description` | ✓ | Het verwachte JSON-schema voor de output. |
| `input_directory` | ✓ | Map met te verwerken bronbestanden. |
| `output_directory` | | Map voor de JSON-uitvoer. Weglaten als je alleen een `collection_file_path` gebruikt. |
| `done_directory` | ✓ | Map waarnaar bronbestanden worden gearchiveerd na verwerking. |
| `template_path` | | Pad naar het `.docx`-template voor Word-rapportage. |
| `report_directory` | | Map voor de gegenereerde Word-rapporten. |
| `collection_file_path` | | Pad naar een `.jsonl`-verzamelbak voor geaggregeerde resultaten. |
| `max_iterations` | | Maximaal aantal PEV-iteraties (standaard: `3`). |

### Voorbeeld `agent.json`

```json
{
  "provider": "ollama",
  "model": "llama3",
  "instructions": "Analyseer het document en extraheer alle actiepunten.",
  "output_description": "{\"verslag\": \"string\", \"actiepunten\": [\"string\"]}",
  "input_directory": "data/input/verslagen",
  "output_directory": "data/output/verslagen",
  "done_directory": "data/done/verslagen",
  "template_path": "data/templates/verslag.docx",
  "report_directory": "data/reports/verslagen",
  "collection_file_path": "data/output/verslagen_master.jsonl",
  "max_iterations": 3
}
```

### Verzamelbak (`collection_file_path`)

Als een agent een `collection_file_path` heeft, wordt het veld `database_file` uit de JSON-output automatisch toegevoegd aan dat `.jsonl`-bestand. Zo bouw je over meerdere sessies een centrale database op. Als je alleen een verzamelbak wilt en geen losse JSON-uitvoer per bestand, laat je `output_directory` weg.

## Providers

### Ollama (lokaal)
- Vereist een draaiende Ollama-instantie op `OLLAMA_BASE_URL`.
- **Documentuploads worden niet ondersteund.** Het framework valt automatisch terug op tekstextractie.

### DocumentDialogue (enterprise)
- Vereist een geldig `ACCESS_TOKEN` in `config.json`.
- Ondersteunt volledige documentuploads, persona's en extensies.

## Uitbreiden

### Nieuwe provider toevoegen
Implementeer de `BaseLLMClient`-interface in `lib/`:

```python
from lib.base_client import BaseLLMClient

class MijnProvider(BaseLLMClient):
    def list_models(self): ...
    def create_chat(self, model=None): ...
    def send_message(self, chat_id, text, model=None): ...
    def upload_document(self, chat_id, file_path): ...
    def delete_chat(self, chat_id): ...
```

### Nieuwe agent toevoegen
1. Maak `agents/mijn-agent.json` aan met instructies en directorystructuur.
2. Optioneel: maak een Word-template in `data/templates/`.
3. Optioneel: schrijf een `agents/mijn-agent.md` als documentatie.

### Word-template aanpassen
Templates worden gerenderd via `docxtpl` (Jinja2-syntax). Gebruik de sleutelnamen uit de JSON-output van de agent als variabelen:

```
{{ verslag }}
{% for actie in actiepunten %}- {{ actie }}{% endfor %}
```

## Licentie
Dit project is bedoeld voor intern gebruik.
