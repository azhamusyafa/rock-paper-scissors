import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

# Initialize webcam
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Initialize hand detector
detector = HandDetector(maxHands=1)

# Initialize variables
timer = 0
stateResult = False
MulaiGame = False
scores = [0, 0]

while True:
    mbg = cv2.imread("D:/projekanges/suit/gambar/bg.png")
    success, img = cam.read()

    imgs = cv2.resize(img, (0, 0), None, 0.950, 0.940)
    imgs = imgs[:, 130:500]

    # Detect hands
    hands, img = detector.findHands(imgs)

    # Display instructions to start the game
    if not MulaiGame:
        cv2.putText(mbg, "Press 's' to start the game", (300, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    if MulaiGame:
        if stateResult == False:
            timer = time.time() - initialTime
            cv2.putText(mbg, str(int(timer)), (605, 88), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                    # AI's random move
                    randomGambar = random.choice(['b.png', 'g.png', 'k.png'])
                    imgAI = cv2.imread(f"D:/projekanges/suit/gambar/{randomGambar}", cv2.IMREAD_UNCHANGED)
                    mbg = cvzone.overlayPNG(mbg, imgAI, (309, 310))

                    # Determine winner
                    if (playerMove == 1 and randomGambar == 'g.png') or \
                       (playerMove == 2 and randomGambar == 'b.png') or \
                       (playerMove == 3 and randomGambar == 'k.png'):
                        scores[1] += 1  # Player wins
                    elif (playerMove == 1 and randomGambar == 'k.png') or \
                         (playerMove == 2 and randomGambar == 'g.png') or \
                         (playerMove == 3 and randomGambar == 'b.png'):
                        scores[0] += 1  # AI wins

                    # Check if either player has won
                    if scores[0] == 3:
                        cv2.putText(mbg, "You Lose!", (450, 400), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)
                        cv2.imshow("background", mbg)
                        cv2.waitKey(0)  # Wait until any key is pressed
                        scores = [0, 0]  # Reset scores
                        MulaiGame = False  # Restart the game
                    elif scores[1] == 3:
                        cv2.putText(mbg, "Congratulations, You Win!", (150, 400), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
                        cv2.imshow("background", mbg)
                        cv2.waitKey(0)  # Wait until any key is pressed
                        scores = [0, 0]  # Reset scores
                        MulaiGame = False  # Restart the game

    mbg[205:656, 685:1055] = imgs

    # Display AI's move
    if stateResult:
        mbg = cvzone.overlayPNG(mbg, imgAI, (309, 310))

    # Display scores
    cv2.putText(mbg, str(scores[0]), (529, 156), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(mbg, str(scores[1]), (987, 156), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Show the images
    cv2.imshow("background", mbg)

    # Start game when 's' is pressed
    key = cv2.waitKey(1)
    if key == ord('s'):
        MulaiGame = True
        initialTime = time.time()
        stateResult = False
