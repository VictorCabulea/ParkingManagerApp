import pygame

from otherFunctions import load_sound


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {}
        self.categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def load_sounds(self):
        for category in self.categories:
            for i in range(1, 11):
                sound_key = f"{category}{i}"
                sound_path = f"resources/sounds/sounds_parking_lots/{sound_key}.mp3"
                self.sounds[sound_key] = load_sound(sound_path)

        self.sounds['parasiti_parcarea'] = load_sound("resources/sounds/parasiti_parcarea.mp3")
        self.sounds['nu_sunt_locuri_disponibile'] = load_sound("resources/sounds/nu_sunt_locuri_disponibile.mp3")
        self.sounds['plata_invalida'] = load_sound("resources/sounds/plata_invalida.mp3")
        self.sounds['plata_inexistenta'] = load_sound("resources/sounds/plata_inexistenta.mp3")
        self.sounds["masina_nu_e_in_parcare"] = load_sound("resources/sounds/masina_nu_e_in_parcare.mp3")

    def play_sound(self, sound_key):
        self.sounds[sound_key].play()
