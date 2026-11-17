# agente.py — Pieza 3: el agente (bucle percibir-pensar-actuar).
# REESCRITO POR EL SUPERVISOR (Muse). El código del agente tenía 6
# errores graves: (1) faltaba "from memoria import Memoria";
# (2) elegir_accion llamaba a predecir(estado) con UN argumento (son
# dos: estado y acción) y usaba modelo_mundo.recompensas, que no existe;
# (3) observar llamaba a memoria.guarda_aleatorio, que no existe;
# (4) correr creaba un mundo, un modelo, una memoria y un agente NUEVOS
# en vez de usar los del propio agente; (5) llamaba a ModeloMundo(mundo)
# con un argumento (el constructor no recibe ninguno);
# (6) llamaba a mundo.aplicar(accion, estado) con los argumentos al
# revés e intentaba iterar sobre la memoria, que no es iterable.
# Nota del supervisor: elegir_accion es codiciosa (greedy) — elige la
# acción cuyo estado predicho está más cerca de la meta (distancia
# Manhattan). Sin planificación (búsqueda), el agente puede dar vueltas;
# eso es una limitación real de este prototipo, no un error.

from mundo import MundoRejilla, ModeloMundo
from memoria import Memoria

class Agente:
    def __init__(self, mundo, modelo_mundo, memoria):
        self.mundo = mundo
        self.modelo_mundo = modelo_mundo
        self.memoria = memoria

    def percibir(self, estado):
        return estado

    def elegir_accion(self, estado):
        acciones = self.mundo.acciones_posibles(estado)
        if not acciones:
            return None
        mejor = None
        mejor_distancia = None
        for accion in acciones:
            predicho = self.modelo_mundo.predecir(estado, accion)
            # Si el modelo no conoce la transición, supone que se queda
            # donde está (sin progreso). Si no conoce ninguna, el empate
            # deja la primera acción posible.
            destino = predicho if predicho is not None else estado
            distancia = (abs(destino[0] - self.mundo.meta[0])
                         + abs(destino[1] - self.mundo.meta[1]))
            if mejor_distancia is None or distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor = accion
        return mejor

    def observar(self, estado, accion, nuevo_estado, recompensa):
        self.modelo_mundo.actualizar(estado, accion, nuevo_estado)
        self.memoria.guardar("De {} con {} llegué a {}".format(estado, accion, nuevo_estado))

    def correr(self, pasos=10):
        estado = self.mundo.estado_inicial()
        visitados = [estado]
        for _ in range(pasos):
            estado = self.percibir(estado)
            accion = self.elegir_accion(estado)
            if accion is None:
                break
            nuevo_estado, recompensa, terminado = self.mundo.aplicar(estado, accion)
            self.observar(estado, accion, nuevo_estado, recompensa)
            estado = nuevo_estado
            visitados.append(estado)
            if terminado:
                break
        return visitados

if __name__ == "__main__":
    mundo = MundoRejilla()
    modelo_mundo = ModeloMundo()
    memoria = Memoria()

    agente = Agente(mundo, modelo_mundo, memoria)

    estados_visitados = agente.correr(pasos=10)
    print(estados_visitados)
    print("Hechos en memoria:", memoria.hechos()[:3])
