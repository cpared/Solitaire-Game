from mesa import *
from mazo import*

CANT_FUNDACIONES = 8
CANT_PILAS_TABLERO = 10

class SolitarioSpider:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo(mazos = 2, palos = 1)

        for i in range(CANT_FUNDACIONES):
            # Creamos 8 fundaciones, una para cada palo, no más restricciones
            self.mesa.fundaciones.append(
                PilaCartas(
                    criterio_apilar=criterio(orden= ASCENDENTE),
                    criterio_mover = criterio(orden= ASCENDENTE)
                ))

        for i in range(CANT_PILAS_TABLERO):
            # Creamos 10 pilas en el tablero, sin restricciones.
            self.mesa.pilas_tablero.append(
                PilaCartas(
                    pila_visible=True, 
                    criterio_apilar = criterio(orden= ASCENDENTE),
                    criterio_mover = criterio(orden= ASCENDENTE)
                ))

            for _ in range(5 + (1 if (i % 3 == 0) else 0)):
                # Barajamos cartas en nuestra pila
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar = True)
            self.mesa.pilas_tablero[i].tope().voltear() # Ponemos boca arriba todas las cartas.

    def termino(self):
        """Avisa si el juego se terminó."""
        for pila in self.mesa.pilas_tablero:
            if not pila.es_vacia():
                return False
        return True

    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""
        j0, p0 = jugada[0]
        j1, p1 = jugada[1] if len(jugada) == 2 else (SALIR, 0)

        if len(jugada) == 1 and j0 == PILA_TABLERO:
            for fundacion in self.mesa.fundaciones:
                if fundacion.es_vacia():
                    self._pila_a_fundacion(self.mesa.pilas_tablero[p0], fundacion)
                    break

        elif len(jugada) == 1 and j0 == MAZO:
            if self.mesa.mazo.es_vacia():
                raise SolitarioError('El mazo está vacío')
            for i in range(10):
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar = True)
                self.mesa.pilas_tablero[i].tope().voltear() # Ponemos boca arriba todas las cartas.

        elif len(jugada) == 2 and j0 == PILA_TABLERO and j1 == PILA_TABLERO:
            # Especificaron origen y destino, intentamos mover del tablero adonde corresponda.
            destino = self.mesa.pilas_tablero[p1]
            self._pila_a_pila(self.mesa.pilas_tablero[p0], destino)
        else:
            # No hay más jugadas válidas según nuestras reglas.
            raise SolitarioError("Movimiento inválido")

    def _carta_a_pila(self, origen, pila):
        """Mueve la carta del tope entre dos pilas, si se puede, levanta SolitarioError si no."""
        if origen.es_vacia():
            raise SolitarioError("La pila está vacía")
            
        # Dejamos que PilaCarta haga las validaciones :)
        pila.apilar(origen.tope())
        origen.desapilar()

        if not origen.es_vacia() and origen.tope().boca_abajo:
            origen.tope().voltear()

    def _pila_a_pila(self, origen, pila):
        """Mueve una pila de cartas a otras, si se puede, levanta SolitarioError si no."""
        if origen.es_vacia():
            raise SolitarioError("La pila está vacía")

        # Dejamos que PilaCarta haga las validaciones :)
        pila.mover(origen)

        if not origen.es_vacia() and origen.tope().boca_abajo:
            origen.tope().voltear()

    def _pila_a_fundacion(self, origen, fundacion):
        """Mueve una pila a la fundación, si se puede, levanta SolitarioError si no."""
        if origen.es_vacia():
            raise SolitarioError("La pila está vacía")

        if origen.tope().valor != 1:
            raise SolitarioError("No se puede apilar a la fundación")

        # Invierte la pila de cartas para que el tope sea una K
        aux=PilaCartas(valor_inicial= 13,
                    criterio_apilar=criterio(orden= ASCENDENTE),
                    criterio_mover = criterio(palo = MISMO_COLOR, orden= ASCENDENTE))
        aux.mover(origen)
        while not aux.es_vacia():
            fundacion.apilar(aux.desapilar(),True)

        if not origen.es_vacia() and origen.tope().boca_abajo:
            origen.tope().voltear()

            
