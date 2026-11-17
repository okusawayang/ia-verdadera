# razonamiento.py

class Razonador:
    def __init__(self, n_caminos=3):
        self.n_caminos = n_caminos
    
    def razonar(self, problema, generador, verificador):
        candidatos = generador(problema)
        puntajes = [verificador(candidato) for candidato in candidatos]
        
        mejor_puntuacion = max(puntajes)
        mejores_candidatos = [candidato for candidato, puntuacion in zip(candidatos, puntajes) if puntuacion == mejor_puntuacion]
        
        return (mejores_candidatos[0], mejor_puntuacion)

def generador_ejemplo(problema):
    return ["Respuesta: 42", "Respuesta: 41", "Primero sumo, luego resto. Respuesta: 42"]

def verificador_ejemplo(candidato, correcta="42"):
    if candidato.endswith(correcta):
        return 1.0
    elif "Primero" in candidato:
        return 0.5
    else:
        return 0.0

if __name__ == "__main__":
    razonador = Razonador()
    problema = "¿Cuánto es 17 + 25?"
    resultado = razonador.razonar(problema, generador_ejemplo, verificador_ejemplo)
    print(resultado[0], resultado[1])
