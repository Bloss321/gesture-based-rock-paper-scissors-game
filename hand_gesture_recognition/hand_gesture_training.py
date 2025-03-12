import mediapipe as mp
import cv2
import csv
import os
import numpy as np
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score

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


def train_model(hand: str):
    # read data
    data_frame = pd.read_csv(hand + '_landmark_points.csv')

    X = data_frame.drop(hand + 'Class', axis = 1) # features
    y = data_frame[hand + 'Class'] # target value
    # create training and testing partitions
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

    pipelines = {
        'lr': make_pipeline(StandardScaler(), LogisticRegression()),
        'rc': make_pipeline(StandardScaler(), RidgeClassifier()),
        'rf': make_pipeline(StandardScaler(), RandomForestClassifier()),
        'gb': make_pipeline(StandardScaler(), GradientBoostingClassifier()),
    }

    # train models for all the above pipelines
    fit_models = {}
    for algorithm, pipeline in pipelines.items():
        model = pipeline.fit(X_train, y_train)
        fit_models[algorithm] = model

    train_test = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }

    return fit_models, train_test


def train_and_evaluate_model(hand: str):
    fit_models, train_test = train_model(hand)

    for algorithm, model in fit_models.items():
        yhat = model.predict(train_test.get("X_test"))
        print(algorithm, accuracy_score(train_test.get("y_test"), yhat))

        '''
        Results: 
        lr 0.9944576405384006
        rc 0.9912905779889153
        rf 0.9920823436262867
        gb 0.9920823436262867
        '''

    with open(hand + '_hand_gestures.pkl', 'wb') as file:
        pickle.dump(fit_models['rf'], file)

    return None


def gesture_recogniser(hand:str):
    with open(hand + '_hand_gestures.pkl', 'rb') as file:
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
    # option to choose either the left or right hand
    # initialise the csv file
    hands = ["left", "right"]
    # class_names = ["rock", "paper", "scissors"]

    # Step 1: initialise the csv files to store data per hand
    '''for hand in hands: 
        initialise_csv(hand)'''

    # Step 2
    # classify_landmarks("scissors", "right")
    # classify_landmarks(class_names[0], hands[0])

    # Step 3
    # train_and_evaluate_model("right")

    # Step 4: test trained model live
    gesture_recogniser("right")
