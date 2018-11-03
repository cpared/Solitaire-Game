from mesa import *
from mazo import*

class Solitario...:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        pass

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        pass

    def termino(self):
        """Avisa si el juego se terminó."""
        pass

    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""
        pass
