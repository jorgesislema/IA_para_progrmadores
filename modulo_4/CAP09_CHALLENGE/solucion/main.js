import 'dotenv/config';
import readline from 'readline';
import { createQuestionClassifier } from './src/chains/classifier.js';
import { loadAllNews, createNewsChain } from './src/chains/newsChain.js';
import { createGeneralChain } from './src/chains/generalChain.js';
import { createConversationMemory } from './src/memory/conversationMemory.js';

// Verificar API key
if (!process.env.OPENAI_API_KEY) {
  console.error("Error: OPENAI_API_KEY no está configurada en el archivo .env");
  process.exit(1);
}

// Crear interfaz de línea de comandos
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Función principal
async function main() {
  console.log("Inicializando Sistema de Consulta de Noticias...");
  
  // Cargar noticias y crear vector store
  console.log("Cargando noticias de CNN Español y CBC News...");
  await loadAllNews();
  console.log("Noticias cargadas correctamente.");
  
  // Inicializar cadenas
  const classifier = createQuestionClassifier();
  const newsChain = createNewsChain();
  const generalChain = createGeneralChain();
  
  // Inicializar memoria (opcional para puntos extra)
  const memory = await createConversationMemory();
  
  console.log("\n=== Sistema de Consulta de Noticias ===");
  console.log("Escribe tu pregunta o 'salir' para terminar\n");

  // Función para manejar preguntas
  const handleQuestion = async (question) => {
    if (question.toLowerCase() === 'salir') {
      rl.close();
      return;
    }
    
    try {
      // 1. Clasificar la pregunta
      console.log("Clasificando pregunta...");
      const classification = await classifier.invoke({ question });
      console.log(`Clasificación: ${classification}`);
      
      // 2. Seleccionar cadena apropiada
      let response;
      if (classification.trim().toUpperCase() === "NOTICIAS") {
        console.log("Buscando información en noticias...");
        // Respuesta con streaming para consultas de noticias
        response = await newsChain.stream({
          question: question,
        });
      } else {
        console.log("Generando respuesta general...");
        // Respuesta con streaming para consultas generales
        response = await generalChain.stream({
          question: question,
        });
      }
      
      // 3. Mostrar respuesta en streaming
      process.stdout.write("Respuesta: ");
      let fullResponse = "";
      for await (const chunk of response) {
        process.stdout.write(chunk);
        fullResponse += chunk;
      }
      console.log("\n");
      
      // 4. Actualizar memoria con la interacción
      await memory.saveContext(
        { input: question },
        { output: fullResponse }
      );
      
      // Pedir la siguiente pregunta
      rl.question("Tu pregunta: ", handleQuestion);
      
    } catch (error) {
      console.error("Error al procesar la pregunta:", error);
      rl.question("Tu pregunta: ", handleQuestion);
    }
  };
  
  // Iniciar diálogo
  rl.question("Tu pregunta: ", handleQuestion);
}

// Ejecutar aplicación
main().catch(error => {
  console.error("Error en la aplicación:", error);
  process.exit(1);
});