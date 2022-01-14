import cv2
import time
import os
import HandTrackingModule as htm

##############################
wCam, hCam = 1080, 940
##############################
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)  # video object created
cap.set(3, wCam)
cap.set(4, hCam)


folderPath = "fingers"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
detector = htm.handDetector(detectionCon=0.7)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()  # this will give frame
    img = detector.findHands(img)
    hand_type, img = detector.get_label(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = []
        if hand_type == 'Right':
            # thumb
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] > lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalFingers = fingers.count(1)
            print(totalFingers)

        if hand_type == 'Left':
                # thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalFingers = fingers.count(1)
            print(totalFingers)

        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]
        cv2.putText(img, str(totalFingers), (500, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0),
                    3)

    cTime = time.time()  # getting current time
    fps = 1 / (cTime - pTime)  # getting fps
    pTime = cTime

    cv2.putText(img, str(int(fps)), (700, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0),
                3)  # placing the fps meter on
    # on the screen with inbuilt parameters
    cv2.imshow("Image", img)  # for showing in the webcam to run it
    cv2.waitKey(1)