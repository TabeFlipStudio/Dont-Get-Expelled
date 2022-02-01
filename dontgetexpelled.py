import sys
import pygame

from settings import Settings
from character import MainCharacter
from inventory import Inventory, Slot
from item import Item
from TiledMap import Map
from npc import NPC

class DoGeX():
    """Ogólna klasa zarządzająca grą i jej zasobami"""

    def __init__(self):
        """Inicjalizacja gry i zasobów"""
        pygame.init()
        self.settings = Settings()

        self.clock = pygame.time.Clock()

        #Wczytanie ekranu i nadanie tytułu
        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Don't Get Expelled! The Batory Game")

        #Wczytanie zasobów z pliku
        self.character = MainCharacter(self)
        self.character.facing = "stationary"
        self.inventory = Inventory(self)
        self.map = Map(self)
        self.map_image = self.map.map_setup(self.map.tmxdata)

        self.slots = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()

        #Przed wywołaniem _create_slots() nie ma jeszcze slotu do upuszczania
        #Atrybut wyłącznie dla przejrzystości kodu
        self.drop_slot = None

        #Utworzenie slotów
        self._create_slots()

        #Testowe rozmieszczenie przedmiotów i NPC
        self.items.add(Item(self, 'red_ball', 100, 100))
        self.items.add(Item(self, 'blue_ball', 1000, 400))
        self.items.add(Item(self, 'green_ball', 500, 650))

        self.npcs.add(NPC(self))

    def run_game(self):
        """Uruchomienie pętli głównej gry"""

        while True:
            self._check_events()
            self.map.collision()

            if not self.inventory.active:
                self.character.update()
                self.map.update()
                self._update_npcs()


            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Reakcja na zdarzenia wywołane przez klawiaturę i mysz"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            if (event.type == pygame.MOUSEBUTTONDOWN and
            self.inventory.grabbed_item is None and self.inventory.active):
                mouse_pos = pygame.mouse.get_pos()
                self.inventory.grab_item(self, mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP and self.inventory.active:
                mouse_pos = pygame.mouse.get_pos()
                self.inventory.release_item(self, mouse_pos)

    def _check_keydown_events(self, event):
        """Reakcja na naciśnięcie klawisza"""

        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.character.moving_right = True
            self.map.moving_left = True
            self.character.facing = "right"

        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.character.moving_left = True
            self.map.moving_right = True
            self.character.facing = "left"

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.character.moving_up = True
            self.map.moving_down = True
            self.character.facing = "up"

        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.character.moving_down = True
            self.map.moving_up = True
            self.character.facing = "down"

        if event.key == pygame.K_i:
            self.inventory.active = not self.inventory.active

        if event.key == pygame.K_e:
            if not self.inventory.active:
                self._pickup_item()

        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        """Reakcja na puszczenie klawisza"""

        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.character.moving_right = False
            self.map.moving_left = False
            self.character.facing = "stationary"

        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.character.moving_left = False
            self.map.moving_right = False
            self.character.facing = "stationary"

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.character.moving_up = False
            self.map.moving_down = False
            self.character.facing = "stationary"

        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.character.moving_down = False
            self.map.moving_up = False
            self.character.facing = "stationary"

    def _create_slots(self):
        """Utworzenie wszystkich slotów ekwipunku"""
        for row_number in range(2): #Dwa rzędy slotów
            for slot_number in range(8): #Po 8 slotów każdy
                slot = Slot(self.inventory)
                slot_width  = slot.rect.width
                slot_height = slot.rect.height

                slot.x = (slot.rect.x + slot_width +
                    1.5 * slot_width * slot_number)
                slot.rect.x = slot.x
                slot.rect.y += slot_height + 2 * slot_height * row_number
                self.slots.add(slot)
            else:
                slot = Slot(self.inventory)
                slot.rect.centerx = self.screen.get_rect().centerx
                slot.rect.y += slot_height + 2 * slot_height * 2
                self.drop_slot = slot

    def _pickup_item(self):
        """Sprawdzenie, czy postać stoi koło przedmiotu
        i ewentualne podniesienie"""

        for item in self.items.copy():
            if pygame.Rect.colliderect(self.character.rect, item):
                for slot in self.slots.sprites():
                    #Umieść przedmiot tylko raz
                    if slot.content is None:
                        slot.content = item
                        break

                self.items.remove(item)

    def _check_npc_vertical_edges(self):
        """Zmiana kierunku poruszania się NPC, jeśli dotarł blisko
        krawędzi ekranu"""
        for npc in self.npcs.sprites():
            if npc.check_vertical_edges():
                npc.yDirection *= -1

    def _update_npcs(self):
        """Uaktualnienie pozycji wszystkich NPC"""
        self._check_npc_vertical_edges()
        self.npcs.update()

    def _update_screen(self):
        """Aktualizacja zawartości ekranu"""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.map_image, (self.map.x, self.map.y))
        #pygame.draw.rect(self.screen, self.map.debug_color, self.map.debug_rect) #TOBEDELETED
        self.character.blitme()

        #Wyświetlamy przedmioty i postacie tylko, gdy ekwipunek jest nieaktywny
        if not self.inventory.active:
            self.character.blitme()

            for npc in self.npcs.sprites():
                npc.blit_npc()

            for item in self.items.sprites():
                item.blit_item()

        #Wyświetlamy ekwipunek tylko, jeśli jest on aktywny (naciśnięto I)
        if self.inventory.active:
            self.inventory.display_inventory()
            for slot in self.slots.sprites():
                slot.draw_slot()
                slot.blit_content()

            #Wyświetlenie slotu do upuszczania przemiotów
            self.drop_slot.draw_slot()

            #Wyświetlenie przedmiotu pochwyconego myszą
            self.inventory.display_grabbed_item()

        #Wyświetlenie zmodyfikowanego ekranu
        pygame.display.flip()



if __name__ == '__main__':
    dogex = DoGeX()
    dogex.run_game()
