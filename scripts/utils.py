import os
import math

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

def circle_collision(radius_1, radius_2, pos_1, pos_2):
    s1 = abs(pos_1[0] - pos_2[0])
    s2 = abs(pos_1[1] - pos_2[1])
    hy = math.sqrt((s1 ** 2) + ( s2 ** 2))

    if hy < (radius_1 + radius_2):
        return True
    
    else:
        return False