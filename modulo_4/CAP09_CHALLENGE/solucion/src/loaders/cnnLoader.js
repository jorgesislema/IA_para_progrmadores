import { RecursiveUrlLoader } from "langchain/document_loaders/web/recursive_url";
import { CheerioWebBaseLoader } from "langchain/document_loaders/web/cheerio";

/**
 * Cargador para noticias de CNN Español
 * Utiliza RecursiveUrlLoader para navegar por la página y extraer enlaces
 */
export const loadCNNNews = async () => {
  console.log("Cargando noticias de CNN Español...");
  
  try {
    // Carga la página principal de CNN Español (versión lite)
    const loader = new RecursiveUrlLoader("https://cnnespanol.cnn.com/lite/", {
      // Definir un extractor de texto personalizado para la página
      extractor: (url, html) => {
        // Extraer solo el texto principal del artículo
        const cheerio = new CheerioWebBaseLoader().parse(html);
        const $ = cheerio.load(html);
        
        // Extraer título y contenido según la estructura de CNN
        const title = $("h1").first().text().trim();
        const content = $("article p").map((_, el) => $(el).text().trim()).get().join("\n");
        
        if (!content) return null; // Ignorar páginas sin contenido
        
        return `TÍTULO: ${title}\n\nCONTENIDO: ${content}`;
      },
      // Parámetros para controlar la recursión
      maxDepth: 2,
      excludePatterns: ["/author/", "/tag/", "/category/"],
    });

    // Cargar los documentos
    const docs = await loader.load();
    console.log(`Cargadas ${docs.length} noticias de CNN Español`);
    
    return docs;
  } catch (error) {
    console.error("Error al cargar noticias de CNN Español:", error);
    return [];
  }
};