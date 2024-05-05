import random

import pygame

from scripts.utils import circle_collision

class WorkStation:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def render(self, surf):
        surf.blit(pygame.transform.scale(self.game.assets['workstation'], self.size), self.pos)

class HandSpanwer:
    def __init__(self, game, count = 1):
        self.game = game
        self.count = count

        self.hand_list = []

    def spawn_hand(self):
        if len(self.game.hands) >= 1:
            self.new_hand_pos = self.game.hands[-1]
            if not self.new_hand_pos.flip and not self.new_hand_pos.rotate[0]:
                if (self.new_hand_pos.pos[1] - 20 - 56) >= (162 + 20):  # 162 is how far the hand moves while bobbing, 20 is the padding
                    self.new_hand = Hand(self.game, (0, self.new_hand_pos.pos[1] - 20 - 56), (164, 56))

                else:
                    self.new_hand = Hand(self.game, (20, 0), (164, 56), rotate = [1, 1])

            elif self.new_hand_pos.rotate[0] and self.new_hand_pos.rotate[1]:
                if (self.new_hand_pos.pos[0] + 20 + 56) <= (self.game.win_size[0] - 20):
                    self.new_hand = Hand(self.game, (self.new_hand_pos.pos[0] + 20 + 56, 0 - 20), (164, 56), rotate = [1, 1])

                else:
                    self.new_hand = Hand(self.game, (self.game.win_size[0] - 164, 162 + 20), (164, 56), flip = True)

            elif self.new_hand_pos.flip:
                if (self.new_hand_pos.pos[1] + 20 + 56) <= (self.game.win_size[1] - 20 - 56 - 164):
                    self.new_hand = Hand(self.game, (self.game.win_size[0] - 164, self.new_hand_pos.pos[1] + 20 + 56), (164, 56), flip = True)

                else:
                    self.new_hand = Hand(self.game, (self.game.win_size[0] - 20 - 56, self.game.win_size[1] - 164), (164, 56), rotate = [1, 0])

            elif self.new_hand_pos.rotate[0] and not self.new_hand_pos.rotate[1]:
                if (self.new_hand_pos.pos[0] - 20 - 56) >= (20):
                    self.new_hand = Hand(self.game, (self.new_hand_pos.pos[0] - 20 - 56, self.game.win_size[1] - 164), (164, 56), rotate = [1, 0])

                else:
                    print("Out of positions")

            if self.new_hand != self.new_hand_pos:
                self.game.hands.append(self.new_hand)

        else:
            self.new_hand = Hand(self.game, (0, self.game.win_size[1] - (164 + 20 + 56)), (164, 56))

            self.game.hands.append(self.new_hand)

class Hand:
    def __init__(self, game, pos, size, flip = False, rotate = [0, 1]):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.flip = flip
        self.rotate = rotate

        self.img = self.game.assets['hands'][random.randint(0, 3)]

        self.has_plate = [False, None]
        self.is_active = True
        self.movement = [1, 0]

    def rect(self):
        if not self.rotate[0]:
            return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        if self.rotate[0]:
            return pygame.Rect(self.pos[0], self.pos[1], self.size[1], self.size[0])

    def move_hand(self):
        if not self.rotate[0] and not self.flip:
            if self.movement[0]:
                self.pos[0] += 1
                if self.rect().centerx >= 80:
                    self.movement = [0, 1]

            if self.movement[1]:
                self.pos[0] -= 1
                if self.rect().centerx <= 20:
                    self.movement = [1, 0]

        if self.rotate[0] and self.rotate[1]:
            if self.movement[0]:
                self.pos[1] += 1
                if self.rect().centery >= 80:
                    self.movement = [0, 1]

            if self.movement[1]:
                self.pos[1] -= 1
                if self.rect().centery <= 20:
                    self.movement = [1, 0]

        if self.flip:
            if self.movement[0]:
                self.pos[0] -= 1
                if self.rect().centerx <= (self.game.win_size[0] - 80):
                    self.movement = [0, 1]

            if self.movement[1]:
                self.pos[0] += 1
                if self.rect().centerx >= (self.game.win_size[0] - 20):
                    self.movement = [1, 0]

        if self.rotate[0] and not self.rotate[1]:
            if self.movement[0]:
                self.pos[1] -= 1
                if self.rect().centery <= (self.game.win_size[1] - 80):
                    self.movement = [0, 1]

            if self.movement[1]:
                self.pos[1] += 1
                if self.rect().centery >= (self.game.win_size[1] - 20):
                    self.movement = [1, 0]

    def update(self):
        if not (self.has_plate[1] is None):
            if not self.has_plate[1].is_active:
                if not self.flip and not self.rotate[0]:
                    if self.rect().centerx >= -100:
                        self.pos[0] -= 2

                    else:
                        self.has_plate[1].is_active = True

                if self.rotate[0] and self.rotate[1]:
                    if self.rect().centery >= - 100:
                        self.pos[1] -= 2

                    else:
                        self.has_plate[1].is_active = True

                if self.flip:
                    if self.rect().centerx <= self.game.win_size[0] + 100:
                        self.pos[0] += 2

                    else:
                        self.has_plate[1].is_active = True

                if self.rotate[0] and not self.rotate[1]:
                    if self.rect().centery <= self.game.win_size[1] + 100:
                        self.pos[1] += 2

                    else:
                        self.has_plate[1].is_active = True

            else:
                self.move_hand()

        else:
            self.move_hand()

    def render(self, surf):
        if not self.rotate[0] and not self.flip:
            surf.blit(pygame.transform.scale(self.img, self.size), self.pos)

        if self.rotate[0] and self.rotate[1]:
            surf.blit(pygame.transform.rotate(pygame.transform.scale(self.img, self.size), -90), self.pos)

        if self.flip:
            surf.blit(pygame.transform.flip(pygame.transform.scale(self.img, self.size), self.flip, False), self.pos)

        if self.rotate[0] and not self.rotate[1]:
            surf.blit(pygame.transform.rotate(pygame.transform.scale(self.img, self.size), 90), self.pos)

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
        self.game.papu.append(PaniPuri(self.game, 0, (self.pos[0] + 100, self.pos[1] - 10), (50, 50)))
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
        surf.blit(pygame.transform.rotate(pygame.transform.scale(self.game.assets['bags'][self.bag_state], self.size), 90), self.pos)

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
        if self.rect().colliderect(self.game.trash):
            if circle_collision(1, self.game.trash.midright[0] - self.game.trash.x, self.rect().center, self.game.trash.center) and not self.is_mouse_active:
                self.game.papu.remove(self)

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