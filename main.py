import pygame
import sys
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid, AsteroidField
from text import Text, Countdown, Instruction
from menu import menu
from game import game

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    
    while True:
        menu_message = menu() 
        if menu_message == "game":
            game()
        if menu_message == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()