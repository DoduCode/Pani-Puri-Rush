import sys

import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PaniPuri, PaniPuriBag, InfPaniPuriBag, Plate, Hand, HandSpanwer
   
"""
To-Do List:
(now)
• Make the hand spawner  ••• ( Done )
• Make more hand colors  • ( Done )
• Randomize the color of the hand  •• ( Done )
• Create a specific station for the papu is next state  •••••
• Make the layout ( Art )  ••••
• Randomise the spawn of the papu ( possibility of broke papu ) ( Done )
• Make a trash to dispose waste ( once this is made it fixes bug #2)

(later)
• Add a rating system
• Create days (level changing)  ••
• Add a currency  •
• Make a shop  •••
• Add music
• Add sfx

Bugs:
• #1 Plate and papus stick together and are hard to be moved ( happens when the papu or the plate is moved over the other one )
• #2 The destroyed papu can be placed on the plate ( fix with the trash to dispose ) ( easy to fix and should be changed after trash is made)

"""

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Pani Puri Rush")
        self.display = pygame.display.set_mode((780, 596))

        self.win_size = [780, 596]

        self.assets = {
            'workstatoin': load_image("workstation.png"),
            'plate': load_image("plate/plate.png"),
            'papus': load_images("panipuri"),
            'bags': load_images("panipuribag"),
            'hands': load_images("hands")
        }

        self.hand_spawner = HandSpanwer(self)

        self.hands = []

        self.plates = [Plate(self, (100, 100), (50, 50))]
        self.active_plate = None

        self.papu_bags = [PaniPuriBag(self, (100, 100), (97, 69), 15), InfPaniPuriBag(self, (0, 0), (0, 0))]

        self.papu = []
        self.max_papu = 32

        self.mouse_active_papu = None
        self.active_papu = None

        self.clicking = False
        self.mpos = [0, 0]
        self.mouse_busy = False

        self.clock = pygame.time.Clock() 

    def run(self):
        while True:
            self.display.fill((5, 129, 173))

            self.mpos = pygame.mouse.get_pos()

            for hand in self.hands:
                hand.update()
                hand.render(self.display)

            #renders all the plates
            for plate in self.plates:
                plate.update()
                if not plate.on_hand[0]:
                    for hand in self.hands:
                        if not hand.flip and not hand.rotate[0]:
                            if plate.rect().collidepoint((hand.rect().centerx + 30, hand.rect().centery - 20)):
                                plate.render(self.display, (hand.rect().centerx + 30, hand.rect().centery - 20))
                                plate.on_hand = [True, hand]
                                hand.has_plate = [True, plate]

                            else:
                                plate.render(self.display, plate.pos)

                        elif hand.rotate[0] and hand.rotate[1]:
                            if plate.rect().collidepoint((hand.rect().centerx - 30, hand.rect().centery + 30)):
                                plate.render(self.display, (hand.rect().centerx - 30, hand.rect().centery + 30))
                                plate.on_hand = [True, hand]
                                hand.has_plate = [True, plate]

                            else:
                                plate.render(self.display, plate.pos)

                        elif hand.flip:
                            if plate.rect().collidepoint((hand.rect().centerx - 30, hand.rect().centery - 20)):
                                plate.render(self.display, (hand.rect().centerx - 30, hand.rect().centery - 20))
                                plate.on_hand = [True, hand]
                                hand.has_plate = [True, plate]

                            else:
                                plate.render(self.display, plate.pos)

                        elif hand.rotate[0] and not hand.rotate[1]:
                            if plate.rect().collidepoint((hand.rect().centerx - 20, hand.rect().centery - 75)):
                                plate.render(self.display, (hand.rect().centerx - 20, hand.rect().centery - 75))
                                plate.on_hand = [True, hand]
                                hand.has_plate = [True, plate]

                            else:
                                plate.render(self.display, plate.pos)

                else:
                    if not plate.on_hand[1].flip and not plate.on_hand[1].rotate[0]:
                        plate.render(self.display, (plate.on_hand[1].rect().centerx + 30, plate.on_hand[1].rect().centery - 20))

                    elif plate.on_hand[1].rotate[0] and plate.on_hand[1].rotate[1]:
                        plate.render(self.display, (plate.on_hand[1].rect().centerx - 30, plate.on_hand[1].rect().centery + 30))
                    
                    elif plate.on_hand[1].flip:
                        plate.render(self.display, (plate.on_hand[1].rect().centerx - 80, plate.on_hand[1].rect().centery - 20))

                    elif plate.on_hand[1].rotate[0] and not plate.on_hand[1].rotate[1]:
                        plate.render(self.display, (plate.on_hand[1].rect().centerx - 20, plate.on_hand[1].rect().centery - 75))

            # renders the pani puri bags
            for papu_bag in self.papu_bags:
                papu_bag.update()
                papu_bag.render(self.display)

            # renders all the pani puri sprites
            for papu in self.papu:
                papu.update()
                if not papu.on_plate[0]:
                    for plate in self.plates:
                        if plate.on_hand and self.mouse_active_papu is None:
                            if plate.rect().collidepoint(papu.rect().center) and plate.on_hand and plate.has_papu[1] is None:
                                papu.on_plate = [True, plate]
                                papu.render(self.display, (plate.rect().centerx - 25, plate.rect().centery - 25))
                                plate.is_active = False
                                plate.has_papu[1] = papu

                            else:
                                papu.render(self.display, papu.pos)

                        else:
                            papu.render(self.display, papu.pos)

                else:
                    papu.render(self.display, (papu.on_plate[1].rect().centerx - 25, papu.on_plate[1].rect().centery - 25))
                    if not papu.on_plate[1].is_active:
                        if plate.rect().x <= -40:
                            if (len(self.papu) - 1) >= 0:
                                self.papu.remove(papu)
                                plate.is_active = False
                                plate.has_papu[1] = None
                                #it works
                                if (len(self.papu) - 1) >= 0:   
                                    self.active_papu = self.papu[len(self.papu) - 1]

            # renders the active pani puris above all others
            if not self.mouse_active_papu is None:
                self.mouse_active_papu.update()
                self.mouse_active_papu.render(self.display, self.mouse_active_papu.pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                        self.mouse_busy = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if len(self.papu) < self.max_papu:
                            self.papu_bags[0].use_papu()

                    if event.key == pygame.K_a:
                        if not (self.active_papu is None):
                            self.active_papu.next_state()

                    if event.key == pygame.K_d:
                        self.papu_bags.insert(-2, PaniPuriBag(self, (100, 100), (97, 69), 15))

                    if event.key == pygame.K_f:
                        if (len(self.papu) - 1) >= 0:
                            self.papu.remove(self.active_papu)
                            self.active_papu = self.papu[len(self.papu) - 1]
                            #it works
                            if (len(self.papu) - 1) >= 0:   
                                self.active_papu = self.papu[len(self.papu) - 1]

                    if event.key == pygame.K_g:
                        self.hand_spawner.spawn_hand()

            pygame.display.update()
            self.clock.tick(60)

Game().run()