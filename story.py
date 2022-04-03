import pygame

class StoryEvents():
    """Zarządzanie biegiem fabuły i zdarzeniami z nim związanymi."""

    def __init__(self, dogex):
        self.settings = dogex.settings
        self.map = dogex.map
        self.window = dogex.window
        self.character = dogex.character
        self.dogex = dogex

        # List of quest codenames and index to decide, which quest is active
        self.quests = ['math', 'zyzio', None]
        self.inx = 0

    def _check_story_events(self):
        """Zdarzenia związane z biegiem fabuły"""
        if self.quests[self.inx] == 'math':
            math_trigger_area = self.map._access_Object('objects.mathtrigger')
            mta_rect = pygame.Rect(math_trigger_area.x, math_trigger_area.y,
                math_trigger_area.width, math_trigger_area.height)

            if self.character.rect.colliderect(mta_rect):
                self.window.active = True
                self.window.node = self.window.dialogues['matma']
                self.window.load_dialogue()
                self.inx += 1

        elif self.quests[self.inx] == 'zyzio':
            encounter = self.map._access_Object('objects.zyzioencounter')
            zyzio_obj = self.map._access_Object('npc.kuba')
            zyzio_obj.x, zyzio_obj.y = encounter.x, encounter.y

            found_npc = self.dogex._find_npc_collision()
            if found_npc and found_npc.id == 'kuba':
                self.window.active = True
                self.window.node = self.window.dialogues[found_npc.id][found_npc.stage]
                self.window.load_dialogue(found_npc)
                self.inx += 1
                
                for npc in self.dogex.npcs.sprites():
                    if npc.id == 'kasia':
                        npc.stage = 0
