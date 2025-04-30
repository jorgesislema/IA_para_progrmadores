#LIBRERIAS
import sys
import time
from typing import Iterator

def stream_to_console(stream: Iterator[str], delay: float = 0.01):
    """
    Imprimimos los fragmentos de un stream a la consola.

    Args:
        stream: Un iterador que produce fragmentos de texto (str).
        delay: Un pequeño retraso opcional entre fragmentos para visualización.
    """
    collected_response = ""
    print("Bot: ", end="")
    sys.stdout.flush()
    try:
        for chunk in stream:
            print(chunk, end="")
            sys.stdout.flush()
            collected_response += chunk
            if delay > 0:
                time.sleep(delay)
        print() # Nueva línea al final de la respuesta completa
    except Exception as e:
        print(f"\nError durante el streaming: {e}")
    finally:
        sys.stdout.flush()
    return collected_response

def stream_message(message: str):
    """Imprime un mensaje completo a la consola (útil para mensajes de estado)."""
    print(message)
    sys.stdout.flush()