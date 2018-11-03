# Estas 3 constantes definen cómo se van a mostrar las cartas. Definirlas
# según lo más adecuado a la plataforma. (Como modo "compatibilidad" definir
# UNICODE_LINDO y COLOR en False y VALOR_10 en '10'.)
UNICODE_LINDO = False
VALOR_10 = '10' # Posibles variantes '⒑', '⏨', '10'
COLOR = False


# Constantes que representan a los palos.
PICAS = 0
CORAZONES = 1
DIAMANTES = 2
TREBOLES = 3


# Constantes para criterios de comparación referidos a palos.
MISMO_PALO = 0
MISMO_COLOR = 1
DISTINTO_COLOR = 2
DISTINTO_PALO = 3

# Constantes para criterios de comparación referidos a valores.
ASCENDENTE = 0
DESCENDENTE = 1
CONSECUTIVA = 2


class Carta:
    """
        Clase que representa una carta de baraja francesa.
        La clase posee tres atributos:
            valor: Un número del 1 al 13.
            palo: Un valor entre PICAS, CORAZONES, DIAMANTES y TREBOLES.
            boca_abajo: Un bool, indica si la carta está boca abajo.
    """

    def __init__(self, valor, palo, boca_abajo=True):
        """Crea una carta de un valor, palo y boca_abajo. Por omisión la carta
        está boca abajo."""
        self.valor = valor
        self.palo = palo
        self.boca_abajo = boca_abajo

    def voltear(self):
        """Da vuelta una carta."""
        self.boca_abajo = not self.boca_abajo

    def __str__(self):
        return _c2s(self.valor, self.palo) if not self.boca_abajo else _c2s(0, 0)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return not self.boca_abajo and self.palo == other.palo and self.valor == other.valor


def criterio(palo=None, orden=None):
    """Generador de funciones de comparación de cartas.
        palo: Un valor entre MISMO_PALO, MISMO_COLOR, DISTINTO_PALO, DISTINTO_COLOR.
        orden: Un valor entre ASCENDENTE, DESCENDENTE o CONSECUTIVA.
    Devuelve una función de comparación cmp(a, b) que indica si la carta b es apilable
    sobre la carta a según el criterio indicado."""
    def comp(a, b):
        if a.boca_abajo or b.boca_abajo:
            # Las cartas tienen que estar boca arriba.
            return False

        if orden is not None:
            # Si hay restricción de valor:
            if orden == ASCENDENTE:
                if a.valor != b.valor + 1:
                    return False
            elif orden == DESCENDENTE:
                if a.valor + 1 != b.valor:
                    return False
            if orden == CONSECUTIVA:
                if a.valor % 13 + 1 != b.valor and a.valor != b.valor % 13 + 1:
                    return False

        if palo is not None:
            # Si hay restricción de palo:
            if palo == MISMO_PALO:
                if a.palo != b.palo:
                    return False
            elif palo == MISMO_COLOR:
                if (a.palo in (CORAZONES, DIAMANTES) and b.palo not in (CORAZONES, DIAMANTES)) or \
                        (a.palo in (PICAS, TREBOLES) and b.palo not in (PICAS, TREBOLES)):
                    return False
            elif palo == DISTINTO_PALO:
                if a.palo == b.palo:
                    return False
            elif palo == DISTINTO_COLOR:
                if (a.palo in (CORAZONES, DIAMANTES) and b.palo in (CORAZONES, DIAMANTES)) or \
                        (a.palo in (PICAS, TREBOLES) and b.palo in (PICAS, TREBOLES)):
                    return False

        return True
    return comp


# A partir de acá son funciones de bajo nivel de las rutinas de impresión...

ANSI_ROJO = "\u001b[31;47m"
ANSI_NEGRO = "\u001b[30;47m"
ANSI_RESET = "\u001b[0m"

def _c2s(valor, palo):
    if COLOR:
        if palo in (CORAZONES, DIAMANTES):
            return _rojo(__c2s(valor, palo))
        else:
            return _negro(__c2s(valor, palo))
    return __c2s(valor, palo)

def _negro(s):
    return ANSI_NEGRO + s + ANSI_RESET

def _rojo(s):
    return ANSI_ROJO + s + ANSI_RESET

def __c2s(valor, palo):
    if UNICODE_LINDO:
        if valor > 11: valor += 1
        return chr(0x1F0A0 + valor + palo*16)
    else:
        if not valor:
            return '▓'
        valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', VALOR_10, 'J', 'Q', 'K']
        palos = "♠♥♦♣"

        return valores[valor-1] + palos[palo]

