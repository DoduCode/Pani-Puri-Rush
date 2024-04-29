import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def randomise_hand(self, img):
    pass

def load_images(path):
    images = []
    for img in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(f"{path}/{img}"))
    return images