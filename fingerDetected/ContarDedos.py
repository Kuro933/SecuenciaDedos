import cv2
import time
import os
# import pyaudio
import wave
import ctypes
import DetectarMano as htm
import secuencia as s
from tkinter import *
from tkinter import simpledialog
from tkinter import Tk
from tkinter.messagebox import Message 
from _tkinter import TclError


ws = Tk()
ws.withdraw()
nombre = ""
manoHabil = ""
numero_telefono = ""
termino = True
inicio = True
guardar = True
secuencia = s.secuencia()
numero_intento = 0
mano = "derecha"
print(secuencia)
cap = cv2.VideoCapture(0)
wCam, hCam = 1366, 720
cap.set(3, wCam)
cap.set(4, hCam)
tiempo_de_juego = 10
try:
    data = open("participantes.txt")
    for dato in data:
        numero_participante = int(dato)
    
    data.close()
except IOError:
    print("no se pudo")

k=0 
reinicio = False
derrota = True
folderPath = "FingerImages"
sorteito = "sorteo"
imagePath = r'C:\\Users\\gonzalezf\\Desktop\\git\\fiestaconfluencia\\SecuenciaDedos\\fingerDetected\\image'
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
 
pTime = 0


detector = htm.handDetector(detectionCon=0.90)
start_time = time.time()
tiempo_restante = tiempo_de_juego

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def Mensaje(title, text, time):
    root = Tk()
    root.withdraw()
    try:
        root.after((time*1000), root.destroy) 
        Message(title=title, message=text, master=root).show()
    except TclError:
        pass

tipIds = [4, 8, 12, 16, 20]
e = 0
while termino:

    if inicio:
        nombre = simpledialog.askstring("Input", "Nombre",parent=ws)
        if nombre is not None:
            numero_telefono = simpledialog.askstring("Input", "Número de telefono",parent=ws)
            print("Tu nombre es: ", nombre)
            print("Tu telefono es: ", numero_telefono)
            inicio = False
            manoHabil = simpledialog.askstring("Input", "Mano Habil", parent=ws).lower()

    if numero_intento != 3:
        if reinicio:
            secuencia = s.secuencia()
            start_time = time.time()
            derrota = True
            reinicio = False
            k = 0
    else:
        Mensaje("Derrota", "Lo siento se terminaron los intentos", 5)
        numero_intento=0
        inicio = True
        # termino = False
        # cv2.destroyAllWindows()
    
    
    elapsed_time = time.time() - start_time
    success, img = cap.read()
    succ, img_temp = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    x_secuencia = 125
    y_secuencia = 40
    if elapsed_time > tiempo_de_juego and derrota == True:
        bad_img = cv2.imread(f'{imagePath}/derrota.jpg')
        reinicio = True
        derrota = False
        tiempo_restante = tiempo_de_juego
        numero_intento += 1
        Mensaje('Derrota', f'Quedan {3 - numero_intento} intentos, proximo en 5 segundos', 5)

        
    if len(lmList) != 0:
        fingers = []

        if manoHabil == "izquierda" or manoHabil == "zurda" or manoHabil == "izquierdo" or manoHabil == "zurdo" or manoHabil == "izq":
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        
            # 4 dedos
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        else:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
     
        # 4 dedos
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        
        longitud = len(secuencia)
        if k < longitud:            
            if (totalFingers) == secuencia[k]:
                print("vamoo")
                print("secuencia ", secuencia)
                secuencia[k] = 'si'
                k += 1
        else:
            print("victoria")
            ok_img = cv2.imread(f'{imagePath}/victoria.jpg')
            Mensaje('Victoria', 'Victoria!!', 5)

            cv2.putText(img_temp, f'Nombre: {str(nombre)}', (int(width*0.5), int(height*0.80)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
            cv2.putText(img_temp, f'Telefono: {str(numero_telefono)}', (int(width*0.5), int(height*0.90)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
            cv2.imwrite(f'{sorteito}/{numero_participante}.jpg',img_temp)
            numero_participante +=1
            reinicio = True
            inicio = True
            numero_intento = 0
            try:
                participante_file = open("participantes.txt",'w')
                print(numero_participante,file=participante_file)
                participante_file.close()
            except IOError:
                print("File error")
            
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    for num in secuencia:
        cv2.putText(img, f'{str(num)}', (x_secuencia,y_secuencia), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        x_secuencia += 40

    cv2.putText(img, f'Tiempo restante: {int(tiempo_restante - elapsed_time)}', (int(width*0.05), int(height*0.90)), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)    

    cv2.imshow("Image", img)
    cv2.waitKey(1)
