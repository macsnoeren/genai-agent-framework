from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseLLMClient(ABC):
    """
    Abstracte basisklasse voor LLM providers.
    """
    
    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_chat(self, model: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def send_message(self, chat_id: str, text: str, model: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def upload_document(self, chat_id: str, file_path: str) -> Dict[str, Any]:
        """
        Uploadt een document naar een specifieke chat.
        """
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> Dict[str, Any]:
        """
        Verwijdert een chat sessie.
        """
        pass