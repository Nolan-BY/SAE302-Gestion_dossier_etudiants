import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from random import *

Window.size = (500,700)
Window.clearcolor = (237/255, 234/255, 225/255, 1)


#Définition de toutes les fenêtres 
class Login(Screen):
    pass
class NavigProf(Screen):
    pass
class Liste(Screen):
    pass
class Trombi(Screen):
    pass
class Add(Screen):
    def __init__(self, **kw):
        super(Add, self).__init__(**kw)
        Window.bind(on_drop_file=self.drop_file)

    def drop_file(self, window, file_path, x, y):
        self.ids.photo.text = str(file_path).split("\\")[-1].strip("'").replace(" ", "_")

class Delete(Screen):
    pass
class WindowManager(ScreenManager):
    pass

class etudos(App):
    def build(self):
        pass

if __name__ == "__main__":
    etudos().run()