from solitario_ejemplo import *

SOLITARIOS = {
	# "Nombre": (Clase, parámetros constructor),
        "Ejemplo": (SolitarioEjemplo, None),
    }

LOGFILE = 'solitario.log'

from mesa import *

import sys, random, datetime

def loguear(logfile, valor):
    if logfile:
        logfile.write('{}\n'.format(valor))

def recuperar():
    try:
        with open(LOGFILE) as f:
            seed = int(f.readline().rstrip('\n'))
            juego = f.readline().rstrip('\n')
            comandos = [l.rstrip('\n') for l in f]
    except (IOError, ValueError):
        print("ERROR: No pudo recuperarse el juego")
        return None
    return (seed, juego, comandos)

def pedir_juego(juegos):
    print("SOLITARIOS:")
    juegos = sorted(juegos)
    for i,s in enumerate(juegos):
        print(i + 1, s)
    print("Otra cosa para salir")
    try:
        n = int(input('Opción: '))
    except ValueError:
        return None

    if n <= 0 or n > len(juegos):
        return None

    return juegos[n - 1]

def main():
    resume = False
    seed = int(datetime.datetime.now().timestamp())
    juego = None
    comandos = []

    if len(sys.argv) == 2 and sys.argv[1] == '-resume':
        r = recuperar()
        if r:
            resume = True
            seed, juego, comandos = r

    random.seed(seed)

    logfile = None
    if resume:
        try:
            logfile = open(LOGFILE, 'a')
        except IOError:
            pass
    else:
        juego = pedir_juego(SOLITARIOS.keys())
        if not juego:
            return

        try:
            logfile = open(LOGFILE, 'w')
        except IOError:
            pass

        loguear(logfile, seed)
        loguear(logfile, juego)

    print()
    print("JUGANDO " + juego)
    print()

    mesa = Mesa()

    constructor, parametros = SOLITARIOS[juego]
    if parametros:
        solitario = constructor(mesa, *parametros)
    else:
        solitario = constructor(mesa)

    solitario.armar()
    mesa.imprimir()
    while not solitario.termino():
        if comandos:
            comando = comandos.pop(0)
            print("COMANDO:", comando)
        else:
            comando = input(mesa.mensaje_jugada())
            resume = False

        jugada = mesa.parsear_jugada(comando)

        if not jugada:
            print("ERROR: Comando incorrecto")
            continue

        if jugada[0][0] == SALIR:
            break

        if not resume:
            loguear(logfile, comando)

        try:
            solitario.jugar(jugada)
        except SolitarioError as e:
            print("ERROR:", e)
            continue

        print()
        mesa.imprimir()

    print()
    print("Juego Terminado!")

    if logfile:
        logfile.close()

if __name__ == "__main__":
    main()
