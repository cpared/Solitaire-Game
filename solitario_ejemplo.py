from mesa import *
from mazo import*

class SolitarioEjemplo:
    """
        SOLITARIO DE EJEMPLO
        Este solitario tiene:
            1 Mazo
            4 Fundaciones
            12 Pilas
        Al inicio el mazo se reparte completo sobre las 12 pilas.
        En las fundaciones hay que apilar cartas del mismo palo sin importar el valor.
        Se puede mover el tope de las pilas del tablero entre distintas pilas.
        El juego se termina cuando se subieron todas las cartas de las pilas del tablero a las fundaciones.
    """
    def __init__(self, mesa):
        """Inicializa con una mesa creada."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero a la configuración inicial."""
        self.mesa.mazo = crear_mazo() # Creamos un mazo.

        for i in range(4):
            # Creamos 4 fundaciones, una para cada palo, no más restricciones
            self.mesa.fundaciones.append(
                PilaCartas(
                    criterio_apilar=criterio(palo=MISMO_PALO),
                ))

        for i in range(12):
            # Creamos 12 pilas en el tablero, sin restricciones.
            self.mesa.pilas_tablero.append(
                PilaCartas(
                    pila_visible=True,
                ))

            for j in range(4 + (1 if i < 4 else 0)):
                # Barajamos cartas en nuestra pila
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar())
            self.mesa.pilas_tablero[i].tope().voltear() # Ponemos boca arriba la última carta.

    def termino(self):
        """Avisa si el juego se terminó."""
        for pila in self.mesa.pilas_tablero:
            if not pila.es_vacia():
                return False
        return True

    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero).
            Si no puede realizarse la jugada se levanta una excepción SolitarioError descriptiva."""
        j0, p0 = jugada[0]
        j1, p1 = jugada[1] if len(jugada) == 2 else (SALIR, 0)

        if len(jugada) == 1 and j0 == PILA_TABLERO:
            # Sólo especificaron una pila de origen, intentamos mover a alguna fundación.
            for fundacion in self.mesa.fundaciones:
                try:
                    self._carta_a_pila(self.mesa.pilas_tablero[p0], fundacion)
                    return
                except SolitarioError:
                    pass
            raise SolitarioError("No puede moverse esa carta a la fundación")
        elif len(jugada) == 2 and j0 == PILA_TABLERO and j1 in (FUNDACION, PILA_TABLERO):
            # Especificaron origen y destino, intentamos mover del tablero adonde corresponda.
            destino = self.mesa.fundaciones[p1] if j1 == FUNDACION else self.mesa.pilas_tablero[p1]
            self._carta_a_pila(self.mesa.pilas_tablero[p0], destino)
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
