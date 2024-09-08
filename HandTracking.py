import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

fingers = [[4, 2, 0], [8, 6], [12, 10], [16, 14], [20, 18]]

def getcoord(coord):
    i = 0
    coord = [[], []]
    for hand in results.multi_hand_landmarks:
        idx = results.multi_handedness[i].classification[0].index
        if idx == 0:
            for f in range(len(hand.landmark)):
                coord[0].append((round(hand.landmark[f].x*1000), round(hand.landmark[f].y*1000)))
        if idx == 1:
            for f in range(len(hand.landmark)):
                coord[1].append((round(hand.landmark[f].x*1000), round(hand.landmark[f].y*1000)))
        getHand(idx, coord)
        i+=1
    #print(idx)
    return coord

def getHand(i, handList):
    if i == 1:
        if handList[i][fingers[0][0]][0]<handList[i][fingers[0][1]][0]:
            binary[0] = 1
        else:
            binary[0] = 0
        j = 1
        while j<5:
            if handList[i][fingers[j][0]][1] < handList[i][fingers[j][1]][1]:
                binary[j] = 1
            else:
                binary[j] = 0
            j+=1
    if i == 0:
        if handList[i][fingers[0][0]][0]>handList[i][fingers[0][1]][0]:
            binary[5] = 1
        else:
            binary[5] = 0
        j = 6
        while j<10:
            if handList[i][fingers[j-5][0]][1] < handList[i][fingers[j-5][1]][1]:
                binary[j] = 1
            else:
                binary[j] = 0
            j+=1

def getNumber(i):
    if i.count(None) != 5:
        return (sum(i))
    else:
        n = ""
        for x in i:
            if x != None:
                n += str(x)
        if n == "00000":
            return 0
        elif n == "01000":
            return 1
        elif n == "01100":
            return 2
        elif n == "11100":
            return 3
        elif n == "01111":
            return 4
        elif n == "11111":
            return 5
        elif n == "01110":
            return 6
        elif n == "01101":
            return 7
        elif n == "01011":
            return 8
        elif n == "00111":
            return 9
        elif n == "10000":
            return 10

with mp_hands.Hands() as hands:
    while cap.isOpened():
        success, image = cap.read()

        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imgRGB = cv2.flip(imgRGB, 1)
        
        results = hands.process(image)
        handList = []
        if results.multi_hand_landmarks:
            j = 0
            binary = [None]*10
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_draw.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
            handList = getcoord(handList)
            getNumber(binary)
            cv2.rectangle(image, (20, 255), (170, 425), (0, 240, 0), cv2.FILLED)
            cv2.putText(image, str(getNumber(binary)), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 20)

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()