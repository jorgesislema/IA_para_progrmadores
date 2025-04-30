# tests/test_llm_interface.py
import unittest
from unittest.mock import patch, MagicMock, PropertyMock # PropertyMock puede no ser necesaria aquí
# Importar directamente LLMInterface para usar patch.object
from src.chat.llm_interface import LLMInterface
from src.chat.memory import ConversationMemory

class TestLLMInterfacePlaceholder(unittest.TestCase):

    def setUp(self):
        # Se ejecuta antes de cada prueba
        # Crear instancias nuevas para cada prueba para evitar contaminación
        self.memory = ConversationMemory()
        # Instanciar LLMInterface dentro de setUp si no guarda estado entre llamadas
        # o si queremos asegurar un estado limpio. Si LLMInterface tuviera estado
        # que debe persistir entre métodos (poco común para esta interfaz),
        # se podría instanciar fuera o como variable de clase.
        # Para este placeholder, instanciar aquí está bien.
        self.llm_interface = LLMInterface()


    # Mockear _execute_tool en lugar de search_google directamente
    # Mantener el mock de extract_content_from_links
    @patch('src.chat.llm_interface.extract_content_from_links')
    @patch.object(LLMInterface, '_execute_tool') # Mockear el método de la instancia
    def test_response_with_search_triggered(self, mock_execute_tool, mock_extract):
        # Forzar la decisión de buscar (simulando palabras clave)
        user_query = "buscar información sobre Python"
        self.memory.add_message("user", user_query)

        # Simular que _execute_tool devuelve un resultado de búsqueda exitoso (con links)
        mock_search_result_data = {
            "links": ["https://python.org", "https://wiki.python.org"],
            "results_summary": "Encontrados 2 resultados."
        }
        mock_execute_tool.return_value = mock_search_result_data

        # Simular resultado de extracción (igual que antes)
        mock_extracted_data = {
            "https://python.org": "Official Python website content snippet...",
            "https://wiki.python.org": "Python wiki content snippet..."
        }
        mock_extract.return_value = mock_extracted_data

        # Ejecutar el método
        response_stream, used_urls = self.llm_interface.get_response_stream(user_query, self.memory)
        # Consumir el generador para obtener la respuesta completa y asegurar ejecución
        full_response = "".join(list(response_stream))

        # Verificaciones
        # 1. Verificar que _execute_tool fue llamado (implica que _decide_tool_use funcionó)
        mock_execute_tool.assert_called_once()
        # 2. Verificar que la extracción fue llamada con los links devueltos por _execute_tool
        mock_extract.assert_called_once_with(["https://python.org", "https://wiki.python.org"])
        # 3. Verificar que las URLs usadas son correctas
        self.assertEqual(used_urls, ["https://python.org", "https://wiki.python.org"])
        # 4. Verificar que la respuesta simulada indica que usó contexto (ajusta si cambia el placeholder)
        self.assertIn("Consultando la información encontrada", full_response)
        # Verificar que el contexto se usa (puede ser sensible a cambios en el placeholder)
        self.assertIn("Fuente: https://python.org", full_response)


    @patch('src.chat.llm_interface.extract_content_from_links')
    @patch.object(LLMInterface, '_execute_tool') # Mockear también _execute_tool para aislar
    @patch.object(LLMInterface, '_decide_tool_use') # Mockear también _decide_tool_use
    def test_response_without_search_triggered(self, mock_decide_tool, mock_execute_tool, mock_extract):
        # Usar un query que NO active la búsqueda simulada
        user_query = "Hola cómo estás"
        self.memory.add_message("user", user_query)

        # Forzar que la decisión sea NO usar herramientas
        mock_decide_tool.return_value = None

        # Ejecutar el método
        response_stream, used_urls = self.llm_interface.get_response_stream(user_query, self.memory)
        full_response = "".join(list(response_stream))

        # Verificaciones
        mock_decide_tool.assert_called_once() # Verificar que se consultó la decisión
        mock_execute_tool.assert_not_called() # No debería llamarse a execute
        mock_extract.assert_not_called()      # Ni a extract
        self.assertEqual(used_urls, [])       # Lista de URLs vacía
        # Verificar que la respuesta simulada indica que NO usó búsqueda
        self.assertIn("Consultando mi base de conocimiento interna", full_response) # <-- Cadena Corregida
        self.assertNotIn("Contexto de Fuentes Web", full_response) # Asegurar que no hay contexto web


    @patch('src.chat.llm_interface.extract_content_from_links') # Mockear para que no se ejecute
    @patch.object(LLMInterface, '_execute_tool') # Mockear para controlar su salida
    @patch.object(LLMInterface, '_decide_tool_use') # Mockear para forzar la decisión
    def test_search_fails(self, mock_decide_tool, mock_execute_tool, mock_extract):
        # Forzar decisión de buscar
        user_query = "buscar algo raro"
        self.memory.add_message("user", user_query)
        # Asegurarse de que _decide_tool_use sí devuelva una decisión de buscar
        mock_decide_tool.return_value = {"tool_name": "buscar_en_google", "tool_args": {"query": user_query}}

        # Simular que la ejecución de la herramienta falla devolviendo un dict con error
        mock_execute_tool.return_value = {"error": "Error simulado al buscar."} # <-- Corregido: Devuelve dict

        # Ejecutar
        response_stream, used_urls = self.llm_interface.get_response_stream(user_query, self.memory)
        full_response = "".join(list(response_stream))

        # Verificaciones
        mock_decide_tool.assert_called_once()
        mock_execute_tool.assert_called_once() # Se intentó ejecutar la herramienta
        mock_extract.assert_not_called()       # No se debió llamar a la extracción si falló la búsqueda
        self.assertEqual(used_urls, [])       # No se usaron URLs si falló la búsqueda/herramienta
        # Verificar que el mensaje de error simulado (o uno genérico) esté en la respuesta placeholder
        self.assertIn("Falló el intento de buscar", full_response)
        self.assertIn("Error simulado al buscar", full_response) # Verificar texto del error simulado


if __name__ == '__main__':
    unittest.main()

# --- NO DEBE HABER NADA MÁS AQUÍ (especialmente clases TestSearchMocked o TestSearchIntegration) ---