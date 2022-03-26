import pygame
from pygame.sprite import Sprite
#TODO 
#IMOPORTANT  
# Plan:
# przdmioty i npc będą tak jak spawn jest zrobiony
# na podstawie koord oraz nazwy 
# funkcja będzie przypisywać img oraz ustawienie danego cośa 
# ma sprawdzać też też kolizję z characterem dla wywoołania dialogów


class NPC(Sprite):
    """Klasa do zarządzania postaciami niekierowanymi przez gracza
    (Non-Person Character)"""

    def __init__(self, dogex, id):
        """Inicjalizacja NPC"""
        super().__init__()
        self.screen = dogex.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = dogex.settings
        self.character = dogex.character
        self.map = dogex.map

        # Identyfikator NPC - używany np. do wczytywania dialogów
        self.id = id

        # Etap 'relacji' z NPC - przed questem, w trakcie, po queście itd.
        self.stage = 0

        image = f'images/{id}.bmp'
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
  
        #Postać testowa zaczyna po lewej stronie mapy
        self.rect.midleft = self.screen_rect.midleft
        self.rect.x += 50
    

        #Położenie NPc przechowywane jest w zmiennej zmiennoprzecinkwej
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #Kierunek poruszania się NPC
        self.xDirection = 1
        self.yDirection = -1

    def check_vertical_edges(self):
        """Zwraca True, jeśli NPC znajduje w określonej odległości od górnej
        lub dolnej krawędzi ekranu"""
        if (self.rect.centery < 100 or
            self.rect.centery > self.settings.screen_height - 100):
            return True

    def update(self):
        """Przesuwanie postaci dookoła mapy"""
        if not self.rect.colliderect(self.character):
            self.y += self.settings.npc_speed * self.yDirection
            self.rect.y = self.y

    def blit_npc(self):
        """Wyświetlene NPC na ekranie"""
        self.screen.blit(self.image, self.rect)
