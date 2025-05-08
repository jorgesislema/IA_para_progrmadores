import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnableSequence } from "@langchain/core/runnables";
import { loadCNNNews } from "../loaders/cnnLoader.js";
import { loadCBCNews } from "../loaders/cbcLoader.js";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

// Vector store global para almacenar noticias
let newsVectorStore = null;

/**
 * Carga noticias de todas las fuentes y las almacena en el vector store
 */
export const loadAllNews = async () => {
  // Cargar noticias de ambas fuentes en paralelo
  const [cnnDocs, cbcDocs] = await Promise.all([
    loadCNNNews(),
    loadCBCNews(),
  ]);

  // Combinar documentos de ambas fuentes
  const allDocs = [...cnnDocs, ...cbcDocs];
  
  // Crear vector store con los documentos
  newsVectorStore = await MemoryVectorStore.fromDocuments(
    allDocs, 
    new OpenAIEmbeddings()
  );
  
  console.log(`Vector store creado con ${allDocs.length} noticias`);
  return newsVectorStore;
};

/**
 * Crea una cadena para consultas de noticias
 */
export const createNewsChain = () => {
  // Asegurar que exista el vector store
  if (!newsVectorStore) {
    throw new Error("Es necesario cargar las noticias primero con loadAllNews()");
  }

  // Modelo para responder
  const model = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    temperature: 0.7,
    streaming: true,
  });

  // Función para recuperar contexto relevante
  const retriever = async (query) => {
    const relevantDocs = await newsVectorStore.similaritySearch(query, 3);
    return { 
      context: relevantDocs.map(doc => doc.pageContent).join("\n\n") 
    };
  };

  // Prompt para responder con contexto de noticias
  const newsPrompt = PromptTemplate.fromTemplate(`
    Eres un asistente especializado en noticias actuales.
    
    Responde a la pregunta del usuario basándote en la información de noticias proporcionada.
    Si la información en el contexto no es suficiente para responder completamente,
    indícalo y proporciona la mejor respuesta posible con lo que tienes.
    
    Contexto de noticias:
    {context}
    
    Pregunta del usuario: {question}
    
    Respuesta:
  `);

  // Crear cadena de noticias
  const newsChain = RunnableSequence.from([
    {
      question: input => input.question,
      context: retriever,
    },
    newsPrompt,
    model,
    new StringOutputParser(),
  ]);

  return newsChain;
};