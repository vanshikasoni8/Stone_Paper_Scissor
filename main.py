import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random


# installed webcam
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False

startGame = False
score = [0,0]   # AI and you

while True:
# put background
    imgBg= cv2.imread("Resources/BG.png")
    success, img = cap.read()

# scaled image
    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled= imgScaled[:,80:480]

    

# find hands
    hands, img= detector.findHands(imgScaled)
    
    if startGame:

        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBg,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)
            
            if timer>3 :
                stateResult =True
                timer = 0
                if hands:
                    hand= hands[0]
                    fingers= detector.fingersUp(hand)
                    if fingers ==[0,0,0,0,0]:
                        playerMove = 1
                    if fingers ==[1,1,1,1,1]:
                        playerMove = 2
                    if fingers ==[0,1,1,0,0]:
                        playerMove = 3

                    randomNumer= random.randint(1,3)
                    imgAI = cv2.imread(f'Resources/{randomNumer}.png',cv2.IMREAD_UNCHANGED) 
                    imgBg = cvzone.overlayPNG(imgBg,imgAI,(149,310))


                    # player wins 
                    if (playerMove ==1 and randomNumer == 3) or \
                       (playerMove == 2 and randomNumer == 1) or \
                       (playerMove ==3 and randomNumer==2):
                       score[1] +=1

                    # AI wins
                    if (playerMove ==3 and randomNumer == 1) or \
                       (playerMove == 1 and randomNumer == 2) or \
                       (playerMove ==2 and randomNumer==3):
                       score[0] +=1  
    

                    # print(playerMove)
                    
        


    

# put image in the background
    imgBg[233:653 ,795:1195] = imgScaled

    if stateResult:
        imgBg = cvzone.overlayPNG(imgBg, imgAI, (149,310))

    cv2.putText(imgBg,str(int(score[0])),(410,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv2.putText(imgBg,str(int(score[1])),(1112,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,0),6)
    # cv2.imshow("Image",img)
    cv2.imshow("BG ",imgBg)
    # cv2.imshow("Scaled ",imgScaled) 


 
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False

