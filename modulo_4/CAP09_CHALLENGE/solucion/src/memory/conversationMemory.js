import { ConversationSummaryMemory } from "langchain/memory";
import { ChatOpenAI } from "@langchain/openai";

/**
 * Crea una memoria para la conversación
 */
export const createConversationMemory = async () => {
  // Modelo para resumir la conversación
  const model = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    temperature: 0,
  });
  
  // Crear memoria con resumen de conversación
  const memory = new ConversationSummaryMemory({
    memoryKey: "chat_history",
    llm: model,
    returnMessages: true,
  });
  
  return memory;
};