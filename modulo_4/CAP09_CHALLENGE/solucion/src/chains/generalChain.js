import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnableSequence } from "@langchain/core/runnables";

/**
 * Crea una cadena para consultas generales
 */
export const createGeneralChain = () => {
  // Modelo para responder consultas generales
  const model = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    temperature: 0.7,
    streaming: true,
  });

  // Prompt para responder consultas generales
  const generalPrompt = PromptTemplate.fromTemplate(`
    Eres un asistente virtual útil y conversacional.
    
    Responde a la pregunta del usuario utilizando tu conocimiento general.
    Sé claro, informativo y amigable en tu respuesta.
    
    Pregunta del usuario: {question}
    
    Respuesta:
  `);

  // Crear cadena general
  const generalChain = RunnableSequence.from([
    generalPrompt,
    model,
    new StringOutputParser(),
  ]);

  return generalChain;
};