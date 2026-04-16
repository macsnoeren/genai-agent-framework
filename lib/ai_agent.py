from typing import Dict, Any, Optional, List, Union
import logging
from lib.base_client import BaseLLMClient

class AIAgent:
    """
    Een modulaire AI-agent die via een provider taken plant, uitvoert en verifieert.
    """
    def __init__(self, client: BaseLLMClient, default_model_id: Optional[str] = None, default_prompt: Optional[str] = None):
        """
        Initialiseert de AIAgent.

        Args:
            client (BaseLLMClient): Een instantie van een LLM client provider.
            default_model_id (Optional[str]): De ID van het standaardmodel om te gebruiken.
            default_prompt (Optional[str]): Een standaard prompt die aan elke taakbeschrijving wordt voorafgegaan.
        """
        self.client = client
        self._current_chat_id: Optional[str] = None
        self.default_prompt = default_prompt
        self.default_model_id = default_model_id

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        # Definieer een aparte logger voor de agent's interne stappen
        agent_logger = logging.getLogger('RWEAIAgent')
        agent_logger.setLevel(logging.INFO) # Kan op DEBUG gezet worden voor meer details
        self.logger = agent_logger

    def list_models(self) -> List[Dict[str, Any]]:
        """
        Haalt een lijst op van beschikbare modellen.

        Returns:
            List[Dict[str, Any]]: Een lijst met modelinformatie.
        """
        models_info = self.client.list_models()
        if isinstance(models_info, list):
            return models_info
        return models_info.get("models", []) if isinstance(models_info, dict) else []

    def create_chat(self, model_id: Optional[str] = None) -> str:
        """
        Maakt een nieuwe chat aan.

        Args:
            model_id (Optional[str]): De ID van het model om voor deze chat te gebruiken.
                                      Indien None, wordt self.default_model_id gebruikt, of het API-standaard.

        Returns:
            str: De ID van de nieuw aangemaakte chat.
        """
        chosen_model = model_id if model_id else self.default_model_id
        self._current_chat_id = self.client.create_chat(model=chosen_model)
        return self._current_chat_id

    def upload_file(self, file_path: str, chat_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Uploadt een bestand naar de chat voor analyse.
        """
        target_chat_id = chat_id if chat_id else self._current_chat_id
        if not target_chat_id:
            raise ValueError("Geen actieve chat. Roep 'create_chat()' aan.")
        
        self.logger.info(f"Bestand uploaden: {file_path}")
        return self.client.upload_document(target_chat_id, file_path)

    def send_message(self, message_text: str, chat_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Verstuurt een bericht naar de chat.

        Args:
            message_text (str): De tekst van het bericht.
            chat_id (Optional[str]): De ID van de chat om het bericht naar te sturen.
                                     Indien None, wordt de laatst aangemaakte chat gebruikt.

        Returns:
            Dict[str, Any]: Het responsbericht van de AI.

        Raises:
            ValueError: Als er geen chat_id is opgegeven en er geen actieve chat is.
        """
        target_chat_id = chat_id if chat_id else self._current_chat_id
        if not target_chat_id:
            raise ValueError("Geen chat_id opgegeven en geen actieve chat beschikbaar. Roep 'create_chat()' aan.")

        response = self.client.send_message(target_chat_id, text=message_text)
        return response

    def get_current_chat_id(self) -> Optional[str]:
        """
        Geeft de ID van de actieve chat terug.
        """
        return self._current_chat_id

    def _plan(self, task_description: str) -> str:
        """
        Gebruikt de LLM om een plan te genereren voor de gegeven taak.
        """
        self.logger.info(f"Agent plant: '{task_description}'")
        # Prompt de LLM om een plan te maken
        plan_prompt_template = (
            f"Je bent een AI-planner. Gegeven de volgende taak, formuleer een gedetailleerd stappenplan om deze te voltooien. "
            f"Focus op de logische stappen die je moet nemen om het gewenste resultaat te bereiken. "
            f"Antwoord alleen met het plan, zonder verdere uitleg. Begin met 'Plan:' "
            f"Taak: {task_description}"
        )
        plan_prompt = (f"{self.default_prompt}\n" if self.default_prompt else "") + plan_prompt_template
        response = self.send_message(plan_prompt)
        plan_content = response.get("content", "").strip()
        self.logger.info(f"Plan gegenereerd: {plan_content}")
        return plan_content

    def _execute(self, plan: str) -> Dict[str, Any]:
        """
        Gebruikt de LLM om het gegenereerde plan uit te voeren.
        """
        self.logger.info(f"Agent voert plan uit: {plan}")
        # Prompt de LLM om het plan uit te voeren
        execute_prompt = (
            f"Je bent een AI-uitvoerder. Gegeven het volgende plan, voer de benodigde acties uit en presenteer het resultaat van je uitvoering. "
            f"Plan: {plan}"
        )
        response = self.send_message(execute_prompt)
        execution_result = response.get("content", "").strip()
        self.logger.info(f"Uitvoeringsresultaat: {execution_result}")
        return response # Return full response to potentially include metadata if needed later

    def _verify(self, original_task: str, execution_result: Dict[str, Any]) -> bool:
        """
        Gebruikt de LLM om te verifiëren of het uitvoeringsresultaat voldoet aan de oorspronkelijke taak.
        """
        result_content = execution_result.get('content', '')
        self.logger.info(f"Agent verifieert. Oorspronkelijke taak: '{original_task}'. Resultaat: '{result_content}'")
        # Prompt de LLM om de uitvoering te verifiëren
        verify_prompt = (
            f"Je bent een AI-verificatie-assistent. Beoordeel of het volgende resultaat de oorspronkelijke taak voldoende beantwoordt en oplost. "
            f"Antwoord met 'JA' als het voldoende is, anders met 'NEE', gevolgd door een korte reden voor de afkeuring. "
            f"Oorspronkelijke taak: {original_task}\n"
            f"Resultaat: {result_content}"
        )
        response = self.send_message(verify_prompt)
        verification_output = response.get("content", "").strip().upper()
        is_verified = verification_output.startswith("JA")
        self.logger.info(f"Verificatie resultaat: {verification_output}. Voldoende: {is_verified}")
        return is_verified

    def run_agent(self, task_description: str, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Voert een taak uit met behulp van de plan -> execute -> verify loop.

        Args:
            task_description (str): De beschrijving van de taak die de agent moet uitvoeren.
            max_iterations (int): Het maximale aantal pogingen om de taak te voltooien.

        Returns:
            Dict[str, Any]: Het uiteindelijke responsbericht van de AI na uitvoering.
        """
        self.logger.info(f"Agent gestart met taak: '{task_description}'")
        current_plan = ""
        final_result = {}

        for i in range(max_iterations):
            self.logger.info(f"--- Iteratie {i+1}/{max_iterations} ---")
            current_plan = self._plan(task_description if not current_plan else f"Besteed aandacht aan de vorige feedback en pas het plan aan om de taak te voltooien: {task_description}. Vorig plan: {current_plan}")
            execution_response = self._execute(current_plan)
            final_result = execution_response # Bewaar de laatste uitvoering als resultaat

            if self._verify(task_description, execution_response):
                self.logger.info(f"Taak succesvol voltooid in {i+1} iteraties.")
                return final_result
            else:
                self.logger.warning("Verificatie mislukt. Agent probeert opnieuw met aangepast plan.")
                # Het volgende plan zal rekening houden met de feedback via de prompt

        self.logger.error(f"Taak niet succesvol voltooid na {max_iterations} iteraties.")
        return final_result # Return het laatste resultaat, zelfs als het niet geverifieerd is.
