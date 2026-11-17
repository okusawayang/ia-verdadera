# test_ia.py — Pruebas de todos los módulos.
# REESCRITO POR EL SUPERVISOR (Muse). El código del agente probador no
# tenía NI UNA importación, llamaba a las funciones con argumentos
# incorrectos e inventaba métodos (model.reconstruir, app.ajustar,
# meta.obtener, app.get_recompensa). Esta versión importa los nombres
# reales y comprueba el comportamiento real de cada módulo.

from objetivo import recompensa, extraer_respuesta_final
from razonamiento import Razonador, generador_ejemplo, verificador_ejemplo
from mundo import MundoRejilla, ModeloMundo
from memoria import Memoria, verificar_paso
from metas import SistemaMetas, Meta
from aprendizaje import AprendizajeContinuo
from ia_verdadera import IAVerdadera

def test_recompensa():
    assert recompensa("Primero sumo. Respuesta: 42", "42") == 1.0
    assert recompensa("Primero sumo. Respuesta: 41", "42") == 0.5
    assert recompensa("No sé", "42") == 0.0
    assert recompensa("Por magia es 42", "42") == -1.0
    assert extraer_respuesta_final("sumo 17 y 25, da 42") == "42"
    assert extraer_respuesta_final("sin números") == ""

def test_razonador():
    razonador = Razonador(n_caminos=3)
    mejor, puntaje = razonador.razonar(
        "¿Cuánto es 17 + 25?", generador_ejemplo, verificador_ejemplo)
    assert puntaje == 1.0
    assert mejor.endswith("42")

def test_mundo():
    mundo = MundoRejilla()
    assert mundo.estado_inicial() == (0, 0)
    assert "arriba" not in mundo.acciones_posibles((0, 0))  # fuera de la rejilla
    assert "derecha" in mundo.acciones_posibles((0, 0))
    nuevo, rec, term = mundo.aplicar((4, 3), "derecha")
    assert nuevo == (4, 4) and rec == 10 and term is True
    modelo = ModeloMundo()
    assert modelo.predecir((0, 0), "derecha") is None
    modelo.actualizar((0, 0), "derecha", (0, 1))
    assert modelo.predecir((0, 0), "derecha") == (0, 1)

def test_memoria():
    mem = Memoria()
    mem.guardar("El perro corre rápido.")
    mem.guardar("La casa está en la ciudad.")
    assert mem.recordar("corre") == ["El perro corre rápido."]
    assert len(mem.hechos()) == 2
    assert verificar_paso("El perro corre rápido.", mem.hechos()) is True
    assert verificar_paso("El perro corre rápido.", ["No El perro corre rápido."]) is False

def test_metas():
    sistema = SistemaMetas()
    sistema.agregar_meta(Meta("llegar a (4, 4)", 10, lambda e: e == (4, 4)))
    sistema.agregar_meta(Meta("visitar (0, 4)", 5, lambda e: e == (0, 4)))
    activa = sistema.meta_activa((0, 0))
    assert activa is not None and activa.descripcion == "llegar a (4, 4)"
    assert sistema.meta_activa((4, 4)).descripcion == "visitar (0, 4)"
    assert len(sistema.revisar((4, 4))) == 1

def test_aprendizaje():
    mem = Memoria()
    modelo = ModeloMundo()
    ap = AprendizajeContinuo(mem, modelo)
    exp = {"estado": (0, 0), "accion": "derecha", "nuevo_estado": (0, 1), "recompensa": -1}
    ap.aprender(exp)
    ap.aprender(exp)
    assert modelo.predecir((0, 0), "derecha") == (0, 1)
    assert len(ap.experiencias()) == 2
    ap.consolidar()
    assert any(h.startswith("Regla:") for h in mem.hechos())

def test_integracion():
    ia = IAVerdadera()
    assert ia.pensar("¿Cuánto es 17 + 25?").endswith("42")
    visitados = ia.actuar_en_mundo(5)
    assert len(visitados) >= 2
    assert visitados[0] == (0, 0)

if __name__ == "__main__":
    test_recompensa()
    test_razonador()
    test_mundo()
    test_memoria()
    test_metas()
    test_aprendizaje()
    test_integracion()
    print("TODAS LAS PRUEBAS PASARON")
