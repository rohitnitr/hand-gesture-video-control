import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# solution APIs
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Volume Control Library Usage
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol, volBar, volPer = volRange[0], volRange[1], 400, 0

# Webcam Setup
wCam, hCam = 640, 480
cam = cv2.VideoCapture(2)
cam.set(3, wCam)
cam.set(4, hCam)

# Mediapipe Hand Landmark Model
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    # Start the Chrome web driver
    selenium_service = Service(r'C:\Users\91891\Desktop/chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=selenium_service)

    # Open YouTube video in web browser
    video_url = "https://www.youtube.com/watch?v=6RrEQJNZwPQ&ab_channel=SHUBHl"
    driver.get(video_url)

    # Variables for hand status and pause/resume message
    hand_open = True
    pause_message = ""
    resume_message = ""
    resume_message_start_time = 0
    resume_message_duration = 0.5

    # Flag to keep track of video playback state
    video_paused = False

    while cam.isOpened():
        success, image = cam.read()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        # multi_hand_landmarks method for Finding position of Hand landmarks
        lmList = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        # Assigning variables for Thumb and Index finger position
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # Marking Thumb and Index finger
            hand_color = (0, 0, 255)  # Default red color for closed hand
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 50:
                hand_color = (0, 255, 0)  # Green color for open hand

            cv2.circle(image, (x1, y1), 15, hand_color, cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, hand_color, cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), hand_color, 3)

            vol = np.interp(length, [50, 220], [0, 100])
            volBar = np.interp(length, [50, 220], [400, 150])
            volume.SetMasterVolumeLevelScalar(vol / 100, None)

        # Assigning variables for Thumb and Index finger position
        if len(lmList) != 0:
            # Index finger landmarks
            index_finger_tip = lmList[8]
            index_finger_base = lmList[5]

            # Middle finger landmarks
            middle_finger_tip = lmList[12]
            middle_finger_base = lmList[9]

            # Ring finger landmarks
            ring_finger_tip = lmList[16]
            ring_finger_base = lmList[13]

            # Little finger landmarks
            little_finger_tip = lmList[20]
            little_finger_base = lmList[17]

            # Check if hand is open or closed
            if (index_finger_tip[2] > index_finger_base[2]) and \
                    (middle_finger_tip[2] > middle_finger_base[2]) and \
                    (ring_finger_tip[2] > ring_finger_base[2]) and \
                    (little_finger_tip[2] > little_finger_base[2]):
                hand_status = "Closed Hand"
                if hand_open:
                    if not video_paused:
                        # Pause the video
                        video = driver.find_element(By.CSS_SELECTOR, 'video')
                        ActionChains(driver).move_to_element(video).click().perform()
                        video_paused = True
                        pause_message = "Video Paused"
                    hand_open = False
            else:
                hand_status = "Open Hand"
                if not hand_open:
                    if video_paused:
                        # Resume the video
                        video = driver.find_element(By.CSS_SELECTOR, 'video')
                        ActionChains(driver).move_to_element(video).click().perform()
                        video_paused = False
                        resume_message = "Video Resumed"
                        resume_message_start_time = time.time()
                hand_open = True

            # Display hand status on the image
            text_color = (0, 0, 255)  # Red color for closed hand status
            if hand_status == "Open Hand":
                text_color = (0, 255, 0)  # Green color for open hand status

            cv2.putText(image, hand_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

            # Volume Bar
            volPer = int(volume.GetMasterVolumeLevelScalar() * 100)

            if volPer <= 80:
                volBarColor = (0, 255, 0)  # Green color
            else:
                volBarColor = (0, 0, 255)  # Red color

            cv2.rectangle(image, (50, 150), (85, 400), (0, 0, 0), 3)
            cv2.rectangle(image, (50, int(volBar)), (85, 400), volBarColor, cv2.FILLED)
            cv2.putText(image, f'{volPer} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), 3)

        # Display the pause and resume messages if hand is closed or open, respectively
        if not hand_open:
            cv2.putText(image, pause_message, (wCam - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif resume_message != "":
            cv2.putText(image, resume_message, (wCam - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the resume message for 1 second after transition from closed to open hand
        if resume_message != "" and (time.time() - resume_message_start_time) < resume_message_duration:
            cv2.putText(image, resume_message, (wCam - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            resume_message = ""

        cv2.imshow('handDetector', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    driver.quit()




