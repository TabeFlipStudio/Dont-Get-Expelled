import pygame


class IntroScreen():


    def __init__(self, dogex):
        self.settings = dogex.settings
        self.screen = dogex.screen
        self.screen_rect = dogex.screen_rect

        self.image = pygame.image.load("images/intro_good.png")#amogus.bmp")
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.screen_rect.topleft

        self.clock = dogex.clock

        self.done = False

    def fadeout(self, speed=0.5):
        """Eleganckia animacja zanikania"""
        fadeout = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        fadeout = fadeout.convert()
        i = 0
        done = True
        while done:
            fadeout.set_alpha(i)
            self.screen.blit(fadeout, (0, 0))
            pygame.display.update()
            i += speed
            if i >= 200:
                done = False

    def fadein(self, image,speed=0.1, duration=255):
        """Elegancka animacja stopniowego pojawiania się"""
        if image == None:
            fadein = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        else:
            fadein = image

        fadein = fadein.convert()
        i = 0
        done = True
        while done:
            fadein.set_alpha(i)
            self.screen.blit(fadein, (0, 0))
            pygame.display.update()
            i += speed
            if i >= duration:
                done = False


    def intro_fadein(self, speed=1):
        fadein = self.image
        fadein = fadein.convert()
        i = 0
        done = True
        while done:
            fadein.set_alpha(i)
            self.screen.blit(fadein, (0, 0))
            pygame.display.update()
            i+=speed
            if i >= 255:
                done = False


    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def black_screen(self):
        self.screen.fill((0,0,0))
