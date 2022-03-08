import cv2
import mediapipe as mp
import time

from pynput.keyboard import Key, Controller
keyboard = Controller()

spaceKeyPressed = Key.space
upArrowKeyPresssed = Key.up
downArrowKeyPresssed = Key.down
time.sleep(2.0)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands


tipIds=[4,8,12,16,20]
 
video = cv2.VideoCapture(0)

with mp_hand.Hands(max_num_hands = 1,
                min_detection_confidence = 0.5,
               min_tracking_confidence = 0.5) as hands:
    while True:
        keyPressed = False

        spacePressed = False
        upArrowPresssed = False
        downArrowPressed = False
 
        key_count = 0
        key_pressed = 0
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        landmarkList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                initialHandPos = results.multi_hand_landmarks[0] #starting point of hand landmark
                # for id, lm in enumerate(myHands.landmark):
                #     h,w,c=image.shape
                #     cx,cy= int(lm.x*w), int(lm.y*h)
                #     lmList.append([id,cx,cy])

                for point, landMark in enumerate(initialHandPos.landmark):
                    heigh, width, color = image.shape
                    cordinateX, cordinateY = int(landMark.x * width), int(landMark.y * heigh)
                    # print(cordinateX, cordinateY)
                    landmarkList.append([point, cordinateX, cordinateY])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
                # print("+++++++++++++++++++++++++", landmarkList)
        fingers = []
        if len(landmarkList) != 0:
            if landmarkList[tipIds[0]][1] > landmarkList[tipIds[0] - 2][1]:
                # print("Thumb Up")
                fingers.append(1)
            else:
                fingers.append(0)
            for i in range(1, 5): # index 0 for thumb
                if landmarkList[tipIds[i]][2] < landmarkList[tipIds[i] - 2][2]:
                    # print("Open")
                    fingers.append(1)
                else:
                    # print("Closed")
                    fingers.append(0)
            
            totalFingers = fingers.count(1)
            # print(totalFingers)

            if(totalFingers == 5):
                print("Open")
                # time.sleep(1.0)
                keyboard.press(spaceKeyPressed)
                spacePressed = True
                current_key_pressed.add(spaceKeyPressed)
                key_pressed=spaceKeyPressed
                keyPressed = True
                key_count=key_count+1
                # time.sleep(1.0)
                # 
            elif totalFingers == 1 and landmarkList[8][2] < landmarkList[6][2]:
                print("Open Index")
                keyboard.press(upArrowKeyPresssed)
                upArrowPresssed = True
                current_key_pressed.add(upArrowKeyPresssed)
                key_pressed=upArrowKeyPresssed
                keyPressed = True
                key_count=key_count+1
            elif totalFingers == 2 and landmarkList[12][2] < landmarkList[10][2] and landmarkList[8][2] < landmarkList[6][2]:
                print("Open Index and Middle")
                keyboard.press(downArrowKeyPresssed)
                downArrowPresssed = True
                current_key_pressed.add(downArrowKeyPresssed)
                key_pressed=downArrowKeyPresssed
                keyPressed = True
                key_count=key_count+1
            elif(totalFingers == 0):
                print("Closed")
                # pass
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                keyboard.release(key)
            # time.sleep(2.0)
            current_key_pressed = set()
        elif key_count == 1 and len(current_key_pressed) == 2:    
            for key in current_key_pressed:              
                if key_pressed != key:
                    keyboard.release(key)
            # time.sleep(2.0)
            current_key_pressed = set()
            for key in current_key_pressed:
                keyboard.release(key)
            # time.sleep(2.0)
            current_key_pressed = set()
      
       	cv2.imshow("Frame", image)
        handleCamWindow = cv2.waitKey(1)
        if handleCamWindow == ord('q'):
        	break
video.release()
cv2.destroyAllWindows()

