# src/main.py (Inicio del archivo)
import sys
import logging
import os
from dotenv import load_dotenv

# --- Configuración del Logging ---
logging.basicConfig(
    level=logging.INFO, # Cambia a logging.DEBUG para ver más detalles
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout) # Enviar logs a la consola
        # Opcional: Añadir un FileHandler para guardar logs en un archivo
        # logging.FileHandler("chatbot.log")
    ]
)
# Obtener un logger específico para este módulo
log = logging.getLogger(__name__)
# Silenciar logs muy verbosos de librerías de terceros si es necesario
# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("newspaper").setLevel(logging.WARNING) # O INFO si quieres ver sus mensajes

# Cargar variables de entorno ANTES de importar otros módulos que las usen
log.info("Cargando variables de entorno...")
load_dotenv()
if not os.getenv("SERPER_API_KEY"):
    log.warning("La variable de entorno SERPER_API_KEY no está configurada.")
else:
    log.info("SERPER_API_KEY cargada.")


# Ahora importar los componentes del chatbot
from src.chat.memory import ConversationMemory # Ajusta la ruta si es necesario
from src.chat.llm_interface import LLMInterface
from src.streaming.streamer import stream_to_console, stream_message
from src.utils.formatter import format_response_with_references

# ... (resto del main.py sin cambios hasta el final)

def main():
    """Función principal para ejecutar el chatbot de consola."""
    log.info("Iniciando el Chatbot Buscador...")

    # --- Inicialización ---
    system_prompt = "Eres un asistente útil que puede buscar en internet para responder preguntas. Responde de forma concisa y cita tus fuentes si buscas información."
    memory = ConversationMemory(system_prompt=system_prompt)
    llm = LLMInterface()
    log.info("Componentes inicializados (Memoria, LLM Interface).")

    print("\n--- Chatbot Buscador (v0.2 - Mejorado) ---")
    print("Escribe tu pregunta o 'salir' para terminar.")

    # --- Ciclo Principal del Chat ---
    while True:
        try:
            user_input = input("Tú: ")
            if user_input.lower().strip() in ["salir", "quit", "exit"]:
                log.info("Comando de salida recibido. Terminando.")
                print("Bot: ¡Hasta luego!")
                break

            if not user_input.strip():
                continue

            log.info(f"Usuario ingresó: '{user_input}'")

            # 1. Añadir mensaje del usuario a la memoria
            memory.add_message("user", user_input)

            # 2. Obtener respuesta del LLM (orquesta búsqueda si es necesario)
            log.info("Obteniendo respuesta del LLM Interface...")
            response_stream, used_urls = llm.get_response_stream(user_input, memory)
            log.info(f"LLM Interface devolvió {len(used_urls)} URLs usadas.")

            # 3. Mostrar respuesta en streaming y recolectarla
            full_response_text = stream_to_console(response_stream)
            log.debug(f"Texto completo de la respuesta recolectada: {full_response_text[:100]}...") # Log corto

            # 4. Añadir respuesta completa del asistente a la memoria
            memory.add_message("assistant", full_response_text)
            log.info("Respuesta del asistente añadida a la memoria.")

            # 5. Formatear respuesta final con referencias (si las hay)
            final_output = format_response_with_references(full_response_text, used_urls)

            # Imprimir una separación antes de la próxima entrada del usuario
            print("\n" + "="*80 + "\n") # Separador visual, no log

        except KeyboardInterrupt:
            log.info("Interrupción de teclado detectada. Terminando.")
            print("\nBot: Interrupción detectada. ¡Adiós!")
            break
        except Exception as e:
            log.exception("Error inesperado en el ciclo principal:") # Log completo del error
            print(f"\nError inesperado. Por favor, revisa los logs. ({e})")
            # Considera si quieres continuar o salir en caso de error grave
            # break

if __name__ == "__main__":
    main()