# genai-agent-framework

Een modulair en uitbreidbaar framework voor het bouwen van AI-agents die taken uitvoeren via een **Plan -> Execute -> Verify** workflow. Het framework ondersteunt meerdere LLM-providers (zoals Ollama en Document Dialogue) en kan batch-verwerking uitvoeren op verschillende bestandstypen.

## Kernfuncties

- **Plan-Execute-Verify Loop**: De agent plant eerst zijn acties, voert ze uit en verifieert vervolgens of het resultaat voldoet aan de opdracht. Bij falen past hij het plan aan.
- **Multi-Provider Support**: Abstracte basisklasse voor LLM-clients, waardoor eenvoudig gewisseld kan worden tussen lokale modellen (Ollama) en enterprise API's.
- **Batch Verwerking**: Verwerkt automatisch alle bestanden in een directory op basis van een JSON-configuratie.
- **Bestandsextractie**: Automatische tekstextractie uit `.txt`, `.docx` (Word) en `.xlsx` (Excel, inclusief tabblad-conversie naar CSV-stijl).
- **Rapportage**: Genereer automatisch Word-documenten in de huisstijl van je bedrijf met behulp van templates (`docxtpl`).

## Projectstructuur

```text
├── agents/             # Agent-specifieke JSON configuraties
├── data/               # Werkdirectories (input, output, done, reports)
├── lib/                # Core logica
│   ├── ai_agent.py     # De hoofd-agent met de PEV-loop
│   ├── base_client.py  # Abstracte interface voor LLM providers
│   ├── ollama_client.py# Provider voor lokale Ollama LLM's
│   └── docdialog_client.py # Provider voor enterprise LLM API
├── templates/          # Word templates (.docx) voor rapportage
├── agent.py            # Hoofd-entrypoint voor batch verwerking
├── chat-test.py        # Interactief test-script voor chat-functionaliteit
├── config.json         # Configuratie voor API-tokens (niet in Git)
├── setup.bat/.sh       # Scripts voor mappen-initialisatie
└── agent.bat           # Windows runner voor de agent
```

## Installatie

1.  **Mappen aanmaken**:
    Voer de setup-script uit om de benodigde mappenstructuur te genereren:
    ```bash
    # Windows
    setup.bat
    # Linux/macOS
    ./setup.sh
    ```

2.  **Afhankelijkheden installeren**:
    Zorg dat de benodigde Python libraries aanwezig zijn:
    ```bash
    pip install requests python-docx openpyxl docxtpl
    ```

3.  **Configuratie**:
    Maak een `config.json` aan in de root met je API-tokens (indien nodig):
    ```json
    {
      "ACCESS_TOKEN": "jouw_token_hier"
    }
    ```

## Gebruik

### Batch Verwerking
Plaats je bestanden in `data/input` en definieer een agent in `agents/agent.json`. Run daarna de agent:

```bash
agent.bat agents/agent.json
```

Het script zal:
1. Elk bestand in `data/input` uitlezen.
2. De tekst (bij .docx/.xlsx) extraheren en aan de prompt toevoegen.
3. De Plan-Execute-Verify loop doorlopen.
4. De resultaten opslaan in `data/output` (JSON) en `data/reports` (Word).
5. Het bronbestand verplaatsen naar `data/done`.

### Interactief Testen
Om de verbinding met je LLM-provider te testen zonder batch-verwerking:

```bash
python chat-test.py
```

## Agent Configuratie (`agent.json`)

Dit bestand bepaalt hoe de agent zich gedraagt en waar de bestanden worden opgeslagen.

| Veld | Type | Beschrijving |
| :--- | :--- | :--- |
| `provider` | string | De LLM provider die gebruikt moet worden (`ollama` of `docdialog`). |
| `model` | string | De ID van het te gebruiken model (bijv. `llama3` of `gpt-oss:120b-cloud`). |
| `instructions` | string | De specifieke taakomschrijving voor de agent. |
| `output_description` | string | Beschrijving van de gewenste JSON-velden voor validatie en rapportage. |
| `input_directory` | string | Pad naar de map met bronbestanden die verwerkt moeten worden. |
| `output_directory` | string | Pad waar de resulterende JSON-bestanden worden opgeslagen. |
| `done_directory` | string | Pad waar de bronbestanden naartoe worden verplaatst na succesvolle verwerking. |
| `template_path` | string | (Optioneel) Pad naar het `.docx` template voor huisstijl-rapportage. |
| `report_directory` | string | (Optioneel) Pad waar de gegenereerde Word-rapporten worden opgeslagen. |

### Voorbeeld `agent.json`
```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "instructions": "Analyseer het document en extraheer actiepunten.",
  "output_description": "JSON: {\"verslag\": \"string\", \"actiepunten\": [\"string\"]}",
  "input_directory": "data/input",
  "output_directory": "data/output",
  "done_directory": "data/done"
}
```

## Uitbreiden

### Nieuwe Provider Toevoegen
Implementeer de `BaseLLMClient` interface in `lib/`:

```python
from lib.base_client import BaseLLMClient

class MijnNieuweProvider(BaseLLMClient):
    def list_models((...)): # Implementatie
    def send_message(self, chat_id, text, model=None): # Implementatie
    # ... etc
```

### Huisstijl Rapportage
Gebruik Jinja2-stijl placeholders in je Word-template in `templates/`. Bijvoorbeeld:
`{{ verslag }}` wordt vervangen door de waarde van de sleutel "verslag" uit de JSON-output van de agent.

## Licentie
Dit project is vertrouwelijk en bedoeld voor intern gebruik.

---
*Gegenereerd door Gemini Code Assist*