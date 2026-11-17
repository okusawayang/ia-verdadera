# mundo.py — Pieza 7: mundo y modelo del mundo.
# REESCRITO POR EL SUPERVISOR (Muse). El código del agente tenía 4
# errores graves: (1) acciones_posibles no comprobaba los bordes de la
# rejilla y su lógica de obstáculos era confusa (además .remove() podía
# fallar dos veces sobre la misma acción); (2) aplicar daba recompensa
# 10 a CUALQUIER movimiento válido y nunca ponía terminado=True;
# (3) ModeloMundo.actualizar guardaba la tabla con una estructura
# distinta a la que predecir esperaba, así que predecir nunca encontraba
# nada; (4) actualizar usaba self.obstaculos, que ModeloMundo no tiene
# (AttributeError).

class MundoRejilla:
    def __init__(self):
        self.meta = (4, 4)
        self.obstaculos = [(1, 1), (2, 2), (3, 1)]
        self.tamano = 5

    def estado_inicial(self):
        return (0, 0)

    def acciones_posibles(self, estado):
        movimientos = {
            "arriba": (-1, 0),
            "abajo": (1, 0),
            "izquierda": (0, -1),
            "derecha": (0, 1),
        }
        validas = []
        for accion, (dx, dy) in movimientos.items():
            nx, ny = estado[0] + dx, estado[1] + dy
            if 0 <= nx < self.tamano and 0 <= ny < self.tamano and (nx, ny) not in self.obstaculos:
                validas.append(accion)
        return validas

    def aplicar(self, estado, accion):
        if accion not in self.acciones_posibles(estado):
            return (estado, -1, False)
        dx, dy = {
            "arriba": (-1, 0),
            "abajo": (1, 0),
            "izquierda": (0, -1),
            "derecha": (0, 1),
        }[accion]
        nuevo_estado = (estado[0] + dx, estado[1] + dy)
        if nuevo_estado == self.meta:
            return (nuevo_estado, 10, True)
        return (nuevo_estado, -1, False)


class ModeloMundo:
    def __init__(self):
        self.tabla = {}    # (estado, accion) -> nuevo_estado más visto
        self.conteos = {}  # (estado, accion) -> {nuevo_estado: veces}

    def predecir(self, estado, accion):
        return self.tabla.get((estado, accion))

    def actualizar(self, estado, accion, nuevo_estado):
        clave = (estado, accion)
        self.conteos.setdefault(clave, {})
        self.conteos[clave][nuevo_estado] = self.conteos[clave].get(nuevo_estado, 0) + 1
        self.tabla[clave] = max(self.conteos[clave], key=self.conteos[clave].get)


if __name__ == "__main__":
    mundo = MundoRejilla()
    modelo_mundo = ModeloMundo()

    print("Estado inicial:", mundo.estado_inicial())

    estado = mundo.estado_inicial()
    for _ in range(3):
        acciones_posibles = mundo.acciones_posibles(estado)
        accion = acciones_posibles[0]
        nuevo_estado, recompensa, terminado = mundo.aplicar(estado, accion)

        print("Acción:", accion)
        print("Nuevo estado:", nuevo_estado)
        print("Recompensa:", recompensa)
        print("Terminado:", terminado)

        modelo_mundo.actualizar(estado, accion, nuevo_estado)
        estado = nuevo_estado
        if terminado:
            break

    print("El modelo predice desde (0, 0) con 'abajo':",
          modelo_mundo.predecir((0, 0), "abajo"))
