# objetivo.py — Pieza 1: objetivo de entrenamiento.
# Recompensa el razonamiento verificable, no la predicción de la palabra.
# CORREGIDO POR EL SUPERVISOR (Muse): el código del agente usaba una
# variable "texto" que no existía (NameError), extraer_respuesta_final
# devolvía int en vez de texto y tomaba el PRIMER número, no el último,
# y faltaba el caso 0.0. Decisión del supervisor: una palabra prohibida
# anula la recompensa aunque la respuesta final sea correcta.

TAREAS_VERIFICABLES = [
    {"pregunta": "¿Cuánto es 17 + 25?", "respuesta": "42"},
    {"pregunta": "¿Cuánto es 30 - 15?", "respuesta": "15"},
    {"pregunta": "¿Cuánto es 8 x 9?", "respuesta": "72"},
    {"pregunta": "¿Cuánto es 45 ÷ 5?", "respuesta": "9"},
    {"pregunta": "¿Cuánto es 60 + 30?", "respuesta": "90"},
]

PALABRAS_PROHIBIDAS = ["cuántico", "telepatía", "magia"]

def extraer_respuesta_final(texto):
    """Devuelve el último número que aparece en el texto, como texto, o "" si no hay ninguno."""
    numeros = [p for p in texto.split() if p.isdigit()]
    return numeros[-1] if numeros else ""

def recompensa(respuesta, correcta):
    """1.0 si la respuesta final coincide; 0.5 si razona pero falla;
    0.0 si no hay razonamiento ni respuesta; -1.0 si inventa un dato prohibido."""
    if not isinstance(respuesta, str) or not isinstance(correcta, str):
        return -1.0
    texto = respuesta.lower()
    if any(p in texto for p in PALABRAS_PROHIBIDAS):
        return -1.0
    if extraer_respuesta_final(respuesta) == correcta:
        return 1.0
    if any(p in texto for p in ("primero", "luego", "entonces")):
        return 0.5
    return 0.0

if __name__ == "__main__":
    print("Correcta con pasos:", recompensa("Primero sumo 17 + 25. Respuesta: 42", "42"))
    print("Pasos pero mal:", recompensa("Primero sumo. Respuesta: 41", "42"))
    print("Sin razonar:", recompensa("No sé", "42"))
    print("Inventada:", recompensa("Por magia cuántica es 42", "42"))
