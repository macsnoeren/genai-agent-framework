#!/usr/bin/env python

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import requests
import json

# Voeg de 'lib' directory toe aan sys.path
sys.path.append(str(Path(__file__).parent / "lib"))

from lib.ollama_client import OllamaClient

def load_config():
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def main():
    config = load_config()
    access_token = config.get("ACCESS_TOKEN", "PASTE_HIER_JOUW_ACCESS_TOKEN")

    # Voor Ollama gebruiken we de nieuwe provider interface
    print("Initialiseren Ollama client...")
    client = OllamaClient(base_url="http://localhost:11434")

    # Voor DocumentDialogue zou het zijn:
    # from lib.docdialog_client import DocumentDialogueClient
    # client = DocumentDialogueClient(access_token)

    # 1) Modellen ophalen
    try:
        models = client.list_models()
    except Exception as e:
        print("Fout bij ophalen van modellen:", e)
        return

    default_model = None

    print("Beschikbare modellen:")
    for i, m in enumerate(models):
        print(f" {i + 1}) {m.get('id', '')} ({m.get('name', '')})")
    print()
    
    if models:
        while True:
            choice = input(f"Selecteer een model (1-{len(models)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    default_model = models[idx].get("id")
                    print(f"Geselecteerd model: {default_model}")
                    break
            print("Ongeldige keuze, probeer het opnieuw.")
    else:
        print("Geen modellen gevonden.")
        return

    # 2) Chat aanmaken
    try:
        chat_id = client.create_chat(model=default_model)
    except Exception as e:
        print("Fout bij aanmaken van chat:", e)
        return

    print(f"Nieuwe chat aangemaakt, id: {chat_id}")
    print("Typ 'exit' om te stoppen.\n")

    # 3) Interactieve loop
    while True:
        user_text = input("Jij: ").strip()
        if user_text.lower() in ("exit", "quit", "q"):
            break

        try:
            response = client.send_message(chat_id, text=user_text, model=default_model)
        except requests.HTTPError as http_err:
            print("HTTP-fout:", http_err.response.status_code, http_err.response.text)
            if http_err.response.status_code == 401:
                print("→ Waarschijnlijk is je access token verlopen of ongeldig.")
            continue
        except Exception as e:
            print("Onbekende fout bij versturen van bericht:", e)
            continue

        role = response.get("role", "assistant")
        content = response.get("content", "")
        print(f"{role.capitalize()}: {content}\n")


if __name__ == "__main__":
    main()
