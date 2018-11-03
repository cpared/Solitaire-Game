from pila_cartas import *

# Constantes que describen las opciones de entrada del usuario.
FUNDACION = 0
PILA_TABLERO = 1
MAZO = 2
DESCARTE = 3
SALIR = 4


class Mesa:
    """Representa la mesa del juego del solitario. Como atributos posee:
        fundaciones: Lista de PilaCartas. Representa las fundaciones del juego,
            numeradas de 1 a n.
        pilas_tablero: Lista de PilaCartas. Representa las pilas del tablero,
            indicatas de la A a la N.
        mazo: PilaCartas. Representa al mazo. Todo solitario posee un mazo,
            aunque el mismo se encuentre vacío.
        descarte: PilaCartas. Representa al descarte."""

    def __init__(self):
        """Crea una mesa vacía."""
        self.fundaciones = []
        self.pilas_tablero = []
        self.mazo = None
        self.descarte = None

    def imprimir(self):
        """Imprime por pantalla una representación de la mesa actual."""
        if self.fundaciones:
            print("FUNDACIONES:")
            for i,fundacion in enumerate(self.fundaciones):
                print(i + 1, fundacion)
        if self.pilas_tablero:
            print("TABLERO:")
            for i,pila in enumerate(self.pilas_tablero):
                print(chr(ord('A')+i), pila)
        print("MAZO")
        print('M', self.mazo)
        if self.descarte:
            print('N', self.descarte)

    def mensaje_jugada(self):
        """Retorna el mensaje que debe mostrársele al usuario para el input
        de la configuración actual de la mesa."""
        msg = "Ingrese"

        if self.fundaciones:
            msg += ' [1-{}]'.format(len(self.fundaciones))

        if self.pilas_tablero:
            msg += ' [A-{}]'.format(chr(ord('A') + len(self.pilas_tablero) - 1))

        msg += ' M'

        if self.descarte:
            msg += ' N'

        msg += ' Q: '

        return msg

    def parsear_jugada(self, inp):
        """Dada la entrada inp del usuario se devuelven las acciones indicadas.
        En funcionamiento normal devuelve una lista de 1 o 2 elementos.
        Cada elemento es un par (PILA, índice) donde PILA es un valor entre
        FUNDACION, MAZO, DESCARTE, PILA_TABLERO o SALIR. El índice es el índice
        de la FUNDACION o de la PILA_TABLERO de corresponder o 0 si no.
        En caso de falla devuelve None."""
        inp = inp.upper()

        jugada = []
        for c in inp:
            if c.isdigit():
                n = int(c)
                if n < 1 or n > len(self.fundaciones):
                    return None
                jugada.append((FUNDACION, n - 1))
            elif c == 'M':
                jugada.append((MAZO, 0))
            elif self.descarte and c == 'N':
                jugada.append((DESCARTE, 0))
            elif c == 'Q':
                jugada.append((SALIR, 0))
            elif c >= 'A' and c < chr(ord('A') + len(self.pilas_tablero)):
                jugada.append((PILA_TABLERO, ord(c) - ord('A')))
            else:
                return None
        return jugada

