from typing import List, Dict, Literal

MessageRole = Literal["user", "assistant", "system", "tool"] # Expandido para tool

class ConversationMemory:
    """Gestiona el historial de la conversación en memoria."""

    def __init__(self, system_prompt: str = None):
        """
        Inicializa la memoria.

        Args:
            system_prompt: Un mensaje opcional para guiar al LLM al inicio.
        """
        self.history: List[Dict[str, str]] = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def add_message(self, role: MessageRole, content: str):
        """
        Añade un mensaje al historial.

        Args:
            role: El rol del mensaje ('user', 'assistant', 'system', 'tool').
            content: El contenido del mensaje.
        """
        if not isinstance(role, str) or not isinstance(content, str):
             raise ValueError("Role y content deben ser strings")
        if role not in ["user", "assistant", "system", "tool"]:
             raise ValueError("Rol inválido. Debe ser 'user', 'assistant', 'system' o 'tool'")

        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """
        Devuelve una copia del historial de conversación actual.
        """
        return list(self.history) # Devuelve una copia para evitar modificación externa

    def clear(self):
        """Limpia el historial de la conversación."""
        # Mantiene el system prompt si existe
        if self.history and self.history[0]["role"] == "system":
             self.history = [self.history[0]]
        else:
            self.history = []