import pygame
import sys, os
from os import listdir
from os.path import isfile, join
import json

IMAGES_PATH = "img/"
DATA_PATH = "data/data.json"

pygame.init()
pygame.display.set_caption("Framing Tool Test")

screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen_ratio = 0.8

size = width, height = int(screen_width * screen_ratio), int(screen_height * screen_ratio)
window = pygame.display.set_mode(size)
screen = pygame.display.get_surface()
bg_color = (255,255,255)

images = [f for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f))]
curr_img = 0

data = None
with open(DATA_PATH, "r") as f:
    data = json.load(f)

def load():
    image = pygame.image.load(IMAGES_PATH + images[curr_img]).convert()
    screen.blit(image, (0, 0))
    for frame in data[images[curr_img]]:
        r = pygame.Rect(int(frame[0] * image.get_width()), int(frame[1] * image.get_height()), int(frame[2] * image.get_width()), int(frame[3] * image.get_height()))
        pygame.draw.rect(screen, (255, 0, 0), r, 2)
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            curr_img += 1

    load()

