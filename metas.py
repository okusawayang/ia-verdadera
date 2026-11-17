# metas.py — Pieza 4: objetivos propios.
# CORREGIDO POR EL SUPERVISOR (Muse): el código del agente devolvía en
# meta_activa la ÚLTIMA meta agregada sin cumplir, no la de MAYOR
# prioridad. Ahora ordena por prioridad. Se agregó el bloque principal
# que pedía la especificación.

class Meta:
    def __init__(self, descripcion, prioridad, condicion):
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.condicion = condicion

    def cumplida(self, estado):
        return self.condicion(estado)

class SistemaMetas:
    def __init__(self):
        self.metas = []

    def agregar_meta(self, meta):
        self.metas.append(meta)

    def meta_activa(self, estado):
        pendientes = [m for m in self.metas if not m.cumplida(estado)]
        if not pendientes:
            return None
        return max(pendientes, key=lambda m: m.prioridad)

    def revisar(self, estado):
        metas_cumplidas = []
        for meta in self.metas:
            if meta.cumplida(estado):
                metas_cumplidas.append(meta)
        return metas_cumplidas

if __name__ == "__main__":
    sistema = SistemaMetas()
    sistema.agregar_meta(Meta("llegar a (4, 4)", 10, lambda e: e == (4, 4)))
    sistema.agregar_meta(Meta("visitar (0, 4)", 5, lambda e: e == (0, 4)))
    activa = sistema.meta_activa((0, 0))
    print("Meta activa en (0, 0):", activa.descripcion if activa else None)
    print("Metas cumplidas en (4, 4):", [m.descripcion for m in sistema.revisar((4, 4))])
