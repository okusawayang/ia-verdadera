# memoria.py — Pieza 5: memoria externa.
# CORREGIDO POR EL SUPERVISOR (Muse): el código del agente tenía el
# atributo self.hechos = [] y el método hechos() con el MISMO nombre:
# el atributo tapaba al método y memoria.hechos() fallaba con
# TypeError. Ahora el atributo es self._hechos. Además verificar_paso
# usaba "No" + paso sin espacio; ahora es "No " + paso.

class Memoria:
    def __init__(self):
        self._hechos = []

    def guardar(self, hecho):
        self._hechos.append(hecho)

    def recordar(self, clave):
        return [h for h in self._hechos if clave.lower() in h.lower()]

    def hechos(self):
        return list(self._hechos)

def verificar_paso(paso, hechos):
    """False si algún hecho es exactamente 'No ' + paso (contradicción), True en otro caso."""
    return ("No " + paso) not in hechos

if __name__ == "__main__":
    memoria = Memoria()

    # Guardar 2 hechos
    memoria.guardar("El perro corre rápido.")
    memoria.guardar("La casa está en la ciudad.")

    # Recordar un hecho por clave
    clave = "corre"
    hechos_con_clave = memoria.recordar(clave)

    print(f"Hechos con '{clave}': {hechos_con_clave}")
    print("Todos los hechos:", memoria.hechos())
