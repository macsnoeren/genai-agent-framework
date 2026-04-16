import requests
from typing import Dict, Any, List, Optional
from lib.base_client import BaseLLMClient

class OllamaClient(BaseLLMClient):
    """
    Koppeling met een lokale Ollama instantie.
    """
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.history: Dict[str, List[Dict[str, str]]] = {}
        self.chat_models: Dict[str, str] = {}

    def list_models(self) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        return [{"id": m["name"], "name": m["name"]} for m in models]

    def create_chat(self, model: Optional[str] = None) -> str:
        import uuid
        chat_id = str(uuid.uuid4())
        self.history[chat_id] = []
        if model:
            self.chat_models[chat_id] = model
        return chat_id

    def send_message(self, chat_id: str, text: str, model: Optional[str] = None) -> Dict[str, Any]:
        if chat_id not in self.history:
            self.history[chat_id] = []
        
        model_to_use = model or self.chat_models.get(chat_id)
        
        if not model_to_use:
            # Haal het eerste beschikbare model op als er echt niets is gekozen
            available = self.list_models()
            model_to_use = available[0]["id"] if available else "llama3"

        self.history[chat_id].append({"role": "user", "content": text})
        
        payload = {
            "model": model_to_use,
            "messages": self.history[chat_id],
            "stream": False
        }
        
        response = requests.post(f"{self.base_url}/api/chat", json=payload)
        response.raise_for_status()
        result = response.json()
        
        assistant_message = result.get("message", {})
        self.history[chat_id].append(assistant_message)
        
        return {
            "role": assistant_message.get("role"),
            "content": assistant_message.get("content")
        }

    def upload_document(self, chat_id: str, file_path: str) -> Dict[str, Any]:
        # Ollama ondersteunt standaard geen RAG via document upload in de /chat API.
        # Dit zou een implementatie vereisen met een vector DB of tools.
        raise NotImplementedError("Ollama provider ondersteunt momenteel geen directe document uploads.")

    def delete_chat(self, chat_id: str) -> Dict[str, Any]:
        if chat_id in self.history:
            del self.history[chat_id]
        if chat_id in self.chat_models:
            del self.chat_models[chat_id]
        return {"message": "Chat deleted successfully", "id": chat_id}