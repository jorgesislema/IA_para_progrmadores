# src/chat/llm_interface.py
import time
import random
import logging
from typing import List, Dict, Iterator, Tuple, Optional

from .memory import ConversationMemory, MessageRole
from ..internet.search import search_google, SEARCH_FUNCTION_SCHEMA
# Usar la nueva función de extracción basada en newspaper
from ..internet.extract import extract_content_from_links
from ..streaming.streamer import stream_message # Para mensajes de estado

log = logging.getLogger(__name__)

class LLMInterface:
    """
    Interfaz (placeholder) para interactuar con un modelo de lenguaje grande (LLM).
    Simula function calling para búsqueda y la generación de respuestas en streaming.
    """
    def __init__(self):
        log.info("Inicializando LLMInterface (Placeholder)...")
        self.available_tools = {
            "buscar_en_google": search_google
        }
        self.tool_schemas = [SEARCH_FUNCTION_SCHEMA]

    def _decide_tool_use(self, user_query: str, history: List[Dict[str, str]]) -> Optional[Dict]:
        """Simula la decisión del LLM sobre si usar una herramienta."""
        keywords = ["buscar", "qué es", "quién es", "dime sobre", "encuentra información", "actualidad", "noticias", "investiga"]
        query_lower = user_query.lower()
        # Añadir contexto: quizás no buscar si la respuesta ya está en el historial reciente? (Lógica compleja para placeholder)
        if any(keyword in query_lower for keyword in keywords):
            log.info("LLMInterface (Placeholder): Decidió usar la herramienta 'buscar_en_google'.")
            return {
                "tool_name": "buscar_en_google",
                "tool_args": {"query": user_query} # Usar el query completo como argumento
            }
        log.info("LLMInterface (Placeholder): Decidió NO usar herramientas.")
        return None

    def _execute_tool(self, tool_call: Dict) -> Optional[Dict]: # Cambiado para devolver siempre Dict o None
        """Ejecuta la herramienta solicitada (solo búsqueda por ahora)."""
        tool_name = tool_call.get("tool_name")
        tool_args = tool_call.get("tool_args", {})
        log.info(f"Ejecutando herramienta solicitada: {tool_name} con args: {tool_args}")

        if tool_name == "buscar_en_google":
            function_to_call = self.available_tools[tool_name]
            try:
                # search_google devuelve List[Dict] o None
                search_api_results = function_to_call(**tool_args)

                if search_api_results is None: # Error en la API
                     log.error("La ejecución de la herramienta 'buscar_en_google' falló (devolvió None).")
                     return {"error": "No se pudo realizar la búsqueda debido a un error interno."}
                elif not search_api_results: # No se encontraron resultados
                     log.warning("La búsqueda no arrojó resultados orgánicos.")
                     return {"links": [], "results_summary": "No se encontraron resultados relevantes."}
                else:
                    # Extraer solo los links para pasarlos a la extracción
                    links = [r['link'] for r in search_api_results if r.get('link')]
                    log.info(f"Herramienta 'buscar_en_google' ejecutada. Encontrados {len(links)} links.")
                    return {"links": links, "results_summary": f"Encontrados {len(search_api_results)} resultados."}

            except Exception as e:
                log.exception(f"Error inesperado ejecutando la herramienta '{tool_name}':")
                return {"error": f"Error inesperado al ejecutar la herramienta: {e}"}
        else:
            log.warning(f"Se solicitó una herramienta desconocida o no implementada: {tool_name}")
            return {"error": f"Herramienta '{tool_name}' desconocida."}


    def _generate_placeholder_response(
        self,
        user_query: str,
        history: List[Dict[str, str]],
        search_context: Optional[str] = None # Renombrado para claridad
    ) -> Iterator[str]:
        """Simula la generación de respuesta del LLM en streaming."""
        log.debug("Generando respuesta placeholder...")
        yield f"Procesando tu consulta: '{user_query[:40]}...'. "
        time.sleep(0.3)

        if search_context:
            yield "\nConsultando la información encontrada en línea... "
            time.sleep(0.5)
            # Simular uso del contexto
            # En un LLM real, este contexto influiría directamente en la respuesta
            context_summary = search_context[:250] # Mostrar un fragmento del contexto recibido
            yield f"\nBasado en: '{context_summary}...'. "
            time.sleep(1)
            yield "\nHe revisado algunas fuentes para responderte. " # Respuesta simulada
        else:
            yield "\nConsultando mi base de conocimiento interna... "
            time.sleep(0.5)
            yield f"\nSobre '{user_query[:30]}...', puedo comentarte que... (respuesta simulada sin búsqueda). "

        time.sleep(0.5)
        yield "\n¿Necesitas algo más?"
        log.debug("Respuesta placeholder generada.")


    def get_response_stream(
        self,
        user_query: str,
        memory: ConversationMemory
    ) -> Tuple[Iterator[str], List[str]]:
        """
        Orquesta la interacción: decide si buscar, busca, extrae y genera respuesta (simulada).

        Returns:
            Un tuple: (generador_de_respuesta_en_stream, lista_de_urls_usadas)
        """
        log.info(f"Procesando query: '{user_query}'")
        current_history = memory.get_history()
        used_urls = []
        search_context_for_llm = None # Texto que se pasaría al LLM

        # 1. Simular decisión de usar herramienta (LLM Call 1 - imaginario)
        tool_decision = self._decide_tool_use(user_query, current_history)

        if tool_decision:
            # 2. Ejecutar la herramienta (búsqueda)
            tool_result = self._execute_tool(tool_decision) # Devuelve Dict o None

            if tool_result and not tool_result.get("error"):
                 search_links = tool_result.get("links", [])
                 if search_links:
                    log.info(f"Búsqueda exitosa, {len(search_links)} links obtenidos. Procediendo a extraer.")
                    # 3. Extraer contenido de los links usando newspaper
                    extracted_data = extract_content_from_links(search_links) # Dict[url, content]

                    if extracted_data:
                        log.info(f"Extracción exitosa para {len(extracted_data)} de {len(search_links)} links.")
                        # 4. Preparar resumen/contexto para el LLM (simulado)
                        search_context_for_llm = "\n\n### Contexto de Fuentes Web:\n"
                        for url, text in extracted_data.items():
                            # Solo incluimos las URLs de las que SÍ se extrajo texto
                            used_urls.append(url)
                            search_context_for_llm += f"\n--- Fuente: {url} ---\n{text[:500]}...\n" # Limitar longitud por fuente
                        search_context_for_llm += "\n### Fin Contexto\n"
                    else:
                        log.warning("La extracción no produjo contenido útil de los links encontrados.")
                        search_context_for_llm = "\nContexto de búsqueda: Se encontraron links pero no se pudo extraer contenido útil de ellos."
                        # Aunque no se extrajo, podríamos listar los links originales si quisiéramos
                        # used_urls = list(search_links) # Descomentar si queremos citar aunque no se extraiga
                 else:
                    log.info("La búsqueda se ejecutó pero no devolvió links.")
                    search_context_for_llm = "\nContexto de búsqueda: La búsqueda no encontró URLs relevantes."
            else:
                # Hubo un error en la búsqueda o la herramienta devolvió un error
                error_msg = tool_result.get("error", "Error desconocido durante la búsqueda.") if tool_result else "La herramienta de búsqueda no devolvió resultado."
                log.error(f"Fallo en la ejecución de la herramienta de búsqueda: {error_msg}")
                search_context_for_llm = f"\nContexto de búsqueda: Falló el intento de buscar información ({error_msg})."


        # 5. Simular generación de respuesta final (LLM Call 2 - imaginario)
        log.info("Generando respuesta final (simulada)...")
        response_generator = self._generate_placeholder_response(
            user_query,
            current_history,
            search_context_for_llm # Pasamos el contexto acumulado (o None)
        )

        log.info(f"Retornando stream de respuesta y {len(used_urls)} URLs.")
        # Devolvemos solo las URLs de las que se extrajo contenido con éxito
        return response_generator, used_urls