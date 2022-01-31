import cv2
import time
import os
import wave
import ctypes
import random

cantidad_ganadores = 6
tiempo_de_sorteo = 10
terminar = True
ganador = False
sorteoPath = "sorteo"
ganadorPath = "ganadores"
numeros_ganadores = []
puestos_ganadores = []
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

def switch(argument):
    switcher = {
        1: "Primer Puesto",
        2: "Segundo Puesto",
        3: "Tercer Puesto",
        4: "Cuarto Puesto",
        5: "Quinto Puesto",
        6: "Sexto Puesto",
        7: "Septimo Puesto",
        8: "Octavo Puesto",
        9: "Noveno Puesto",
        10: "Decimo Puesto"
    }

    return switcher.get(argument)

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


while terminar and (len(numeros_ganadores) < cantidad_ganadores):
    
    elapsed_time = time.time() - start_time

    if ((int)(tiempo_de_sorteo - elapsed_time)) == 0:
        if(rnd not in numeros_ganadores):
            numeros_ganadores.append(rnd)
            height, width, channels = img.shape
            # cv2.rectangle(img, (int(width*0.13), int(height*0.10)), (int(width*0.51), int(height*0.20)), (178,105,3), cv2.FILLED)
            # cv2.putText(img, f'Puesto: {len(numeros_ganadores)}', (int(width*0.17), int(height*0.17)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
        
        etiqueta = switch(len(numeros_ganadores))
        if(etiqueta not in puestos_ganadores):
            puestos_ganadores.append(etiqueta)
        cv2.imwrite(f'{ganadorPath}/{etiqueta}.jpg',img)
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


for imagenes in puestos_ganadores:
    cv2.imshow(str(imagenes), cv2.imread(f'{ganadorPath}/{imagenes}.jpg'))
    
cv2.waitKey(0)