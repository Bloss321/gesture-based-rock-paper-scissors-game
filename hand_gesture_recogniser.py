import pickle

import mediapipe as mp
import cv2
import numpy as np
import pandas as pd


def gesture_recogniser(hand:str):
    with open('hand_gesture_recognition/' + hand + '_hand_gestures.pkl', 'rb') as file:
        model = pickle.load(file)

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

                # Estimate hand gestures based on model
                try:
                    hand_res = results.multi_hand_landmarks[0].landmark  # train one hand at a time
                    hand_row = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_res]).flatten())

                    X = pd.DataFrame([hand_row])
                    hand_gesture_class = model.predict(X)[0]
                    hand_gesture_probability = model.predict_proba(X)[0]
                    print(hand_gesture_class, hand_gesture_probability)

                    # print hand (left/right) and gesture to the screen
                    cv2.putText(frame, f'{hand_label}: ' + hand_gesture_class,
                                (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]),
                                 int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                except:
                    pass

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    gesture_recogniser("right")



# user should first choose if using left or right hand?
