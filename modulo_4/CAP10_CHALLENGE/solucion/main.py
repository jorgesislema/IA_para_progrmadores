"""
Script principal para el Sistema de Atención al Cliente Automatizado con LangChain.

Este sistema procesa solicitudes de clientes y decide el método más apropiado para responder,
ya sea consultando una base de datos, una base de conocimientos o utilizando el conocimiento
integrado en un modelo de lenguaje de gran escala (LLM).
"""

import os
import csv
import logging
from typing import Dict, List, Optional, Any

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import RouterOutputParser
from langchain.schema.language_model import BaseLanguageModel

# Importar los diferentes proveedores de LLM
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    
try:
    from langchain_mistralai import ChatMistralAI
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False
    
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Importación condicional de claves API
try:
    from config_api import API_KEYS
except ImportError:
    API_KEYS = {
        "openai": "",
        "google": "",
        "mistral": "",
        "groq": ""
    }

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rutas y configuraciones
CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saldos.csv")
INDEX_DIR = "./index"

# Modelos de LLM disponibles
LLM_MODELS = []

if OPENAI_AVAILABLE:
    LLM_MODELS.append({"id": "1", "name": "OpenAI (GPT)", "key": "openai", "class": ChatOpenAI, "available": True})
else:
    LLM_MODELS.append({"id": "1", "name": "OpenAI (GPT)", "key": "openai", "class": None, "available": False})

if GOOGLE_AVAILABLE:
    LLM_MODELS.append({"id": "2", "name": "Google (Gemini)", "key": "google", "class": ChatGoogleGenerativeAI, "available": True})
else:
    LLM_MODELS.append({"id": "2", "name": "Google (Gemini)", "key": "google", "class": None, "available": False})

if MISTRAL_AVAILABLE:
    LLM_MODELS.append({"id": "3", "name": "Mistral AI", "key": "mistral", "class": ChatMistralAI, "available": True})
else:
    LLM_MODELS.append({"id": "3", "name": "Mistral AI", "key": "mistral", "class": None, "available": False})

if GROQ_AVAILABLE:
    LLM_MODELS.append({"id": "4", "name": "Groq", "key": "groq", "class": ChatGroq, "available": True})
else:
    LLM_MODELS.append({"id": "4", "name": "Groq", "key": "groq", "class": None, "available": False})


def select_model() -> Optional[Dict]:
    """
    Muestra un menú para seleccionar el modelo LLM y configurar la API key.
    
    Returns:
        Optional[Dict]: Información del modelo seleccionado o None si no se pudo seleccionar.
    """
    print("\n=== Selección de Modelo de Lenguaje ===")
    print("Seleccione el modelo de IA que desea utilizar:")
    
    available_models = []
    for model in LLM_MODELS:
        status = "✓ Instalado" if model["available"] else "✗ No instalado"
        print(f"{model['id']}. {model['name']} ({status})")
        if model["available"]:
            available_models.append(model["id"])
    
    if not available_models:
        logger.error("No hay modelos disponibles. Instale al menos una biblioteca de LLM.")
        return None
    
    while True:
        choice = input("\nIngrese el número del modelo (o 'q' para salir): ")
        
        if choice.lower() == 'q':
            return None
        
        if choice not in [m["id"] for m in LLM_MODELS]:
            print("Opción no válida. Intente de nuevo.")
            continue
        
        selected = next(m for m in LLM_MODELS if m["id"] == choice)
        
        if not selected["available"]:
            print(f"El modelo {selected['name']} no está instalado. Instale la biblioteca correspondiente.")
            continue
        
        api_key = API_KEYS.get(selected["key"], "")
        
        # Solicitar API key si no está configurada
        if not api_key:
            print(f"\nNecesita configurar la API key para {selected['name']}.")
            api_key = input(f"Ingrese su {selected['name']} API key: ")
            
            # Guardar en la variable global de entorno
            os.environ[f"{selected['key'].upper()}_API_KEY"] = api_key
            
            # Actualizar el diccionario de API keys
            API_KEYS[selected["key"]] = api_key
        
        print(f"\nSeleccionado: {selected['name']}")
        return selected


def create_llm_instance(model_info: Dict) -> BaseLanguageModel:
    """
    Crea una instancia del modelo LLM seleccionado.
    
    Args:
        model_info (Dict): Información del modelo seleccionado.
    
    Returns:
        BaseLanguageModel: Instancia del modelo de lenguaje.
    """
    model_class = model_info["class"]
    model_key = model_info["key"]
    api_key = API_KEYS.get(model_key, "")
    
    if model_key == "openai":
        return model_class(temperature=0, api_key=api_key, model="gpt-3.5-turbo")
    elif model_key == "google":
        return model_class(temperature=0, google_api_key=api_key, model="gemini-pro")
    elif model_key == "mistral":
        return model_class(temperature=0, mistral_api_key=api_key, model="mistral-small-latest")
    elif model_key == "groq":
        return model_class(temperature=0, api_key=api_key, model="llama3-8b-8192")
    else:
        raise ValueError(f"Modelo no soportado: {model_info['name']}")


