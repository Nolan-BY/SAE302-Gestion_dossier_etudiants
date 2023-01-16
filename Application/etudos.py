#!Authors: Nolan BEN YAHYA, Quentin DELCHIAPPO 

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import filechooser
import mysql.connector as sql
import io, random

Window.size = (500,700)
Window.clearcolor = (237/255, 234/255, 225/255, 1)

config = {'host': '192.168.122.242',
          'database': 'bdetu',
          'user': 'etuadmin',
          'password': 'etuadmin'}

class Login(Screen):
    def on_leave(self):
        self.ids.connect_login.text = ''
        self.ids.connect_mdp.text = ''

    def connect(self):
        App.get_running_app().root.current = "NavigProf"
        # db = sql.connect(**config)
        # cursor = db.cursor()
        # cursor.execute("SELECT identifiant, password FROM users")
        # data = cursor.fetchall()
        # users = []
        # log = False
        # for user in data:
        #     users_dict = {'ident': user[0], 'pass': user[1]}
        #     users.append(users_dict)
        
        # for user in users:
        #     if self.ids.connect_login.text == user['ident'] and self.ids.connect_mdp.text == user['pass']:
        #         log = True
        #         App.get_running_app().root.current = "NavigProf"

        # if log == False:
        #     self.ids.login_error.text = "Identifiants invalides !"
    
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
        self.ids.picture_add_etu.text = str(file_path).split("/")[-1].strip("'").replace(" ", "_")
        self.photo_path = str(file_path).replace("\\", "/")
    
    def file_chooser(self):
        filechooser.open_file(on_selection=self.picture_selected)

    def picture_selected(self, selection):
        if len(selection) >= 1:
            self.ids.picture_add_etu.text = selection[0].split("/")[-1].strip("'").replace(" ", "_")
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
        etu_err = False
        if self.ids.surname_etu.text == '' or self.ids.name_etu.text == '' or self.ids.age_etu.text == '' or self.ids.subject_choice_etu.text == 'Matière ?' or self.ids.moyenne_etu.text == '' or self.ids.year_choice_etu.text == "Année ?" or self.ids.picture_add_etu.text == 'Cliquez ou glissez la photo ici':
            self.ids.add_etu_error.text = 'Un ou des champs sont vides'
        else:
            db = sql.connect(**config)
            cursor = db.cursor()
            cursor.execute("SELECT surname, name FROM etudiants")
            data = cursor.fetchall()
            values = []
            for etu in data:
                values_dict = {"surname": etu[0], "name": etu[1]}
                values.append(values_dict)
            
            for etu in values:
                if (self.ids.surname_etu.text.lower() == etu['surname'].lower() and self.ids.name_etu.text.lower() == etu['name'].lower()):
                    self.ids.add_etu_error.text = "Cet étudiant existe déjà !"
                    etu_err = True
                    self.reset("ERR")
                    break
                elif (round(float(self.ids.moyenne_etu.text), 2) > 20 or round(float(self.ids.moyenne_etu.text), 2) < 0):
                    self.ids.add_etu_error.text = "La moyenne n'est pas valide !"
                    etu_err = True
                    self.reset("ERR")
                    break
                elif (int(self.ids.age_etu.text) < 17 or int(self.ids.age_etu.text) > 100):
                    self.ids.add_etu_error.text = "L'âge' n'est pas valide !"
                    etu_err = True
                    self.reset("ERR")
                    break
                
            if etu_err == False:
                ident = self.ids.surname_etu.text[0].upper() + self.ids.name_etu.text[0].upper() + str(random.randint(2000, 9000))
                to_insert_stud = [ident, self.ids.surname_etu.text, self.ids.name_etu.text, int(self.ids.age_etu.text), self.ids.year_choice_etu.text, round(float(self.ids.moyenne_etu.text), 2), self.convert_pic(self.photo_path)]
                to_insert_subject = [ident, self.ids.subject_choice_etu.text, float(self.ids.moyenne_etu.text)]
                cursor.execute("INSERT INTO etudiants (id, surname, name, age, year, global_moy, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)", to_insert_stud)
                cursor.execute("INSERT INTO matières (id, subject, moy) VALUES (%s, %s, %s)", to_insert_subject)
                self.reset("ALL")
            db.commit()
            db.close()

