import cv2
import time
import os
import pyaudio
import wave
import ctypes
import imutils
import numpy as np
import json
import cgi
import DetectarMano as htm
import secuencia as s
import argparse
import datetime
from multiprocessing import Process
from flask import Response
from flask import request
from flask import Flask
from flask import render_template
from tkinter import *
from tkinter import simpledialog
from tkinter.messagebox import askyesno
from tkinter import Tk
from tkinter.messagebox import Message 
from _tkinter import TclError

app = Flask(__name__)



def guardar_ganador(img_temp,img_temporal,width,height,nombre,user_insta,numero_participante):
    # guardar 2 fotos al momento de la victoria del jugador, una con los datos completos y otra con datos editados para poder mostrar en el sorteo 
    user_insta = "@" + user_insta
    user_editado = "@"
    user_longitud = len(user_insta)
    mitad_long = user_longitud // 2
    if user_insta != "@":
        s = (user_insta)
        b = list(s)
        largo = len(b)
        for x in range(mitad_long):
            b[largo - (x+1)] = "X"
        user_editado = "".join(b)
    cv2.rectangle(img_temp, (int(width*0.05), int(height*0.70)), (int(width*0.5), int(height*0.95)), (178,105,3), cv2.FILLED)
    cv2.putText(img_temp, f'Nombre: {str(nombre)}', (int(width*0.1), int(height*0.80)), cv2.FONT_HERSHEY_DUPLEX,1, (255, 255, 255), 2)
    cv2.putText(img_temp, f'IG: {str(user_editado)}', (int(width*0.1), int(height*0.90)), cv2.FONT_HERSHEY_DUPLEX,1, (255, 255, 255), 2)
    cv2.rectangle(img_temporal, (int(width*0.05), int(height*0.70)), (int(width*0.5), int(height*0.95)), (178,105,3), cv2.FILLED)
    cv2.putText(img_temporal, f'Nombre: {str(nombre)}', (int(width*0.1), int(height*0.80)), cv2.FONT_HERSHEY_DUPLEX,1, (255, 255, 255), 2)
    cv2.putText(img_temporal, f'IG: {str(user_insta)}', (int(width*0.1), int(height*0.90)), cv2.FONT_HERSHEY_DUPLEX,1, (255, 255, 255), 2)
    cv2.imwrite(f'sorteo/{numero_participante}.jpg',img_temp)
    cv2.imwrite(f'participantes/{numero_participante}.jpg',img_temporal)

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

def gen_frames():

    ws = Tk()
    ws.withdraw()
    nombre = ""
    manoHabil = ""
    user_insta = ""
    h = "0"
    w = "0"
    termino = True
    inicio = True
    ganador = False
    primerEjecucion = True
    guardar = True
    secuencia = s.secuencia()
    numero_intento = 0
    mano = "derecha"
    staticPath = "static"
    logo = cv2.imread(f'{staticPath}/logito.png')
    print(secuencia)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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
    myList = os.listdir(folderPath)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    
    pTime = 0


    detector = htm.handDetector(detectionCon=0.90)
    start_time = time.time()
    tiempo_restante = tiempo_de_juego

    while termino:

        

        if primerEjecucion:
            preguntaParticipantes = Tk()
            preguntaParticipantes.withdraw()
            respuesta = askyesno(title='Pregunta', message='Reiniciar numero de participantes?')
            if respuesta:
                print("si")
                numero_participante = 1
                try:
                    parti_file = open("participantes.txt",'w')
                    print(numero_participante,file=parti_file)
                    parti_file.close()
                except IOError:
                    print("File error")
                
            primerEjecucion = False

        if inicio:
            nombre = simpledialog.askstring("Input", "Nombre",parent=ws)
            user_insta = simpledialog.askstring("Input", "Usuario de Instagram",parent=ws)
            localidad = simpledialog.askstring("Input", "Localidad", parent=ws).lower()
            manoHabil = simpledialog.askstring("Input", "Mano Habil", parent=ws).lower()
            inicio = False
            ganador = False

        if numero_intento != 3:
            if reinicio:
                secuencia = s.secuencia()
                start_time = time.time()
                derrota = True
                reinicio = False
                ganador = False
                k = 0
        else:
            Mensaje("Derrota", "Lo siento se terminaron los intentos", 5)
            numero_intento=0
            inicio = True
        
        elapsed_time = time.time() - start_time
        success, img = cap.read()
        succ, img_temp = cap.read()
        succes, img_temporal = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


        if elapsed_time > tiempo_de_juego and derrota == True:
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
                Mensaje('Victoria', 'Victoria!!', 5)
                h_l, w_l, c = logo.shape
                
                img_temp[515:h_l+515 , 811:w_l+811] = logo
                img_temporal[515:h_l+515 , 811:w_l+811] = logo
                guardar_ganador(img_temp,img_temporal,width,height,nombre,user_insta,numero_participante)
                numero_participante +=1
                reinicio = True
                ganador = True
                inicio = True
                # termino = False
                if ganador:
                    img_ganador = cv2.imread(f'{staticPath}/fondo-ganaste.jpg')
                    img = img_ganador
                    ret, buffer = cv2.imencode('.jpg', img)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
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

        x_secuencia = int(width*0.17)
        y_secuencia = int(height*0.17)

        cv2.rectangle(img, (int(width*0.13), int(height*0.10)), (int(width*0.51), int(height*0.20)), (178,105,3), cv2.FILLED)

        for num in secuencia:
            cv2.putText(img, f'{str(num)}', (x_secuencia,y_secuencia), cv2.FONT_HERSHEY_DUPLEX,1.3,(255,255,255),2)
            x_secuencia += 40


        cv2.rectangle(img, (int(width*0.04), int(height*0.85)), (int(width*0.45), int(height*0.95)), (178,105,3), cv2.FILLED)
        cv2.putText(img, f'Tiempo restante: {int(tiempo_restante - elapsed_time)}', (int(width*0.08), int(height*0.92)), cv2.FONT_HERSHEY_DUPLEX,1.3, (255, 255, 255), 2)    


        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)




@app.route("/", methods=["GET", "POST"])
def index():
    form = cgi.FieldStorage()
    
    return render_template("index.html")

@app.route("/sorteo")
def messages():
    return render_template("sorteo.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        missing = []
        inputs = []
        print(request.form)
        fields = ['nombre', 'telefono', 'mano']
        for field in fields:
            value = request.form.get(field, None)
            if value is None or value == '':
                missing.append(field)
            else:
                inputs.append(value)
                # print(value)
        if not missing:
            return render_template('index.html', inputs=inputs)
    return render_template("login.html")


@app.route('/video_feed', methods=["GET","POST"])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# check to see if this is the main thread of execution
if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
    
	app.run(host=args["ip"], port=args["port"], debug=True, use_reloader=True)
