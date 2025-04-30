import sys
from dotenv import load_dotenv

# Cargar variables de entorno ANTES de importar otros módulos que las usen
load_dotenv()

# Ahora importar los componentes del chatbot
from chat.memory import ConversationMemory
from chat.llm_interface import LLMInterface
from streaming.streamer import stream_to_console, stream_message
from utils.formatter import format_response_with_references

def main():
    """Función principal para ejecutar el chatbot de consola."""

    # Verificar si la API Key de Serper está cargada (opcional pero útil)
    import os
    if not os.getenv("SERPER_API_KEY"):
        print("ADVERTENCIA: La variable de entorno SERPER_API_KEY no está configurada.")
        print("La funcionalidad de búsqueda en internet no funcionará.")
        # Podrías decidir salir si la búsqueda es esencial:
        # sys.exit("Error: Falta SERPER_API_KEY. Saliendo.")

    # --- Inicialización ---
    # Prompt del sistema opcional para guiar al bot
    system_prompt = "Eres un asistente útil que puede buscar en internet para responder preguntas. Responde de forma concisa y cita tus fuentes si buscas información."
    memory = ConversationMemory(system_prompt=system_prompt)
    llm = LLMInterface() # Usamos nuestro placeholder

    print("--- Chatbot Buscador (v0.1) ---")
    print("Escribe tu pregunta o 'salir' para terminar.")

    # --- Ciclo Principal del Chat ---
    while True:
        try:
            user_input = input("Tú: ")
            if user_input.lower().strip() in ["salir", "quit", "exit"]:
                print("Bot: ¡Hasta luego!")
                break

            if not user_input.strip():
                continue

            # 1. Añadir mensaje del usuario a la memoria
            memory.add_message("user", user_input)

            # 2. Obtener respuesta del LLM (orquesta búsqueda si es necesario)
            # get_response_stream devuelve el iterador y las URLs usadas
            response_stream, used_urls = llm.get_response_stream(user_input, memory)

            # 3. Mostrar respuesta en streaming y recolectarla
            full_response_text = stream_to_console(response_stream)

            # 4. Añadir respuesta completa del asistente a la memoria
            memory.add_message("assistant", full_response_text)

            # 5. Formatear respuesta final con referencias (si las hay)
            # No se imprime directamente aquí, sino que se guarda para el historial
            # La impresión final con referencias se haría fuera del stream_to_console si fuera necesario
            # O modificamos stream_to_console para devolver el texto y luego formatearlo
            # -> Modificamos stream_to_console para que devuelva el texto

            final_output = format_response_with_references(full_response_text, used_urls)

            # Imprimir una separación antes de la próxima entrada del usuario
            print("\n" + "="*80 + "\n")


        except KeyboardInterrupt:
            print("\nBot: Interrupción detectada. ¡Adiós!")
            break
        except Exception as e:
            print(f"\nError inesperado en el ciclo principal: {e}")
            # Podrías querer limpiar la memoria o intentar recuperarte
            # memory.clear() # Opcional: limpiar memoria en caso de error grave

if __name__ == "__main__":
    main()