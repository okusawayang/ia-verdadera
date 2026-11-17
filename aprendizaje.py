# aprendizaje.py — Pieza 6: aprendizaje continuo.
# REESCRITO POR EL SUPERVISOR (Muse). El código del agente llamaba a
# métodos que no existen (actualizar_transicion, guardar_experiencia,
# memoria.experiencias), usaba variables no definidas (nuevo_estado y
# recompensa dentro de consolidar), trataba los hechos de texto como
# diccionarios con ['texto'], y su bloque principal tenía una variable
# "experience" que no existía. Esta versión usa los nombres reales de
# Memoria y ModeloMundo, y guarda las experiencias también como datos
# estructurados para consolidar sin parsear texto.

from memoria import Memoria
from mundo import ModeloMundo

class AprendizajeContinuo:
    def __init__(self, memoria, modelo_mundo):
        self.memoria = memoria
        self.modelo_mundo = modelo_mundo
        self._experiencias = []

    def aprender(self, experiencia):
        self._experiencias.append(experiencia)
        self.modelo_mundo.actualizar(
            experiencia["estado"], experiencia["accion"], experiencia["nuevo_estado"])
        self.memoria.guardar(
            "Aprendí: de {} con {} llegué a {}".format(
                experiencia["estado"], experiencia["accion"], experiencia["nuevo_estado"]))

    def consolidar(self):
        # Cuenta cuántas veces aparece cada (estado, accion) y guarda una
        # regla para las que aparecen 2 o más veces.
        conteo = {}
        for exp in self._experiencias:
            clave = (exp["estado"], exp["accion"])
            conteo[clave] = conteo.get(clave, 0) + 1
            if conteo[clave] == 2:
                self.memoria.guardar(
                    "Regla: de {} con {} casi siempre llego a {}".format(
                        clave[0], clave[1], exp["nuevo_estado"]))

    def experiencias(self):
        # Devuelve los hechos de la memoria que empiezan con "Aprendí:"
        return [h for h in self.memoria.hechos() if h.startswith("Aprendí:")]

if __name__ == "__main__":
    # Crear una memoria
    memoria = Memoria()

    # Crear un modelo del mundo
    modelo_mundo = ModeloMundo()

    # Crear un aprendizaje continuo con la memoria y el modelo del mundo
    aprendizaje_continuo = AprendizajeContinuo(memoria, modelo_mundo)

    # Aprende 2 experiencias iguales
    experiencia1 = {"estado": (0, 0), "accion": "derecha", "nuevo_estado": (0, 1), "recompensa": -1}
    experiencia2 = {"estado": (0, 0), "accion": "derecha", "nuevo_estado": (0, 1), "recompensa": -1}
    aprendizaje_continuo.aprender(experiencia1)
    aprendizaje_continuo.aprender(experiencia2)

    # Consolidar
    aprendizaje_continuo.consolidar()

    # Mostrar las experiencias de la memoria que empiezan con "Aprendí:"
    print("Experiencias de la memoria que empiezan con 'Aprendí:'")
    for experiencia in aprendizaje_continuo.experiencias():
        print(experiencia)
    print("Hechos tras consolidar:", memoria.hechos())
