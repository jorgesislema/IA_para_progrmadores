# InternetWhisper

![InternetWhisper Banner](https://github.com/santiagomorillosegovia/InternetWhisper/assets/28943730/26840b24-92d3-4ddf-bbd1-82cc6b992c7f)

---

## 🧠 Descripción del Proyecto

**InternetWhisper** es un innovador chatbot de inteligencia artificial diseñado para interactuar con el mundo online. A diferencia de los asistentes virtuales tradicionales, InternetWhisper puede buscar, entender y proporcionar información en tiempo real directamente desde Internet. Está pensado como una herramienta poderosa para obtener respuestas precisas, actualizadas y relevantes, sin necesidad de navegar entre múltiples sitios.

### 🚀 Capacidades Únicas

- **Acceso a información en tiempo real**
- **Comprensión del lenguaje natural y del contexto**
- **Interfaz conversacional tipo chatbot**

### 💡 Valor Agregado

InternetWhisper transforma la experiencia de búsqueda, permitiendo a los usuarios obtener respuestas conversacionales rápidas y útiles desde la web, sin complicaciones.

---

## ⚙️ Explicación Técnica

La arquitectura de InternetWhisper combina procesamiento de lenguaje natural con acceso a datos en tiempo real.

### 🧱 Tecnologías Principales

- **Lenguaje de programación**: JavaScript / TypeScript
- **Framework**: Node.js con Express o Next.js (según configuración actual del proyecto)
- **Motor de IA**: Integración con modelos de lenguaje (probablemente OpenAI API o similar)
- **Acceso a Internet**: Capacidad de scraping o uso de APIs de búsqueda para extraer información dinámica
- **Documentación**: OpenAPI (Swagger)

---

## 🔐 Variables de Entorno

Para que el proyecto funcione correctamente, debes definir las siguientes variables en un archivo `.env` o en el entorno del sistema:

```env
API_KEY=tu_clave_api
BASE_URL=https://internetwhisper.com/api
PORT=3000
```

### 📌 Configuración en Linux/macOS

```bash
export API_KEY="tu_api_key"
export BASE_URL="https://internetwhisper.com/api"
export PORT=3000
```

### 📌 Configuración en Windows

```bash
set API_KEY="tu_api_key"
set BASE_URL="https://internetwhisper.com/api"
set PORT=3000
```

---

## 🛠️ Pasos para Ejecutar Localmente

1. **Clonar el repositorio**

```bash
git clone https://github.com/santiagomorillosegovia/InternetWhisper.git
cd InternetWhisper
```

2. **Instalar dependencias**

```bash
npm install # o yarn install
```

3. **Configurar las variables de entorno**

Edita un archivo `.env` o usa los métodos anteriores.

4. **Iniciar el servidor**

```bash
npm run dev # o yarn dev
```

5. **Abrir en el navegador**

```
http://localhost:3000
```

---

## 📘 Documentación OpenAPI (Swagger)

InternetWhisper expone su documentación OpenAPI de manera automática.

### 📍 Acceso:

```
http://localhost:3000/api-docs
```

### 📚 ¿Por qué es útil?

- Descubre todos los endpoints disponibles
- Visualiza ejemplos de peticiones y respuestas
- Prueba directamente los endpoints desde el navegador
- Exporta o genera clientes automáticamente (Postman, cURL, etc.)

---

## 👥 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz un fork del repositorio
2. Crea una nueva rama con tu funcionalidad: `git checkout -b feature/mi-funcionalidad`
3. Haz commit de tus cambios: `git commit -m "Añade nueva funcionalidad"`
4. Push a la rama: `git push origin feature/mi-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**. Consulta el archivo `LICENSE` para más detalles.

---

## 🙌 Créditos

Desarrollado por **Santiago Morillo Segovia** como parte de un reto de inteligencia artificial aplicado al desarrollo de software conversacional.

---

## 🧠 Bonus Tip

Usa herramientas como **Cody AI**, **ChatGPT**, o **BlackBox** para explorar el repositorio, sugerir mejoras o generar documentación más profunda y personalizada.
