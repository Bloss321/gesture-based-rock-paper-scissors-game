# simple algorithm for choosing rock, paper or scissors action as the opponent

options = ["rock", "paper", "scissors"]

movement_dict = {
    "rock": {"beats": "scissors", "defeated by": "paper"},
    "paper": {"beats": "rock", "defeated by": "scissors"},
    "scissors": {"beats": "paper", "defeated by": "rock"}
}

def opponent_choice(user_choice):
    pass
