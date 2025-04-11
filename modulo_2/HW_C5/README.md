# Clon Landing Page - SoyHenry

Este proyecto es un clon funcional de la página principal de [soyhenry.com](https://www.soyhenry.com), construido como parte de un desafío técnico en el que se utilizó inteligencia artificial para generar el frontend a partir de una imagen de referencia.

## 📌 Objetivo

Replicar de forma fiel el diseño y estructura de la landing page de SoyHenry utilizando tecnologías modernas de frontend, a pesar de no contar con experiencia previa en desarrollo web.

---

## 🧠 Problemas enfrentados y soluciones

| Problema | Solución aplicada |
|---------|-------------------|
| No reconocimiento de `npx` | Se instaló correctamente Node.js desde la web oficial y se configuró el PATH |
| Error en instalación de Tailwind (`npx tailwindcss init -p`) | Se creó manualmente el archivo `tailwind.config.js` y `postcss.config.js` siguiendo instrucciones precisas |
| Imagen no visible en la página | Se renombró el archivo y se colocó correctamente en la carpeta `/public` para ser servida estáticamente |
| No había carpeta `components/` | Se creó manualmente para alojar el componente `LandingComponent.jsx` |
| El diseño no era visible o se mostraba incompleto | Se ajustaron rutas de importación, estilos y estructura del código con la guía de GPT |

---

## 🚀 Tecnologías utilizadas

- [Next.js 15](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Node.js](https://nodejs.org/)
- [v0.dev](https://v0.dev/) (Generación de componentes UI a partir de imagen)
- ChatGPT-4o (Asistente IA para debug y guía técnica)

---

## 📁 Estructura del Proyecto

```bash
/solution
├── /app
│   ├── layout.js
│   ├── page.js
│   └── globals.css
├── /components
│   └── LandingComponent.jsx
├── /public
│   └── landing-results.png
├── package.json
├── tailwind.config.js
├── postcss.config.js
```

---

## ⚙️ Cómo usar este proyecto

### 1. Clona el repositorio o copia los archivos

```bash
git clone https://github.com/tu-usuario/soyhenry-clon.git
cd soyhenry-clon
```

### 2. Instala dependencias

```bash
npm install
```

### 3. Ejecuta el servidor de desarrollo

```bash
npm run dev
```

Abre tu navegador en [http://localhost:3000](http://localhost:3000) y ¡listo!

---

## 🎓 Lecciones aprendidas

- Entendí cómo se estructura una app en Next.js con rutas, layouts y componentes.
- Aprendí a instalar y configurar Tailwind CSS manualmente.
- Comprendí cómo funciona la carpeta `/public` para servir imágenes.
- Vi en acción el poder de la IA como copiloto de desarrollo en tiempo real.

---

## 📸 Resultado

![Captura de pantalla](https://github.com/jorgesislema/IA_para_progrmadores/blob/main/modulo_2/HW_C5/Screenshot%202025-04-11%20at%2011-36-17%20Create%20Next%20App.png?raw=true)

---

## 🧹 Estado del proyecto

- ✅ Proyecto funcional
- 🟡 Diseño adaptable en proceso
- 🔜 Posible integración de tests y despliegue en Vercel

---

## 📄 Licencia

Este proyecto es de uso libre con fines educativos.


