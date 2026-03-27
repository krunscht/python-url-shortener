from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '550')

import os, sys
import threading
import pyshorteners
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.resources import resource_add_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

resource_add_path(resource_path('.'))

class MainLayout(BoxLayout):
    pass

class ShortenerApp(App):
    def build(self):
        self.title = "URL Shortener"
        self.spinner_anim = None
        return MainLayout()
    
    def animate_button(self, widget):
        anim = Animation(background_color=(0.1, 0.4, 0.7, 1), d=0.05) + \
               Animation(background_color=(0.2, 0.6, 1, 1), d=0.05)
        anim.start(widget)

    def shorten_link(self):
        self.start_spinner()
        threading.Thread(target=self._shorten_logic, daemon=True).start()

    def start_spinner(self):
        lbl = self.root.ids.result_label
        lbl.text = "<|>" 
        lbl.font_size = '50sp'
        lbl.color = (0.2, 0.6, 1, 1)
        
        if self.spinner_anim:
            self.spinner_anim.cancel(lbl)
        
        self.spinner_anim = Animation(rotation=-360, d=0.5)
        self.spinner_anim.repeat = True
        self.spinner_anim.start(lbl)

    def stop_spinner(self, text, color):
        lbl = self.root.ids.result_label
        if self.spinner_anim:
            self.spinner_anim.cancel(lbl)
        
        lbl.rotation = 0
        lbl.font_size = '16sp'
        lbl.text = text
        lbl.color = color

    def _shorten_logic(self):
        root = self.root
        long_url = root.ids.url_input.text.strip()
        
        RED = (1, 0.3, 0.3, 1)
        GREEN = (0.3, 0.9, 0.4, 1)
        ORANGE = (1, 0.7, 0.4, 1)

        if not long_url:
            self._update_ui("\nВнимание:\nПоле пустое", ORANGE)
            return

        try:
            shortener = pyshorteners.Shortener()
            short_link = shortener.tinyurl.short(long_url)

            Clipboard.copy(short_link)
            self._update_ui(f"Готово!\n[b]{short_link}[/b]\n(Скопировано)", GREEN)

        except Exception as e:
            print(f"Error: {e}")
            self._update_ui("Ошибка сети или\nневерная ссылка", RED)

    def _update_ui(self, text, color):
        Clock.schedule_once(lambda dt: self.stop_spinner(text, color))

if __name__ == '__main__':
    ShortenerApp().run()
