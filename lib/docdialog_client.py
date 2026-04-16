# docdialog_client.py
import requests
from typing import Dict, Any, Optional, List, Union
from lib.base_client import BaseLLMClient

BASE_URL = "https://docdialog-data-apim.azure-api.net/dd-chat/v1"


class DocumentDialogueClient(BaseLLMClient):
    def __init__(self, access_token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
        })

    # ---------- Models ----------

    def list_models(self) -> Dict[str, Any]:
        """
        Normaliseer /models response naar:
        {
          "models": [...],
          "default": <id> | None
        }
        """
        resp = self.session.get(f"{BASE_URL}/models")
        resp.raise_for_status()
        data: Union[Dict[str, Any], List[Dict[str, Any]]] = resp.json()

        if isinstance(data, list):
            return {"models": data, "default": None}
        elif isinstance(data, dict):
            return {
                "models": data.get("models", []),
                "default": data.get("default"),
            }
        else:
            raise ValueError(f"Onverwacht /models response type: {type(data)}")

    # ---------- Chats ----------

    def list_chats(self) -> Dict[str, Any]:
        resp = self.session.get(f"{BASE_URL}/chats")
        resp.raise_for_status()
        return resp.json()

    def create_chat(
        self,
        *,
        persona_id: Optional[str] = None,
        extension_id: Optional[str] = None,
        model: Optional[str] = None,
    ) -> str:
        payload: Dict[str, Any] = {}
        if persona_id:
            payload["personaId"] = persona_id
        if extension_id:
            payload["extensionId"] = extension_id
        if model:
            payload["model"] = model

        resp = self.session.post(f"{BASE_URL}/chats", json=payload)
        resp.raise_for_status()
        return resp.json()["id"]

    def rename_chat(self, chat_id: str, name: str) -> Dict[str, Any]:
        payload = {"name": name}
        resp = self.session.patch(f"{BASE_URL}/chats/{chat_id}", json=payload)
        resp.raise_for_status()
        return resp.json()

    def delete_chat(self, chat_id: str) -> Dict[str, Any]:
        resp = self.session.delete(f"{BASE_URL}/chats/{chat_id}")
        resp.raise_for_status()
        return resp.json()

    # ---------- Messages ----------

    def get_messages(self, chat_id: str) -> List[Dict[str, Any]]:
        resp = self.session.get(f"{BASE_URL}/chats/{chat_id}/messages")
        resp.raise_for_status()
        data = resp.json()
        return data.get("messages", []) if isinstance(data, dict) else data

    def send_message(
        self,
        chat_id: str,
        text: str,
        *,
        model: Optional[str] = None,
        persist: bool = True,
        multi_modal_image: Optional[str] = None,
    ) -> Dict[str, Any]:
        url = f"{BASE_URL}/chats/{chat_id}/messages"
        payload: Dict[str, Any] = {"text": text}

        if not persist:
            payload["persist"] = "false"
        if model:
            payload["model"] = model
        if multi_modal_image:
            payload["multiModalImage"] = multi_modal_image

        headers = {"Content-Type": "application/json"}
        resp = self.session.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()

    # ---------- Documents ----------

    def list_documents(self, chat_id: str) -> Dict[str, Any]:
        resp = self.session.get(f"{BASE_URL}/chats/{chat_id}/documents")
        resp.raise_for_status()
        return resp.json()

    def upload_document(self, chat_id: str, file_path: str) -> Dict[str, Any]:
        url = f"{BASE_URL}/chats/{chat_id}/documents"
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}
            resp = self.session.post(url, files=files)
        resp.raise_for_status()
        return resp.json()

    # ---------- Personas / Prompts / Extensions ----------

    def list_personas(self) -> Dict[str, Any]:
        resp = self.session.get(f"{BASE_URL}/personas")
        resp.raise_for_status()
        return resp.json()

    def list_prompts(self) -> Dict[str, Any]:
        resp = self.session.get(f"{BASE_URL}/prompts")
        resp.raise_for_status()
        return resp.json()

    def list_extensions(self) -> Dict[str, Any]:
        resp = self.session.get(f"{BASE_URL}/extensions")
        resp.raise_for_status()
        return resp.json()
