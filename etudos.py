from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.image import CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import filechooser
import mysql.connector as sql
import io

Window.size = (500,700)
Window.clearcolor = (237/255, 234/255, 225/255, 1)


#Définition de toutes les fenêtres
class Login(Screen):
    def on_leave(self):
        self.ids.connect_login.text = ''
        self.ids.connect_mdp.text = ''

    def connect(self):
        db = sql.connect(host="127.0.0.1", database='bdetu', user="etuadmin", password="etuadmin")
        cursor = db.cursor()
        cursor.execute("SELECT identifiant, password FROM users LIMIT 1")
        data = cursor.fetchone()
        if self.ids.connect_login.text == data[0] and self.ids.connect_mdp.text == data[1]:
            App.get_running_app().root.current = "NavigProf"
        else:
            self.ids.login_error.text = "Identifiants invalides !"
    
    def reset_err_msg(self):
        self.ids.login_error.text = ""

class NavigProf(Screen):
    pass

class Add(Screen):
    def __init__(self, **kw):
        super(Add, self).__init__(**kw)
        Window.bind(on_drop_file=self.drop_file)
        self.photo_path = ''

    def drop_file(self, window, file_path, x, y):
        self.ids.picture_add_etu.text = str(file_path).split("\\")[-1].strip("'").replace(" ", "_")
        self.photo_path = str(file_path).replace("\\", "/")
    
    def file_chooser(self):
        filechooser.open_file(on_selection=self.picture_selected)

    def picture_selected(self, selection):
        if len(selection) >= 1:
            self.ids.picture_add_etu.text = selection[0].split("\\")[-1].strip("'").replace(" ", "_")
            self.photo_path = selection[0].replace("\\", "/")
    
    def convert_pic(self, file_path):
        with open(file_path, 'rb') as file:
            photo = file.read()
        return photo

    def reset(self, type):
        if type == "ALL":
            self.ids.surname_etu.text = ''
            self.ids.name_etu.text = ''
            self.ids.age_etu.text = ''
            self.ids.subject_choice_etu.text = 'Matière ?'
            self.ids.moyenne_etu.text = ''
            self.ids.year_choice_etu.text = 'Année ?'
            self.ids.picture_add_etu.text = 'Cliquez ou glissez la photo ici'
            self.ids.add_etu_error.text = ''
        elif type == "ERR":
            self.ids.surname_etu.text = ''
            self.ids.name_etu.text = ''
            self.ids.age_etu.text = ''
            self.ids.subject_choice_etu.text = 'Matière ?'
            self.ids.moyenne_etu.text = ''
            self.ids.year_choice_etu.text = 'Année ?'
            self.ids.picture_add_etu.text = 'Cliquez ou glissez la photo ici'

    def on_leave(self):
        self.reset("ALL")

    def add_student(self):
        etu_exist = False
        if self.ids.surname_etu.text == '' or self.ids.name_etu.text == '' or self.ids.age_etu.text == '' or self.ids.subject_choice_etu.text == 'Matière ?' or self.ids.moyenne_etu.text == '' or self.ids.year_choice_etu.text == "Année ?" or self.ids.picture_add_etu.text == 'Cliquez ou glissez la photo ici':
            self.ids.add_etu_error.text = 'Il y a une ou des erreurs de saisie'
        else:
            db = sql.connect(host="127.0.0.1", database='bdetu', user="etuadmin", password="etuadmin")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM etudiants")
            data = cursor.fetchall()
            values = []
            for etu in data:
                values_dict = {"surname": etu[0], "name": etu[1], "age": etu[2], "year": etu[3], "subject": etu[4], "moy": etu[5], "photo": etu[6]}
                values.append(values_dict)
            
            for etu in values:
                if ((self.ids.surname_etu.text.lower() == etu['surname'].lower() and self.ids.name_etu.text.lower() == etu['name'].lower()) and ((self.ids.subject_choice_etu.text == etu['subject']) or (self.ids.age_etu.text != etu['age']) or (self.ids.year_choice_etu.text != etu['year']) or (hash(CoreImage(io.BytesIO(self.convert_pic(self.photo_path)), ext="png").texture) != hash(CoreImage(io.BytesIO(etu['photo']), ext="png").texture)))):
                    self.ids.add_etu_error.text = "Cet étudiant existe déjà ! Essayez de rentrer une autre matière."
                    etu_exist = True
                    self.reset("ERR")
                    break
                
            if etu_exist == False:
                to_insert = [self.ids.surname_etu.text, self.ids.name_etu.text, int(self.ids.age_etu.text), self.ids.year_choice_etu.text, self.ids.subject_choice_etu.text, float(self.ids.moyenne_etu.text), self.convert_pic(self.photo_path)]
                cursor.execute("INSERT INTO etudiants (surname, name, age, year, subject, moy, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)", to_insert)
                self.reset("ALL")

        db.commit()
        db.close()


