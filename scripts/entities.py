import random

import pygame

class HandSpanwer:
    def __init__(self, game, count = 1):
        self.game = game
        self.count = count

class Hand:
    def __init__(self, game, pos, size, flip = [False, False]):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.flip = flip

        self.img = self.game.assets['hands'][random.randint(0, 3)]

        self.has_plate = [False, None]
        self.is_active = True
        self.movement = [1, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def move_hand(self):
        if self.movement[0]:
            self.pos[0] += 1
            if self.rect().centerx >= 80:
                self.movement = [0, 1]

        if self.movement[1]:
            self.pos[0] -= 1
            if self.rect().centerx <= 20:
                self.movement = [1, 0]

    def update(self):
        if not (self.has_plate[1] is None):
            if not self.has_plate[1].is_active:
                if self.rect().centerx >= -100:
                    self.pos[0] -= 2

                else:
                    self.has_plate[1].is_active = True

            else:
                self.move_hand()

        else:
            self.move_hand()

    def render(self, surf):
        surf.blit(pygame.transform.scale(self.img, self.size), self.pos)

class Plate:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size

        self.is_active = True
        self.is_mouse_active = False
        self.game.active_plate = self

        self.on_hand = [False, None]
        self.has_papu = [False, None]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self):
        if self.game.clicking and (not self.game.mouse_busy or self.is_active):
            if self.rect().collidepoint(self.game.mpos):
                self.is_mouse_active = True
                self.game.mouse_busy = True
                # self.game.mouse_active_papu = self
                self.game.active_plate = self
            
        else:
            self.is_mouse_active = False

        if not self.game.mouse_busy:
            self.game.mouse_active_papu = None

        if self.is_mouse_active:
            self.pos[0] = self.game.mpos[0] - (self.size[0] // 2)
            self.pos[1] = self.game.mpos[1] - (self.size[1] // 2)

    def render(self, surf, pos):
        self.pos = list(pos)
        surf.blit(pygame.transform.scale(self.game.assets['plate'], self.size), pos)

class PaniPuriBag:
    def __init__(self, game, pos, size, bag_size = 15, no_papu = 15):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.bag_size = bag_size
        self.no_papu = no_papu
        self.bag_state = 0

    def use_papu(self):
        self.game.papu.append(PaniPuri(self.game, 0, self.game.mpos, (50, 50)))
        self.no_papu -= 1
        if self.no_papu <= 0:
            self.game.papu_bags.pop(0)

    def update(self):
        if self.no_papu in range(self.bag_size - (self.bag_size // 3), self.bag_size + 1):
            self.bag_state = 0

        if self.no_papu in range(self.bag_size - (self.bag_size // 3 * 2), self.bag_size - (self.bag_size // 3)):
            self.bag_state = 1

        if self.no_papu in range(self.bag_size - (self.bag_size // 3) * 3, self.bag_size - (self.bag_size // 3 * 2)):
            self.bag_state = 2

    def render(self, surf):
        surf.blit(pygame.transform.scale(self.game.assets['bags'][self.bag_state], self.size), self.pos)

class InfPaniPuriBag(PaniPuriBag):
    def use_papu(self):
        pass

class PaniPuri:
    def __init__(self, game, papu_state, pos, size):
        self.game = game
        self.papu_state = papu_state
        self.pos = list(pos)
        self.size = size

        self.img = self.game.assets['papus'][0] if random.random() > 0.1 else self.game.assets['papus'][3]

        self.is_active = False
        self.is_mouse_active = False

        self.game.active_papu = self
        self.on_plate = [False, None]

    def next_state(self):
        self.papu_state = min(2, self.papu_state + 1)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self):
        if not self.on_plate[0]:
            if self.game.clicking and (not self.game.mouse_busy or self.is_active):
                if self.rect().collidepoint(self.game.mpos):
                    self.is_active = True
                    self.is_mouse_active = True
                    self.game.mouse_busy = True
                    self.game.mouse_active_papu = self
                    self.game.active_papu = self
                
            else:
                self.is_mouse_active = False

            if not self.game.mouse_busy:
                self.game.mouse_active_papu = None

            if self.is_mouse_active:
                self.pos[0] = self.game.mpos[0] - (self.size[0] // 2)
                self.pos[1] = self.game.mpos[1] - (self.size[1] // 2)

    def render(self, surf, pos):
        if self.img == self.game.assets['papus'][0]:
            surf.blit(pygame.transform.scale(self.game.assets['papus'][self.papu_state], self.size), pos)

        else:
            surf.blit(pygame.transform.scale(self.img, self.size), pos)