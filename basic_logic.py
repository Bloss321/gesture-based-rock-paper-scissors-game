import random

options = ["rock", "paper", "scissors"]


def get_user_input():
    user_input = input("Enter choice: ")
    if user_input not in options:
        print("Invalid game input! Try again.")
        get_user_input()
    return user_input

def check_if_game_over(player, score):
    if score < 5:
        return False
    else:
        print("\n", player, " has won the game!")
        print("User Score: " + str(score))
        print("Computer Score: " + str(score))
        return True

def run_game():
    computer_score = 0
    user_score = 0
    game_running = True

    while game_running:
        computer_choice = random.choice(options)
        user_choice = get_user_input()

        computer_win_message = "Computer chose " + computer_choice + ". Computer won this round!"
        user_win_message = "Computer chose " + computer_choice + ". You won this round!"

        if computer_choice == user_choice:
            print("Tie")
        elif computer_choice == "rock":
            if user_choice == "paper":
                user_score += 1
                print(user_win_message)
            else:
                computer_score += 1
                print(computer_win_message)
        elif computer_choice == "paper":
            if user_choice == "scissors":
                user_score += 1
                print(user_win_message)
            else:
                computer_score += 1
                print(computer_win_message)
        else: # computer choice is scissors
            if user_choice == "rock":
                user_score += 1
                print(user_win_message)
            else:
                computer_score += 1
                print(computer_win_message)

        if check_if_game_over("Computer", computer_score):
            game_running = False

        if check_if_game_over("You", user_score):
            game_running = False


if __name__ == "__main__":
    run_game()
