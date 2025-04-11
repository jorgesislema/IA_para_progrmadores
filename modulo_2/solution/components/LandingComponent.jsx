'use client'

export default function LandingComponent() {
  return (
    <div className="min-h-screen bg-white flex flex-col justify-between">
      
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-8 py-4 shadow-sm">
        <div className="text-2xl font-bold text-black">HENRY</div>
        <div className="flex gap-6 text-sm font-medium text-gray-700">
          <a href="#" className="hover:text-black">Para estudiantes</a>
          <a href="#" className="hover:text-black">Para empresas</a>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-1 border border-black text-black rounded hover:bg-gray-100">Ingresar</button>
          <button className="px-4 py-1 bg-yellow-400 text-black rounded font-semibold hover:bg-yellow-300">Aplicar</button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="flex flex-col-reverse md:flex-row items-center justify-between px-8 py-12 md:py-24">
        
        {/* Text Section */}
        <div className="max-w-xl space-y-6">
          <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900">
            Comienza o acelera tu carrera en tecnología
          </h1>
          <p className="text-xl text-gray-700">
            Estudia Desarrollo Full Stack, Data Science o Data Analytics.
          </p>
          <ul className="space-y-2 text-gray-600">
            <li>✅ Online, en vivo y flexible</li>
            <li>✅ Basado en proyectos</li>
            <li>✅ Basado en cohortes</li>
            <li>✅ Garantía de Empleo</li>
          </ul>
          <button className="mt-6 px-6 py-3 bg-yellow-400 text-black rounded font-bold hover:bg-yellow-300">
            Aplicar
          </button>
        </div>

        {/* Image Section */}
        <div className="mt-10 md:mt-0 md:ml-12">
        <img
          src="/landing-results.png"
          alt="Estudiante feliz en su escritorio"
           className="rounded-xl shadow-lg w-[400px] max-w-full"
        />

        </div>
      </section>

      {/* FOOTER */}
      <footer className="text-center bg-gray-100 py-4 text-lg font-medium text-gray-800">
        Bootcamp #1 de Latam
      </footer>
    </div>
  );
}
