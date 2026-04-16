#!/usr/bin/env python

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import requests

# Voeg de 'lib' directory toe aan sys.path
sys.path.append(str(Path(__file__).parent / "lib"))

from docdialog_client import DocumentDialogueClient

# Get your access token on the RWE website https://ai.rwe.com/
ACCESS_TOKEN = "PASTE_HIER_JOUW_ACCESS_TOKEN"  # <-- vervang door je echte token

def main():
    if ACCESS_TOKEN == "PASTE_HIER_JOUW_ACCESS_TOKEN":
        print("⚠️ Vul eerst je ACCESS_TOKEN in bovenaan app.py.")
        return

    client = DocumentDialogueClient(ACCESS_TOKEN)

    # 1) Modellen ophalen
    try:
        models_info = client.list_models()
    except Exception as e:
        print("Fout bij ophalen van modellen:", e)
        return

    models = models_info.get("models", [])
    default_model = models_info.get("default")

    print("Beschikbare modellen:")
    for m in models:
        mark = ""
        if default_model and m.get("id") == default_model:
            mark = " (default)"
        print(f" - {m.get('id', '')}: {m.get('name', '')}{mark}")
    print()

    if not default_model and models:
        default_model = models[0].get("id")

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
            response = client.send_message(chat_id, text=user_text)
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
