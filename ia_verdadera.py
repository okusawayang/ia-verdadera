# ia_verdadera.py — Módulo principal: une las 7 piezas en una sola IA.
# REESCRITO POR EL SUPERVISOR (Muse). El código del agente de
# integración inventó una API que no existe en ningún módulo:
# ModeloMundo(mundo), Razonador(generador, verificador),
# Agente(razonador, sistema_metas), Meta(descripción, condición),
# AprendizajeContinuo() sin argumentos, razonador.pensar(),
# mundo.obtener_estado(), agente.actuar(), mundo.actualizar(),
# mundo.recompensar(), aprendizaje.ajustar_recompensas() y
# meta.get_estado_activo(). Esta versión usa los nombres y firmas reales
# de cada módulo.

from mundo import MundoRejilla, ModeloMundo
from memoria import Memoria
from metas import SistemaMetas, Meta
from razonamiento import Razonador, generador_ejemplo, verificador_ejemplo
from agente import Agente
from aprendizaje import AprendizajeContinuo

class IAVerdadera:
    def __init__(self):
        self.mundo = MundoRejilla()
        self.modelo_mundo = ModeloMundo()
        self.memoria = Memoria()
        self.sistema_metas = SistemaMetas()
        self.sistema_metas.agregar_meta(
            Meta("llegar a la meta del mundo", 10, lambda estado: estado == (4, 4)))
        self.razonador = Razonador(n_caminos=3)
        self.agente = Agente(self.mundo, self.modelo_mundo, self.memoria)
        self.aprendizaje = AprendizajeContinuo(self.memoria, self.modelo_mundo)

    def pensar(self, problema):
        mejor, _puntuacion = self.razonador.razonar(
            problema, generador_ejemplo, verificador_ejemplo)
        return mejor

    def actuar_en_mundo(self, pasos=10):
        return self.agente.correr(pasos=pasos)

    def aprender(self, estado, accion, nuevo_estado, recompensa):
        self.aprendizaje.aprender({
            "estado": estado,
            "accion": accion,
            "nuevo_estado": nuevo_estado,
            "recompensa": recompensa,
        })

    def meta_activa(self, estado):
        return self.sistema_metas.meta_activa(estado)

if __name__ == "__main__":
    ia = IAVerdadera()
    problema = "¿Cuánto es 17 + 25?"
    resultado = ia.pensar(problema)
    print(f"Resultado: {resultado}")
    estados_visitados = ia.actuar_en_mundo(10)
    print("Estados visitados:", estados_visitados)
    estado_final = estados_visitados[-1]
    meta = ia.meta_activa(estado_final)
    print("Meta activa en el estado final:",
          meta.descripcion if meta else "ninguna (meta cumplida)")
