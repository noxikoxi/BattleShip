import pygame
from string import ascii_uppercase

WIDTH, HEIGHT = 1100, 700
MAP_SIZE = 10
BLOCK_SIZE = int((WIDTH - 200) / 2 / MAP_SIZE)
FPS = 60

OFFSET_X = 50
OFFSET_Y = 50

OPPONENT_MAP_OFFSET_X = WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5

SELECTED_BLOCK_COLOR = (255, 70, 0)
BLOCK_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)
SHOT_CIRCLE_COLOR = (255, 165, 0)

START_SHIPS = {1: 4, 2: 3, 3: 2, 4: 1}

LETTER_TO_DECIMAL = {}

ALPHABET = ascii_uppercase[:MAP_SIZE]

for num, text in enumerate(ALPHABET):
    LETTER_TO_DECIMAL[text] = num

DECIMAL_TO_LETTER = {value: key for key, value in LETTER_TO_DECIMAL.items()}