class CustomerSupportSystem:
    """
    Sistema de Atención al Cliente Automatizado que procesa solicitudes y las enruta al flujo apropiado.
    """
    
    def __init__(self, llm: BaseLanguageModel):
        """
        Inicializa el sistema cargando los recursos necesarios.
        
        Args:
            llm (BaseLanguageModel): Modelo de lenguaje a utilizar.
        """
        self.balance_data = self._load_balance_data()
        self.vectorstore = self._load_vector_store()
        self.llm = llm
        self.router_chain = self._setup_router_chain()
        
    def _load_balance_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Carga los datos de balance desde el archivo CSV.
        
        Returns:
            Dict[str, Dict[str, Any]]: Diccionario con IDs de cédula como claves y datos del cliente como valores.
        """
        logger.info(f"Cargando datos de balance desde {CSV_FILE_PATH}")
        balance_data = {}
        
        try:
            with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    balance_data[row['ID_Cedula']] = {
                        'Nombre': row['Nombre'],
                        'Balance': float(row['Balance'])
                    }
            logger.info(f"Se cargaron datos de {len(balance_data)} clientes")
            return balance_data
        except Exception as e:
            logger.error(f"Error al cargar datos de balance: {e}")
            return {}
            
    def _load_vector_store(self) -> Optional[FAISS]:
        """
        Carga el almacén de vectores FAISS desde el directorio de índice.
        
        Returns:
            Optional[FAISS]: El almacén de vectores FAISS o None si no se puede cargar.
        """
        logger.info(f"Cargando índice de vectores desde {INDEX_DIR}")
        
        try:
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
            logger.info("Índice de vectores cargado exitosamente")
            return vectorstore
        except Exception as e:
            logger.error(f"Error al cargar el índice de vectores: {e}")
            logger.warning("Ejecute el script indexer.py para generar el índice")
            return None

    def _setup_router_chain(self):
        """
        Configura la cadena de enrutamiento para decidir cómo procesar cada solicitud.
        
        Returns:
            LLMChain: La cadena de enrutamiento configurada con un analizador de salida.
        """
        logger.info("Configurando cadena de enrutamiento")
        
        # Definir las rutas posibles
        destinations = [
            {"name": "consulta_balance", "description": "Consultas sobre el balance o saldo de una cuenta bancaria específica, utilizando un ID de cédula"},
            {"name": "info_bancaria", "description": "Preguntas sobre procesos bancarios como abrir cuentas, solicitar tarjetas o realizar transferencias"},
            {"name": "general", "description": "Preguntas generales que no requieren consultar bases de datos o conocimientos específicos"}
        ]
        
        # Convertir la lista de destinos a un formato de string para el prompt
        destinations_str = "\n".join([f"{d['name']}: {d['description']}" for d in destinations])
        
        # Crear el prompt de enrutamiento
        router_template = """
        Tu tarea es analizar la consulta del usuario y determinar la mejor categoría para procesarla.
        
        Las categorías disponibles son:
        {destinations}
        
        Consulta del usuario: {input}
        
        Respuesta en formato JSON: {{"destination": "NOMBRE_DE_LA_CATEGORÍA"}}
        """
        
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            partial_variables={"destinations": destinations_str}
        )
        
        # Crear la cadena de enrutamiento con un analizador de salida adecuado
        router_chain = LLMChain(
            llm=self.llm,
            prompt=router_prompt,
            output_parser=RouterOutputParser()
        )
        
        return router_chain
    
    def _process_balance_query(self, query: str) -> str:
        """
        Procesa una consulta de balance extrayendo el ID de cédula y buscando la información correspondiente.
        
        Args:
            query (str): La consulta del usuario.
            
        Returns:
            str: Respuesta con la información de balance.
        """
        logger.info("Procesando consulta de balance")
        
        # Extraer ID de cédula de la consulta
        prompt = PromptTemplate(
            template="""
            Tu tarea es extraer el ID de cédula (formato V-XXXXXXXX) de la siguiente consulta:
            
            {query}
            
            Solo devuelve el ID de cédula en formato V-XXXXXXXX, sin texto adicional.
            Si no hay un ID de cédula válido, responde con "NO_ID".
            """,
            input_variables=["query"]
        )
        
        extraction_chain = LLMChain(llm=self.llm, prompt=prompt)
        extracted_id = extraction_chain.run(query=query).strip()
        
        if extracted_id == "NO_ID" or extracted_id not in self.balance_data:
            return "Lo siento, no puedo encontrar información para ese ID de cédula. Por favor, verifica si el ID es correcto."
        
        client_data = self.balance_data[extracted_id]
        return f"El cliente {client_data['Nombre']} (ID: {extracted_id}) tiene un balance de ${client_data['Balance']:.2f}."
    
    def _process_knowledge_query(self, query: str) -> str:
        """
        Procesa una consulta de conocimiento bancario utilizando la base de conocimientos indexada.
        
        Args:
            query (str): La consulta del usuario.
            
        Returns:
            str: Respuesta generada a partir de la base de conocimientos.
        """
        logger.info("Procesando consulta de conocimiento bancario")
        
        if not self.vectorstore:
            return "Lo siento, la base de conocimientos no está disponible en este momento. Por favor, asegúrate de ejecutar el script indexer.py primero."
        
        # Buscar documentos relevantes
        docs = self.vectorstore.similarity_search(query, k=2)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generar respuesta
        prompt = PromptTemplate(
            template="""
            Eres un asistente bancario experto de BANCO HENRY. Usa la siguiente información para responder a la pregunta del cliente.
            
            Información:
            {context}
            
            Pregunta del cliente:
            {query}
            
            Tu respuesta debe ser profesional, clara y basada solo en la información proporcionada.
            Si la información proporcionada no es suficiente para responder, indícalo educadamente.
            """,
            input_variables=["context", "query"]
        )
        
        knowledge_chain = LLMChain(llm=self.llm, prompt=prompt)
        return knowledge_chain.run(context=context, query=query)
    
    def _process_general_query(self, query: str) -> str:
        """
        Procesa una consulta general utilizando el conocimiento del LLM.
        
        Args:
            query (str): La consulta del usuario.
            
        Returns:
            str: Respuesta generada por el LLM.
        """
        logger.info("Procesando consulta general")
        
        prompt = PromptTemplate(
            template="""
            Eres un asistente bancario profesional y amable de BANCO HENRY.
            
            Pregunta del cliente:
            {query}
            
            Proporciona una respuesta útil, precisa y profesional.
            """,
            input_variables=["query"]
        )
        
        general_chain = LLMChain(llm=self.llm, prompt=prompt)
        return general_chain.run(query=query)
        
    def process_query(self, query: str) -> str:
        """
        Procesa una consulta del usuario decidiendo el método más apropiado para responder.
        
        Args:
            query (str): La consulta del usuario.
            
        Returns:
            str: Respuesta a la consulta.
        """
        logger.info(f"Procesando consulta: {query}")
        
        try:
            # Enrutar la consulta
            result = self.router_chain.run(input=query)
            
            # Intentar analizar el resultado como JSON
            try:
                router_output = RouterOutputParser().parse(result)
                destination = router_output.get("destination", "general")
            except Exception as parse_error:
                logger.warning(f"Error al analizar la respuesta del router: {parse_error}. Utilizando ruta general.")
                destination = "general"
            
            logger.info(f"Ruta seleccionada: {destination}")
            
            # Procesar según el destino
            if destination == "consulta_balance":
                return self._process_balance_query(query)
            elif destination == "info_bancaria":
                return self._process_knowledge_query(query)
            else:  # general u otro caso
                return self._process_general_query(query)
        except Exception as e:
            logger.error(f"Error al procesar consulta: {e}")
            return "Lo siento, ha ocurrido un error al procesar tu consulta. Por favor, intenta de nuevo."

def main():
    """
    Función principal que ejecuta el sistema de atención al cliente.
    """
    logger.info("Iniciando Sistema de Atención al Cliente Automatizado")
    
    print("=" * 50)
    print("Sistema de Atención al Cliente Automatizado - BANCO HENRY")
    print("=" * 50)
    
    # Seleccionar modelo
    model_info = select_model()
    if not model_info:
        print("No se ha seleccionado un modelo. Saliendo del programa.")
        return
    
    try:
        # Crear la instancia del LLM
        llm = create_llm_instance(model_info)
        
        # Inicializar el sistema
        system = CustomerSupportSystem(llm)
        
        print("\nSistema listo para procesar consultas.")
        print("Por favor, haz tu consulta. Para salir, escribe 'salir'.")
        
        # Bucle principal de interacción
        while True:
            print("\n" + "-" * 30)
            query = input("Tu consulta: ")
            
            if query.lower() in ["salir", "exit", "quit"]:
                print("Gracias por utilizar nuestro sistema. ¡Que tengas un buen día!")
                break
            
            # Procesar consulta
            response = system.process_query(query)
            print("\nRespuesta:", response)
    
    except KeyboardInterrupt:
        print("\nSesión terminada por el usuario.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        print(f"\nHa ocurrido un error inesperado: {e}")
    
    logger.info("Finalizando Sistema de Atención al Cliente Automatizado")

if __name__ == "__main__":
    main()
