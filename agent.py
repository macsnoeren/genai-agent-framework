#!/usr/bin/env python

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging
import requests

# Voeg de 'lib' directory toe aan sys.path, als deze niet al is toegevoegd
if str(Path(__file__).parent / "lib") not in sys.path:
    sys.path.append(str(Path(__file__).parent / "lib"))

from docdialog_client import DocumentDialogueClient
from ai_agent import AIAgent

# Configureer logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Definieer een aparte logger voor de agent's interne stappen
agent_logger = logging.getLogger('RWEAIAgent')
agent_logger.setLevel(logging.INFO) # Kan op DEBUG gezet worden voor meer details

# Get your access token on the RWE website https://ai.rwe.com/
ACCESS_TOKEN = "VERVANG_DOOR_JE_ECHTE_TOKEN"  # <-- VERVANG DOOR JE ECHTE TOKEN

def main():
    if ACCESS_TOKEN == "VERVANG_DOOR_JE_ECHTE_TOKEN":
        print("⚠️ Vul eerst je ACCESS_TOKEN in bovenaan rwe-ai-agent.py.")
        return

    # Voorbeeld van het instellen van een default_prompt
    # default_agent_instructions = "Zorg ervoor dat al je antwoorden bondig en direct zijn."
    # agent = RWEAIAgent(ACCESS_TOKEN, default_prompt=default_agent_instructions)
    agent = AIAgent(ACCESS_TOKEN)

    print("Modellen ophalen...")
    models = agent.list_models()
    print(f"Beschikbare modellen: {[m['id'] for m in models]}")

    print("\nNieuwe chat aanmaken...")
    chat_id = agent.create_chat()
    print(f"Chat aangemaakt met ID: {chat_id}")
    logger.info(f"Actieve chat_id voor agent: {chat_id}")
    
    print("\nStart agent interactie (typ 'exit' om te stoppen):")
    print("De agent zal proberen complexe taken op te lossen via Plan -> Execute -> Verify.")
    while True:
        user_input = input("\nJij (Agent Taak): ").strip()
        if user_input.lower() in ["exit", "quit", "q"]:
            break

        try:
            # Gebruik de run_agent methode voor multi-step reasoning
            response = agent.run_agent(user_input, max_iterations=3)
            role = response.get("role", "assistant")
            content = response.get("content", "")
            print(f"{role.capitalize()}: {content}\n")
        except requests.HTTPError as http_err:
            logger.error(f"HTTP-fout: {http_err.response.status_code} - {http_err.response.text}")
            print(f"HTTP-fout: {http_err.response.status_code} - {http_err.response.text}")
            if http_err.response.status_code == 401:
                print("→ Waarschijnlijk is je access token verlopen of ongeldig.")
            continue
        except ValueError as ve:
            logger.error(f"Configuratiefout: {ve}")
            print(f"Fout: {ve}")
            continue
        except Exception as e:
            logger.error(f"Onbekende fout bij agent run: {e}", exc_info=True)
            print(f"Onbekende fout bij agent run: {e}")
            
            continue

if __name__ == "__main__":
    main()
