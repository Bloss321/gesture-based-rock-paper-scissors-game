import mediapipe as mp
import cv2


def gesture_recogniser():
    mp_drawing = mp.solutions.drawing_utils
    mp_hand_sol = mp.solutions.hands

    # video capture using OpenCV
    cap = cv2.VideoCapture(0)


# user should first choose if using left or right hand?
