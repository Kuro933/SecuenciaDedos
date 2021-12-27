import random
from copy import deepcopy
from colorama import init, Fore, Style
import cv2

MINIMO_FILAS = 5
MAXIMO_FILAS = 10
MINIMO_COLUMNAS = 6
MAXIMO_COLUMNAS = 10
ESPACIO_VACIO = " "
COLOR_1 = "x"
COLOR_2 = "o"
JUGADOR_1 = 1
# La CPU también es el jugador 2
JUGADOR_2 = 2
CONECTA = 4
ESTA_JUGANDO_CPU = False
cap = cv2.VideoCapture(0)
wCam, hCam = 1366, 720
cap.set(3, wCam)
cap.set(4, hCam)
def solicitar_columnas():
    return 6
    # while True:
    #     columnas = solicitar_entero_valido("Ingresa el número de columnas:")
    #     if columnas < MINIMO_COLUMNAS or columnas > MAXIMO_COLUMNAS:
    #         print(f"El mínimo de columnas es {MINIMO_COLUMNAS} y el máximo {MAXIMO_COLUMNAS}")
    #     else:
    #         return columnas


def solicitar_filas():
    return 6
    # while True:
    #     filas = solicitar_entero_valido("Ingresa el número de filas:")
    #     if filas < MINIMO_FILAS or filas > MAXIMO_FILAS:
    #         print(f"El mínimo de filas es {MINIMO_FILAS} y el máximo {MAXIMO_FILAS}")
    #     else:
    #         return filas


def crear_tablero(filas, columnas):
    tablero = []
    for fila in range(filas):
        tablero.append([])
        for columna in range(columnas):
            tablero[fila].append(ESPACIO_VACIO)
    return tablero


def imprimir_tablero(tablero, img, height, width):
    # Imprime números de columnas   
    x = 0.05
    y = 0.10

    print("|", end="")
    r = "| "
    cv2.putText(img, f'{r}', (int(width), int(height)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    for f in range(1, len(tablero[0]) + 1):
        cv2.putText(img, f'|{f}|', (int(width*x), int(height*y)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
        x += 0.05
        print(f, end="|")
    print("")
    # Datos
    y+= 0.10
    x = 0.05
    for fila in tablero:
        print("|", end="")
        for valor in fila:
            cv2.putText(img, f'|{valor}|', (int(width*x), int(height*y)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
            x += 0.05
            color_terminal = Fore.GREEN
            if valor == COLOR_2:
                color_terminal = Fore.RED
            print(color_terminal + valor, end="")
            print(Style.RESET_ALL, end="")
            print("|", end="")
        print("")
    # Pie
    print("+", end="")
    for f in range(1, len(tablero[0]) + 1):
        print("-", end="+")
    print("")


while True:
    tablero = crear_tablero(6,6)
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    success, img = cap.read()
    imprimir_tablero(tablero,img,height,width)
    x_secuencia = 125
    y_secuencia = 40
    cv2.imshow("Image", img)
    cv2.waitKey(1)
