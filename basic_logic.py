import math
import pickle
import random

import cv2
import numpy as np
import pandas as pd
import pygame
import time

import mediapipe as mp
import warnings

from assets.countdown.game_countdown import start_game_countdown

pygame.init()

display_width = 1000
display_height = 600
display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("AI Rock Paper Scissors Game")
background_colour = (51, 102, 153)

options = ["rock", "paper", "scissors"]

player_window_dimensions = (300, 300)

def display_score(score: int):
    white = (255, 255, 255)
    score_font = pygame.font.SysFont("Cooper", 50)
    score_text = score_font.render(str(score), True, white)
    display.blit(score_text, (display_width / 2.1, display_height / 9))

def display_game_message(message: str):
    start_message_timer = time.time()
    if time.time() - start_message_timer < 1:
    # display.fill(background_colour)
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        over_text = game_over_font.render(message, True, (255, 255, 255))
        display.blit(over_text, (100, 200))
    # pygame.time.delay(1000)

def get_user_input():
    user_input = input("Enter choice: ")
    if user_input not in options:
        display_game_message("Invalid game input! Try again.")
        # print("Invalid game input! Try again.")
        get_user_input()
    return user_input

def check_if_game_over(player, score):
    if score < 500:
        return False
    else:
        display_game_message(player + " has won the game!")
        print("\n", player, " has won the game!")
        print("User Score: " + str(score))
        print("Computer Score: " + str(score))
        return True

def resize_video_output(frame, scale):  # scale given as decimal e.g. 0.75
    height = int(frame.shape[0] * scale)
    width = int(frame.shape[1] * scale)
    new_dimension = (width, height)
    return cv2.resize(frame, new_dimension, interpolation=cv2.INTER_AREA)

def run_game():
    computer_score = 0
    user_score = 0
    game_running = True
    frame_count = 0
    # rps_countdown = 0  # rock paper scissors countdown before player move - every 3 (4) seconds

    clock = pygame.time.Clock()

    computer_hand_pos = (200, 200)  # width, height
    hand_sign_images = {
        "rock": pygame.image.load('assets/images/rock_sign.png'),
        "paper": pygame.image.load('assets/images/paper_sign.png'),
        "scissors": pygame.image.load('assets/images/scissors_sign.png')
    }

    # initialise mediapipe
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(0)

    # hand gesture recognition model
    warnings.filterwarnings('ignore',
                            message="X does not have valid feature names, but StandardScaler was fitted with feature names",
                            category=UserWarning)
    hand = "right"  # later add in option for player to choose hand, or process both
    with open('hand_gesture_recognition/' + hand + '_hand_gestures.pkl', 'rb') as file:
        model = pickle.load(file)

    # start = time.time()   # Every three seconds capture movement, if neutral, they lose -
    # too slow! message pops up
    # The words Rock --> Paper --> Scissors, should appear sequentially each second
    # then for 1.5 seconds

    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
        start = time.time()
        while game_running:
            frame_count += 1
            print(frame_count)

            display.fill(background_colour)
            display_score(user_score)

            # seconds 1-3, second 4: player move, second 5: round message, then repeat
            # consider 5-second cycles

            # if second is only divisible by 4, show the player move, then the message for a second
            # else: call the rock paper scissors countdown
            if math.ceil(time.time() - start) % 5 == 0 or (time.time() - start) < 0.5:   # so every 5 seconds call this?
                start_game_countdown(display, display_width, display_height)
                frame_count = 0

            computer_choice = random.choice(options)
            display.blit(hand_sign_images[computer_choice], computer_hand_pos)
            user_choice = "neutral" # get_user_input()

            computer_win_message = "Computer won this round!"
            user_win_message = "You won this round"

            # computer_win_message = "Computer chose " + computer_choice + ". Computer won this round!"
            # user_win_message = "Computer chose " + computer_choice + ". You won this round!"

            # read in and process each frame from webcam to track hand gestures
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # mirror the frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False

            results = hands.process(rgb_frame)

            rgb_frame.flags.writeable = True
            # rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    num_landmarks = len(hand_landmarks.landmark)  # 21 landmarks per hand

                    hand_label = results.multi_handedness[idx].classification[0].label

                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Estimate hand gestures based on model
                    try:
                        hand_res = results.multi_hand_landmarks[0].landmark  # train one hand at a time
                        hand_row = list(
                            np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_res]).flatten())

                        X = pd.DataFrame([hand_row])
                        hand_gesture_class = model.predict(X)[0]
                        user_choice = hand_gesture_class # pick first detected and keep the same

                        # print hand (left/right) and gesture to the screen
                        cv2.putText(frame, f'{hand_label}: ' + hand_gesture_class,
                                    (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]),
                                     int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    except:
                        pass

            if user_choice == "neutral":
                display_game_message("Too Slow!")
                pass
            elif computer_choice == user_choice:
                display_game_message("Tie")
                print("Tie")
            elif computer_choice == "rock":
                if user_choice == "paper":
                    user_score += 1
                    display_game_message(user_win_message)
                    print(user_win_message)
                else:
                    computer_score += 1
                    display_game_message(computer_win_message)
                    print(computer_win_message)
            elif computer_choice == "paper":
                if user_choice == "scissors":
                    user_score += 1
                    display_game_message(user_win_message)
                    print(user_win_message)
                else:
                    computer_score += 1
                    display_game_message(computer_win_message)
                    print(computer_win_message)
            else: # computer choice is scissors
                if user_choice == "rock":
                    user_score += 1
                    display_game_message(user_win_message)
                    print(user_win_message)
                else:
                    computer_score += 1
                    display_game_message(computer_win_message)
                    print(computer_win_message)

            display_score(user_score)

            if check_if_game_over("Computer", computer_score):
                game_running = False

            if check_if_game_over("You", user_score):
                game_running = False

            pygame.event.pump()

            # add video feed to pygame window
            frame_300 = resize_video_output(rgb_frame, 0.5)
            rgb_frame = frame_300
            rgb_frame = np.flip(rgb_frame, 0)  # mirror the video stream
            rgb_frame = np.rot90(rgb_frame, 3)  # rotate the video stream so its upwards
            rgb_frame = pygame.surfarray.make_surface(rgb_frame)  # apply footage as pygame surface
            display.blit(rgb_frame, (600, 200))  # add video stream to game window


            pygame.display.update()
            clock.tick(60)
            # cv2.imshow("Hand Tracking", frame)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
