import time
import random

import pygame


def main():
    pygame.init()

    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    background_colour = (51, 102, 153)

    display = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("AI Rock Paper Scissors Game")

    clock = pygame.time.Clock()

    def display_score():
        pass

    def countdown():
        pass

    def start_game():
        hand_options = ["rock", "paper", "scissors"]
        computer_score = 0
        player_score = 0

        computer_win = False
        player_win = False
        tie = False
        run_game = False

        movement_dict_0 = {
            "rock": {"beats": "scissors", "defeated by": "paper"},  # makes more sense to use scores?
            "paper": {"beats": "rock", "defeated by": "scissors"},
            "scissors": {"beats": "paper", "defeated by": "rock"}
        }
        movement_dict = {  # scores for the computer
            "rock": {"rock": 0, "paper": -1, "scissors": 1},  # if player chooses paper, lose score
            "paper": {"rock": 1, "paper": 0, "scissors": -1},
            "scissors": {"rock": -1, "paper": 1, "scissors": 0}
        }

        # if the computer goes first it randomly chooses one of the movements
        initial_computer_choice = random.choice(hand_options)
        computer_choice = initial_computer_choice
        player_choice = "scissors"

        # there should be some 3-second countdown
        overall_scores = movement_dict[computer_choice][player_choice]
        if overall_scores == 1:
            computer_score += 1
        elif overall_scores == -1:
            player_score += 1

        if computer_score > player_score:
            computer_win = True
        elif player_score > computer_score:
            player_win = True
        else:
            tie = True


if __name__ == "__main__":
    main()
