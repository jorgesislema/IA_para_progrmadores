import unittest
from src.chat.memory import ConversationMemory

class TestMemory(unittest.TestCase):

    def test_add_and_get_message(self):
        memory = ConversationMemory()
        memory.add_message("user", "Hola")
        memory.add_message("assistant", "Hola! ¿Cómo puedo ayudarte?")
        history = memory.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], {"role": "user", "content": "Hola"})
        self.assertEqual(history[1], {"role": "assistant", "content": "Hola! ¿Cómo puedo ayudarte?"})

    def test_system_prompt(self):
        prompt = "Eres un bot."
        memory = ConversationMemory(system_prompt=prompt)
        history = memory.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], {"role": "system", "content": prompt})
        memory.add_message("user", "Test")
        self.assertEqual(len(memory.get_history()), 2)

    def test_clear_memory(self):
         prompt = "System prompt"
         memory = ConversationMemory(system_prompt=prompt)
         memory.add_message("user", "Pregunta")
         memory.add_message("assistant", "Respuesta")
         self.assertEqual(len(memory.get_history()), 3)
         memory.clear()
         history = memory.get_history()
         # Debe mantener el system prompt
         self.assertEqual(len(history), 1)
         self.assertEqual(history[0], {"role": "system", "content": prompt})

if __name__ == '__main__':
    unittest.main()