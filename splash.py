import os
import re
import sys
import time

AZUL = "\033[94m"
NARANJA = "\033[38;5;208m"
VERDE = "\033[92m"
GRIS = "\033[90m"
NEGRITA = "\033[1m"
NORMAL = "\033[0m"

ANCHO_BARRA = 34
PASOS_DE_CARGA = ["Cargando usuarios", "Cargando tickets", "Preparando el menú"]

PLANTILLA_LOGO = [
    "╭──────────────────────────┬─────────╮",
    "│                   ##     ┊    A    │",
    "│                 ##       ┊         │",
    ")    ##         ##         ┊    N    (",
    "│      ##     ##           ┊         │",
    "│         ####             ┊    V    │",
    "╰──────────────────────────┴─────────╯",
]


def habilitar_colores_en_windows():
    if os.name == "nt":
        os.system("")


def colorear(texto, color, usar_colores):
    if not usar_colores:
        return texto
    return f"{color}{texto}{NORMAL}"


def dibujar_logo(usar_colores):
    colores_de_estado = {"A": AZUL, "N": NARANJA, "V": VERDE}
    lineas = []
    for fila in PLANTILLA_LOGO:
        linea = re.sub(r"#+", lambda bloque: colorear("█" * len(bloque.group()), VERDE, usar_colores), fila)
        for letra, color in colores_de_estado.items():
            linea = linea.replace(letra, colorear("●", color, usar_colores))
        lineas.append("   " + linea)
    return lineas


def dibujar_barra(progreso, usar_colores):
    llenos = int(ANCHO_BARRA * progreso)
    barra = colorear("█" * llenos, VERDE, usar_colores) + colorear("░" * (ANCHO_BARRA - llenos), GRIS, usar_colores)
    return f"   [{barra}] {int(progreso * 100):3d}%"


def mostrar_splash(duracion=1.5):
    usar_colores = sys.stdout.isatty()
    if usar_colores:
        habilitar_colores_en_windows()

    print()
    for linea in dibujar_logo(usar_colores):
        print(linea)
    print()
    print(colorear("          M E S A   D E   A Y U D A", NEGRITA, usar_colores))
    print(colorear("      Tickets de fallas · Universidad", GRIS, usar_colores))
    print()

    if not usar_colores:
        print(dibujar_barra(1, usar_colores))
        return

    pausa = duracion / (ANCHO_BARRA + 1)
    for paso in range(ANCHO_BARRA + 1):
        progreso = paso / ANCHO_BARRA
        mensaje = PASOS_DE_CARGA[min(int(progreso * len(PASOS_DE_CARGA)), len(PASOS_DE_CARGA) - 1)]
        sys.stdout.write(f"\r{dibujar_barra(progreso, usar_colores)}  {colorear(mensaje, GRIS, usar_colores):<40}")
        sys.stdout.flush()
        time.sleep(pausa)
    sys.stdout.write(f"\r{dibujar_barra(1, usar_colores)}  {colorear('¡Listo!', VERDE, usar_colores):<40}\n")