class Liste(Screen):
    def on_pre_enter(self):
        self.populate()
        
    def on_leave(self):
        self.ids.list_key_search.text = ""
        self.ids.list_sort_by.text = "Trier par"
    
    def sort_list(self, search):
        search_list = {"Reset": "",
                        "1A": "AND year = '1A'", "2A": "AND year = '2A'",
                        "Prénoms A-Z": "ORDER BY surname", "Prénoms Z-A": "ORDER BY surname DESC",
                        "Noms A-Z": "ORDER BY name", "Noms Z-A": "ORDER BY name DESC",
                        "Age >": "ORDER BY age", "Age <": "ORDER BY age DESC",
                        "Moyenne G >": "ORDER BY global_moy", "Moyenne G <": "ORDER BY global_moy DESC"}

        if search == "Trier par":
            return ""
        return search_list[search]

    def sort_specific(self, search):
        if len(search.split(' ')) == 1:
            return "WHERE surname LIKE '" + search + "%' "
        elif len(search.split(' ')) >= 2:
            return "WHERE surname LIKE '" + search.split(' ')[0] + "%' AND name LIKE '" + " ".join(search.split(' ')[1:]) + "%' "

    def populate(self):
        db = sql.connect(**config)
        cursor = db.cursor()
        key_search = self.sort_specific(self.ids.list_key_search.text)
        order_search = self.sort_list(self.ids.list_sort_by.text)
        cursor.execute("SELECT surname, name, age, year, global_moy, photo FROM etudiants " + key_search + order_search)
        data = cursor.fetchall()
        studs = []
        for etu in reversed(data):
            stud_dict = {"surname": etu[0], "name": etu[1], "age": etu[2], "year": etu[3], "global_moy": etu[4], "photo": etu[5]}
            studs.append(stud_dict)
        studs_lists = [i for i in self.ids.stud_lists.children]
        for stud_list in studs_lists:
            self.ids.stud_lists.remove_widget(stud_list)
        for etu in studs:
            stud = StudList()
            stud.ids.stud_list_surname.text = etu['surname']
            stud.ids.stud_list_name.text = etu['name'].upper()
            stud.ids.stud_list_age.text = str(etu['age'])
            stud.ids.stud_list_year.text = str(etu['year'])
            stud.ids.stud_list_global_moy.text = str(round(etu['global_moy'], 2))
            stud.ids.stud_list_picture.texture = CoreImage(io.BytesIO(etu['photo']), ext="png").texture
            self.ids.stud_lists.add_widget(stud)

class Trombi(Screen):
    pass
    # def on_enter(self):
    #     self.studs = ["Quentin DELCHIAPPO", "Bernard"]
    #     studs_trombis = [i for i in self.ids.trombi_studs.children]
    #     for trombi_stud in studs_trombis:
    #         self.ids.trombi_studs.remove_widget(trombi_stud)
    #     for studi in self.studs:
    #         trombi = TrombiStud()
    #         trombi.ids.trombi_stud_name.text = studi
    #         self.ids.trombi_studs.add_widget(trombi)
    
    # def search(self):
    #     print("searching : " + self.ids.trombi_search.text)

