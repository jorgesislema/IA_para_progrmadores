@echo off
REM Activar entorno virtual
call "venv\Scripts\activate.bat"

REM Iniciar servidor FastAPI con Uvicorn
uvicorn app.main:app --reload

REM Esperar para que no se cierre la consola al terminar
pause
