import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import StringProperty
from plyer import filechooser
from kivy.uix.screenmanager import ScreenManager, Screen

from random import *

Window.size = (500,700)
Window.clearcolor = (237/255, 234/255, 225/255, 1)


#Définition de toutes les fenêtres
class Login(Screen):
    pass

class NavigProf(Screen):
    pass

class Add(Screen):
    def __init__(self, **kw):
        super(Add, self).__init__(**kw)
        Window.bind(on_drop_file=self.drop_file)

    def drop_file(self, window, file_path, x, y):
        self.ids.picture_add.text = str(file_path).split("\\")[-1].strip("'").replace(" ", "_")
    
    def file_chooser(self):
        filechooser.open_file(on_selection=self.picture_selected)

    def picture_selected(self, selection):
        if len(selection) >= 1:
            self.ids.picture_add.text = selection[0].split("\\")[-1].strip("'").replace(" ", "_")

class Liste(Screen):
    def on_enter(self):
        self.studs = ["Quentin", "Bernard", "Pierre", "Moustique"]
        for studi in self.studs:
            stud = StudList()
            stud.ids.stud_list_surname.text = studi
            self.ids.stud_lists.add_widget(stud)

    def search(self):
        print("searching : " + self.ids.list_search.text)

class Trombi(Screen):
    pass

class StudentView(Screen):
    def moy_modify(self):
        show = PopUpMoy()
        popupWindow = Popup(title ="Popup Window", content = show, size_hint =(None, None), size =(300, 400))
        popupWindow.open()

class StudList(BoxLayout):
    pass

class PopUpMoy(BoxLayout):
    pass

class WindowManager(ScreenManager):
    pass

class etudos(App):
    def build(self):
        pass

if __name__ == "__main__":
    etudos().run()