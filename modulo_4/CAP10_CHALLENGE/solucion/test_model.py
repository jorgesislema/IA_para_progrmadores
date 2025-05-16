from main import select_model, create_llm_instance

# Seleccionar modelo
model_info = select_model()

if model_info:
    # Crear instancia del LLM
    llm = create_llm_instance(model_info)
    print(f"Modelo creado: {llm}")
else:
    print("No se seleccionó ningún modelo.")
