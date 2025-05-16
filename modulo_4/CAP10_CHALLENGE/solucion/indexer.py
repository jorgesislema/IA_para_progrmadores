"""
Script para generar el índice de la base de conocimientos utilizando FAISS y embeddings.
Este script lee los archivos de la carpeta knowledge_base, genera embeddings utilizando 
el modelo sentence-transformers/all-MiniLM-L6-v2 y los almacena en un índice FAISS.
"""

import os
import logging
from typing import List, Dict, Any

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rutas
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base")
INDEX_DIR = "./index"

def load_documents() -> List[Dict[str, Any]]:
    """
    Carga todos los documentos de texto de la carpeta knowledge_base.
    
    Returns:
        List[Dict[str, Any]]: Lista de documentos cargados
    """
    logger.info(f"Cargando documentos desde {KNOWLEDGE_BASE_DIR}")
    try:
        loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()
        logger.info(f"Se cargaron {len(documents)} documentos")
        return documents
    except Exception as e:
        logger.error(f"Error al cargar documentos: {e}")
        raise

def split_documents(documents):
    """
    Divide los documentos en chunks más pequeños para un mejor procesamiento.
    
    Args:
        documents: Lista de documentos a dividir
        
    Returns:
        List: Lista de documentos divididos
    """
    logger.info("Dividiendo documentos en chunks")
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def create_index(documents):
    """
    Crea un índice FAISS a partir de los documentos proporcionados.
    
    Args:
        documents: Lista de documentos para indexar
        
    Returns:
        FAISS: El índice FAISS creado
    """
    logger.info("Creando embeddings e índice FAISS")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

def save_index(vectorstore):
    """
    Guarda el índice FAISS en disco.
    
    Args:
        vectorstore: El índice FAISS a guardar
    """
    logger.info(f"Guardando índice en {INDEX_DIR}")
    os.makedirs(INDEX_DIR, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)
    logger.info("Índice guardado exitosamente")

def main():
    """
    Función principal que ejecuta el proceso de indexación.
    """
    logger.info("Iniciando proceso de indexación")
    try:
        # Cargar documentos
        documents = load_documents()
        
        # Dividir documentos en chunks
        chunks = split_documents(documents)
        
        # Crear índice FAISS
        vectorstore = create_index(chunks)
        
        # Guardar índice
        save_index(vectorstore)
        
        logger.info("Proceso de indexación completado exitosamente")
    except Exception as e:
        logger.error(f"Error en el proceso de indexación: {e}")
        raise

if __name__ == "__main__":
    main()