class Liste(Screen):
    def on_enter(self):
        db = sql.connect(host="127.0.0.1", database='bdetu', user="etuadmin", password="etuadmin")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM etudiants")
        data = cursor.fetchall()
        studs = []
        for etu in data:
            stud_dict = {"surname": etu[0], "name": etu[1], "age": etu[2], "year": etu[3], "subject": etu[4], "moy": etu[5], "photo": etu[6]}
            studs.append(stud_dict)
        studs_lists = [i for i in self.ids.stud_lists.children]
        for stud_list in studs_lists:
            self.ids.stud_lists.remove_widget(stud_list)
        for etu in studs:
            stud = StudList()
            stud.ids.stud_list_surname.text = etu['surname']
            stud.ids.stud_list_name.text = etu['name']
            stud.ids.stud_list_age.text = str(etu['age'])
            stud.ids.stud_list_year.text = str(etu['year'])
            stud.ids.stud_list_subject.text = etu['subject']
            stud.ids.stud_list_moy.text = str(etu['moy'])
            stud.ids.stud_list_picture.texture = CoreImage(io.BytesIO(etu['photo']), ext="png").texture
            self.ids.stud_lists.add_widget(stud)

    def search(self):
        print("searching : " + self.ids.list_search.text)

class Trombi(Screen):
    def on_enter(self):
        self.studs = ["Quentin DELCHIAPPO", "Bernard"]
        studs_trombis = [i for i in self.ids.trombi_studs.children]
        for trombi_stud in studs_trombis:
            self.ids.trombi_studs.remove_widget(trombi_stud)
        for studi in self.studs:
            trombi = TrombiStud()
            trombi.ids.trombi_stud_name.text = studi
            self.ids.trombi_studs.add_widget(trombi)
    
    def search(self):
        print("searching : " + self.ids.trombi_search.text)

class StudentView(Screen):
    def on_enter(self):
        self.moys = ["Physique", "Web", "Java", "Me"]
        stud_moys = [i for i in self.ids.stud_view_moys.children]
        for stud_moy in stud_moys:
            self.ids.stud_view_moys.remove_widget(stud_moy)
        for moyi in self.moys:
            moy = EtuMoy()
            moy.ids.stud_view_moy_subject.text = moyi
            self.ids.stud_view_moys.add_widget(moy)
    
    def populate(self, stud_surname, stud_name):
        self.ids.stud_view_picture.texture

class StudList(BoxLayout):
    def test(self):
        print(self.ids.stud_list_surname.text + " " + self.ids.stud_list_name.text)

class ButtonGrid(ButtonBehavior, BoxLayout):
    pass

class TrombiStud(BoxLayout):
    pass

class EtuMoy(BoxLayout):    
    def moy_suppr(self):
        self.parent.remove_widget(self)

class WindowManager(ScreenManager):
    pass

class etudos(App):
    def build(self):
        pass

if __name__ == "__main__":
    etudos().run()