class StudentView(Screen):
    def on_pre_enter(self):
        self.ids.stud_view_moy_error.text = ""
        self.ids.stud_view_subject_choice_etu.text = "Matière ?"
        self.ids.stud_view_moyenne_etu.text = ""
        self.populate(choosen_surname, choosen_name)

    def populate(self, stud_surname, stud_name):
        db = sql.connect(**config)
        cursor = db.cursor()
        cursor.execute("SELECT id, age, year, global_moy, photo FROM etudiants WHERE surname = '" + stud_surname + "' AND name = '" + stud_name + "'")
        data = cursor.fetchone()
        stud_dict = {"ident": data[0], "age": data[1], "year": data[2], "global_moy": data[3], "photo": data[4]}
        self.ids.stud_view_picture.texture = CoreImage(io.BytesIO(stud_dict['photo']), ext="png").texture

        cursor.execute("SELECT subject, moy FROM matières WHERE id = '" + stud_dict["ident"] + "'")
        data = cursor.fetchall()
        stud_moys_list = []
        for moy in data:
            moy_dict = {"subject": moy[0], "moy": round(moy[1], 2)}
            stud_moys_list.append(moy_dict)
        stud_moys_del = [i for i in self.ids.stud_view_moys.children]
        for stud_moy_del in stud_moys_del:
            self.ids.stud_view_moys.remove_widget(stud_moy_del)
        for stud_moy_i in stud_moys_list:
            cursor.execute("SELECT MAX(moy) FROM matières INNER JOIN etudiants ON matières.id = etudiants.id WHERE subject = '" + stud_moy_i['subject'] + "' AND year = '" + stud_dict['year'] + "' LIMIT 1")
            data = cursor.fetchone()
            best_moy = data[0]
            stud_moy = EtuMoy()
            stud_moy.ids.stud_view_moy_subject.text = stud_moy_i['subject']
            stud_moy.ids.stud_view_moy_moy.text = str(round(stud_moy_i['moy'], 2))
            stud_moy.ids.stud_view_moy_best_moy.text = str(round(best_moy, 2))
            self.ids.stud_view_moys.add_widget(stud_moy)
        
        self.ids.stud_view_infos.text = "[b]" + stud_surname + " " + stud_name.upper() + "[/b]\n" + str(stud_dict['age']) + " ans\n" + stud_dict['year'] + "\nMoyenne générale : [b]" + str(round(stud_dict['global_moy'], 2)) + "[/b]"
        db.commit()
        db.close()

    def add_moy(self):
        if self.ids.stud_view_subject_choice_etu.text == "Matière ?":
            self.ids.stud_view_moy_error.text = "Matière invalide"
        elif self.ids.stud_view_moyenne_etu.text == "" or round(float(self.ids.stud_view_moyenne_etu.text), 2) < 0 or round(float(self.ids.stud_view_moyenne_etu.text), 2) > 20:
            self.ids.stud_view_moy_error.text = "Moyenne invalide"
        else:
            db = sql.connect(**config)
            cursor = db.cursor()
            cursor.execute("SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "' LIMIT 1")
            data = cursor.fetchone()
            ident = data[0]
            moy_add = [ident, self.ids.stud_view_subject_choice_etu.text, round(float(self.ids.stud_view_moyenne_etu.text), 2)]

            cursor.execute("SELECT count(*) FROM matières WHERE id = '" + ident + "' AND subject = '" + self.ids.stud_view_subject_choice_etu.text + "' LIMIT 1")
            subject_exist = cursor.fetchone()[0]
            if subject_exist == 0:
                cursor.execute("INSERT INTO matières (id, subject, moy) VALUES (%s, %s, %s)", moy_add)
                cursor.execute("UPDATE etudiants SET global_moy = (SELECT AVG (moy) FROM matières WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')) WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')")
                db.commit()
                db.close()
                App.get_running_app().root.current = "Liste"
                App.get_running_app().root.current = "StudentView"
            else:
                self.ids.stud_view_moy_error.text = "La matière existe déjà"
    
    def image_change(self):
        filechooser.open_file(on_selection=self.picture_selected)
        db = sql.connect(**config)
        cursor = db.cursor()
        new_image = [self.convert_pic(self.photo_path)]
        cursor.execute("UPDATE etudiants SET photo = %s WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')", new_image)
        db.commit()
        db.close()
        App.get_running_app().root.current = "Liste"
        App.get_running_app().root.current = "StudentView"

    def picture_selected(self, selection):
        if len(selection) >= 1:
            self.photo_path = selection[0].replace("\\", "/")
    
    def convert_pic(self, file_path):
        with open(file_path, 'rb') as file:
            photo = file.read()
        return photo

class StudList(BoxLayout):
    def stud_choose(self):
        global choosen_surname
        global choosen_name
        choosen_surname = self.ids.stud_list_surname.text
        choosen_name = self.ids.stud_list_name.text
        App.get_running_app().root.current = "StudentView"

class EtuMoy(BoxLayout):
    def moy_suppr(self):
        db = sql.connect(**config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM matières WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "') AND subject = '" + self.ids.stud_view_moy_subject.text + "'")
        cursor.execute("UPDATE etudiants SET global_moy = (SELECT AVG (moy) FROM matières WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')) WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')")
        if len(self.parent.children) <= 1:
            cursor.execute("DELETE FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "'")
            db.commit()
            db.close()
            App.get_running_app().root.current = "Liste"
        else:
            db.commit()
            db.close()
            App.get_running_app().root.current = "Liste"
            App.get_running_app().root.current = "StudentView"

class TrombiStud(BoxLayout):
    pass


class ButtonGrid(ButtonBehavior, BoxLayout):
    pass

class WindowManager(ScreenManager):
    pass

class etudos(App):
    def build(self):
        self.icon = "assets/logo.png"
        self.title = "Dossier étudiants"

if __name__ == "__main__":
    etudos().run()