# Documentatie: Todo Agent

De **Todo Agent** scant diverse documenten op taken, actiepunten en to-do items en consolideert deze in een centrale verzamelbak. De agent produceert **geen losse JSON-uitvoer per bestand** — alle resultaten worden direct toegevoegd aan de master-lijst (`todo_master_list.jsonl`).

## 1. Doelstelling

- **Identificatie**: Expliciete en impliciete taken herkennen in ongestructureerde tekst.
- **Prioritering**: Belangrijke taken krijgen prioriteit `hoog`, overige taken `normaal`.
- **Consolidatie**: Actiepunten uit verschillende bronbestanden samenvoegen in één centrale lijst.

## 2. Prompt Logica

1. **Extractie** — scannen op trefwoorden zoals "moet", "actie", "todo", "taak" en werkwoordsvormen die duiden op een opdracht.
2. **Prioritering** — bepalen of een taak als belangrijk aangemerkt moet worden (`hoog`) of niet (`normaal`).
3. **Sortering** — taken met prioriteit `hoog` worden bovenaan gezet in de output.
4. **Analytische samenvatting** — een korte `analyse` biedt context over het brondocument.
5. **Database-object** — het `database_file`-veld bevat datum, bronvermelding en de takenlijst, klaar voor de verzamelbak.

## 3. JSON Output Schema

```json
{
  "analyse": "string",
  "todos": [
    {
      "taak": "string",
      "prioriteit": "hoog | normaal",
      "status": "open"
    }
  ],
  "database_file": {
    "datum": "string",
    "bron": "string",
    "items": [
      {
        "taak": "string",
        "prioriteit": "hoog | normaal",
        "status": "open"
      }
    ]
  }
}
```

## 4. Configuratie

```json
{
  "provider": "ollama",
  "model": "gpt-oss:120b-cloud",
  "input_directory": "data/input/todos",
  "done_directory": "data/done/todos",
  "collection_file_path": "data/output/todos/todo_master_list.jsonl"
}
```

> **Let op**: `output_directory` is bewust weggelaten. De agent slaat geen losse JSON op per bestand — alleen het `database_file`-object wordt via `collection_file_path` aan de centrale master-lijst toegevoegd.

## 5. Voorbeeld Invoer

```text
Memo: Voorbereiding Kwartaalcijfers
We moeten de presentatie voor de stakeholders uiterlijk vrijdag af hebben.
Sophie, kan jij de grafieken van de omzet trekken?
Vergeet niet dat de audit-resultaten ook nog in de bijlage moeten.
Mark gaat over de tekstuele toelichting bij de winst- en verliesrekening.
Het is belangrijk dat we morgen even kort afstemmen over de voortgang.
```

## 6. Word Template (Jinja2-variabelen)

De todo-agent gebruikt geen Word-template — resultaten worden uitsluitend naar de centrale verzamelbak geschreven. Wil je toch een rapport genereren, voeg dan `template_path` en `report_directory` toe aan de configuratie en gebruik onderstaande variabelen:

| Variabele | Beschrijving |
| :--- | :--- |
| `{{ analyse }}` | Korte samenvatting van het brondocument |
| `{% for todo in todos %}` | Loop over taken (`todo.taak`, `todo.prioriteit`, `todo.status`) |
| `{{ database_file.bron }}` | Bestandsnaam van het bronbestand |
| `{{ database_file.datum }}` | Datum van verwerking |
