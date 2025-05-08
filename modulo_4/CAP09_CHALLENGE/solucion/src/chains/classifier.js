import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnableSequence } from "@langchain/core/runnables";

/**
 * Clasificador que determina si una pregunta debe ser respondida con información de noticias
 * o con conocimientos generales
 */
export const createQuestionClassifier = () => {
  // Crear modelo con temperatura baja para clasificación
  const model = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    temperature: 0,
  });

  // Prompt para clasificar la pregunta
  const classifierPrompt = PromptTemplate.fromTemplate(`
    Tu tarea es clasificar la pregunta del usuario para determinar si requiere 
    información de noticias recientes o conocimientos generales.
    
    Clasifica la pregunta en una de estas categorías:
    1. NOTICIAS: Si la pregunta solicita información sobre eventos actuales, noticias recientes,
       o temas que podrían estar cubiertos en portales de noticias.
    2. GENERAL: Si la pregunta es sobre conocimientos generales, conceptos, historia, ciencia,
       o temas que no necesitan información de noticias actualizadas.
    
    Responde SOLO con la palabra "NOTICIAS" o "GENERAL".
    
    Pregunta: {question}
  `);

  // Crear secuencia de clasificación
  const classifierChain = RunnableSequence.from([
    classifierPrompt,
    model,
    new StringOutputParser(),
  ]);

  return classifierChain;
};