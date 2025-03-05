import mediapipe as mp
import cv2
import csv
import os
import numpy as np

def initialise_csv(hand: str): # run twice for each hand
    num_landmarks = 21  # 21 landmark coordinates per hand
    landmarks = [hand + 'Class']  # leftClass or rightClass
    for val in range(1, num_landmarks + 1):
        landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val)]

    with open(hand + '_landmark_points.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(landmarks)

# classify the landmarks for each hand gesture and write to respective csv files (per hand)
def classify_landmarks(class_name, hand):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

    # video capture using OpenCV
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False

        results = hands.process(rgb_frame)

        rgb_frame.flags.writeable = True
        rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                num_landmarks = len(hand_landmarks.landmark)  # 21 landmarks per hand

                hand_label = results.multi_handedness[idx].classification[0].label

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f'{hand_label}',
                            (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]),
                             int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # export detected landmarks to csv
        try:
            hand_res = results.multi_hand_landmarks[0].landmark  # train one hand at a time
            hand_row = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_res]).flatten())
            hand_row.insert(0, class_name)

            with open(hand + '_landmark_points.csv', mode='a', newline='') as file:
                csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(hand_row)
        except:
            pass

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# two recognisers for left and right hands????
def gesture_recogniser(hand:str):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

    # video capture using OpenCV
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False

        results = hands.process(rgb_frame)

        rgb_frame.flags.writeable = True
        rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                num_landmarks = len(hand_landmarks.landmark) # 21 landmarks per hand

                hand_label = results.multi_handedness[idx].classification[0].label

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f'{hand_label}',
                            (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]),
                             int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()









def gesture_recogniser2(hand:str):  # to keep track
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

    # video capture using OpenCV
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False

        results = hands.process(rgb_frame)

        rgb_frame.flags.writeable = True
        rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                num_landmarks = len(hand_landmarks.landmark) # 21 landmarks per hand

                hand_label = results.multi_handedness[idx].classification[0].label

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f'{hand_label}',
                            (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]),
                             int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # option to choose either the left or right hand
    # initialise the csv file
    hands = ["left", "right"]
    '''for hand in hands: 
        initialise_csv(hand)'''

    # class_names = ["rock", "paper", "scissors"]
    # classify_landmarks("scissors", "right")
    # classify_landmarks(class_names[0], hands[0])


    # gesture_recogniser(hand)



# user should first choose if using left or right hand?
