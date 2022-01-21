import cv2
import time
import os
import wave
import ctypes
import random

cantidad_ganadores = 3
tiempo_de_sorteo = 10
terminar = True
ganador = False
sorteoPath = "sorteo"
ganadorPath = "ganadores"
numeros_ganadores = []
cantidad_fotos = 0
miLista = os.listdir(sorteoPath)
overlayList = []
for imgPath in miLista:
    # print(imgPath)
    image = cv2.imread(f'{sorteoPath}/{imgPath}')
    overlayList.append(image)
    cantidad_fotos += 1

start_time = time.time()


pasar_foto = 0

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


while terminar and (len(numeros_ganadores) < cantidad_ganadores):
    
    elapsed_time = time.time() - start_time

    if ((int)(tiempo_de_sorteo - elapsed_time)) == 0:
        if(rnd not in numeros_ganadores):
            numeros_ganadores.append(rnd)
            height, width, channels = img.shape
            cv2.putText(img, f'Puesto: {len(numeros_ganadores)}', (int(width*0.05), int(height*0.90)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
        if (len(numeros_ganadores) == 1):
            etiquieta = "Primer Puesto"
        elif (len(numeros_ganadores) == 2):
            etiquieta = "Segundo Puesto"
        else:
            etiquieta = "Tercer Puesto"
        cv2.imwrite(f'{ganadorPath}/{etiquieta}.jpg',img)
        tiempo_de_sorteo = 10
        

    if (((int)(pasar_foto)) % 20 == 0) and not ganador:
        rnd = (random.randrange(0,cantidad_fotos) + 1)
        if len(numeros_ganadores) > 0:
            if (rnd not in numeros_ganadores):
                img = cv2.imread(f'{sorteoPath}/{rnd}.jpg')
        else:
            img = cv2.imread(f'{sorteoPath}/{rnd}.jpg')
            
    pasar_foto += 1
    cv2.imshow('sorteo', img)
    cv2.waitKey(1)
