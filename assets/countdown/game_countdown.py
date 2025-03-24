import pygame
from pygame import Surface

# load text images
scissors = pygame.image.load('assets/countdown/scissors_word.png')
paper = pygame.image.load('assets/countdown/paper_word.png')
rock = pygame.image.load('assets/countdown/rock_word.png')

# scale text images
rock_scale = (rock.get_width() // 1.2, rock.get_height() // 1.2)
paper_scale = (paper.get_width() // 1.1, paper.get_height() // 1.1)
scissors_scale = (scissors.get_width() * 1.1, scissors.get_height() * 1.1)

rock = pygame.transform.scale(rock, rock_scale)
paper = pygame.transform.scale(paper, paper_scale)
scissors = pygame.transform.scale(scissors, scissors_scale)


countdown_images = [
    rock,
    paper,
    scissors
]


# position for centralising the numbers on screen
def get_count_location(image: Surface, display_width, display_height):
    x_pos = display_width // 2 - (image.get_width() // 2)
    y_pos = display_height // 2 - (image.get_height() // 2)
    return x_pos, y_pos


def start_game_countdown(display: Surface, display_width, display_height):
    for i in range(3):
        display.blit(countdown_images[i], get_count_location(countdown_images[i], display_width, display_height))
        pygame.display.update()
        pygame.time.delay(1000)  # delay for 1 second
