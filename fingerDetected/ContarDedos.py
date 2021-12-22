import cv2
import time
import os
import ctypes
import DetectarMano as htm
import secuencia as s
 
termino = True
secuencia = s.secuencia()
numero_intento = 0
print(secuencia)
cap = cv2.VideoCapture(1)
wCam, hCam = 1366, 720
cap.set(3, wCam)
cap.set(4, hCam)
k=0 
reinicio = False
derrota = True
folderPath = "FingerImages"
imagePath = r'C:\\Users\\gonzalezf\\Desktop\\git\\fiestaconfluencia\\fingerDetected\\image'
myList = os.listdir(folderPath)
# print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
 
# print(len(overlayList))
pTime = 0
 
detector = htm.handDetector(detectionCon=0.90)
start_time = time.time()
tiempo_restante = 15

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

tipIds = [4, 8, 12, 16, 20]
e = 0
while termino:

    if numero_intento != 3:
        if reinicio:
            secuencia = s.secuencia()
            start_time = time.time()
            derrota = True
            reinicio = False
            k = 0
    else:
        Mbox("Derrota", "Lo siento se terminaron los intentos", 0)
        numero_intento=0
        termino = False
        cv2.destroyAllWindows()
    
    
    elapsed_time = time.time() - start_time
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    x_secuencia = 125
    y_secuencia = 40
    if elapsed_time > 15 and derrota == True:
        bad_img = cv2.imread(f'{imagePath}/derrota.jpg')
        # cv2.imshow("Derrota", bad_img)
        reinicio = True
        derrota = False
        tiempo_restante = 15
        numero_intento += 1
        Mbox('Derrota', f'Quedan {3 - numero_intento} intentos', 0)
        


    
    if len(lmList) != 0:
        fingers = []
 
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # 4 Fingers
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
                #intentar poner un tilde
                k += 1
        else:
            print("victoria")
            # ret, frame = cap.read()
            # hi,wi,_ = cv2.imread(f'{imagePath}/victoria.jpg').shape
            # ok_img = cv2.imread(f'{imagePath}/victoria.jpg')
            # frame[ 0:hi , 0:wi ] = ok_img
            # cv2.imshow("Image", frame)
            ok_img = cv2.imread(f'{imagePath}/victoria.jpg')
            # cv2.imshow("Victory", ok_img)
            # time.sleep(2)
            reinicio = True
            numero_intento = 0
            Mbox('Victoria', 'Victoria!!', 0)
            

            
            
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

 
        #cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        #cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,10, (255, 0, 0), 25)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    for num in secuencia:
        cv2.putText(img, f'{str(num)}', (x_secuencia,y_secuencia), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        x_secuencia += 40

    
    cv2.putText(img, f'Tiempo restante: {int(tiempo_restante - elapsed_time)}', (20, 450), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
