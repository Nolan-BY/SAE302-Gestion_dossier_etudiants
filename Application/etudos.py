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

# Initialise la configuration de la base de données
config = {'host': '127.0.0.1',
          'database': 'bdetu',
          'user': 'etuadmin',
          'password': 'etuadmin'}

class Login(Screen):
    # Lorsque l'écran est quitté, on remet à zéro les champs d'identifiant et de mot de passe
    def on_leave(self):
        self.ids.connect_login.text = ''
        self.ids.connect_mdp.text = ''

    # Lorsqu'on clique sur le bouton "Connexion", les identifiants rentrés sont comparés à ceux existants dans la BDD
    def connect(self):
        db = sql.connect(**config)
        cursor = db.cursor()
        cursor.execute("SELECT identifiant, password FROM users")
        data = cursor.fetchall()
        users = []
        log = False

        # Boucle pour créer une liste d'utilisateurs sous forme de dictionnaires
        for user in data:
            users_dict = {'ident': user[0], 'pass': user[1]}
            users.append(users_dict)
        
        # Boucle pour vérifier les identifiants saisis avec les utilisateurs de la liste
        for user in users:
            if self.ids.connect_login.text == user['ident'] and self.ids.connect_mdp.text == user['pass']:
                log = True
                App.get_running_app().root.current = "NavigProf"

        if log == False:
            self.ids.login_error.text = "Identifiants invalides !"
    
    # Réinitialise le Label affichant les erreurs sur la page
    def reset_err_msg(self):
        self.ids.login_error.text = ""

class NavigProf(Screen):
    pass

class Add(Screen):
    def __init__(self, **kw):
        super(Add, self).__init__(**kw)
        Window.bind(on_drop_file=self.drop_file)
        self.photo_path = ''

    # Lorsque l'utilisateur glisse un fichier sur le champ "photo",
    # le nom du fichier sélectionné est affiché et le chemin de ce fichier est stocké
    def drop_file(self, window, file_path, x, y):
        self.ids.picture_add_etu.text = str(file_path).split("\\")[-1].strip("'").replace(" ", "_")
        self.photo_path = str(file_path).replace("\\", "/")
    
    # Ouvre une fenêtre de sélection de fichier pour permettre à l'utilisateur de sélectionner une photo
    def file_chooser(self):
        filechooser.open_file(on_selection=self.picture_selected)

    # Lorsque l'utilisateur sélectionne une photo, afficher le nom de la photo sélectionnée et stock le chemin de cette photo
    def picture_selected(self, selection):
        if len(selection) >= 1:
            self.ids.picture_add_etu.text = selection[0].split("\\")[-1].strip("'").replace(" ", "_")
            self.photo_path = selection[0].replace("\\", "/")
    
    # Converti la photo sélectionnée en format binaire pour pouvoir l'enregistrer dans la base de données
    def convert_pic(self, file_path):
        with open(file_path, 'rb') as file:
            photo = file.read()
        return photo

    # Réinitialise les champs de saisie.
    # Si le type est "ALL", tous les champs et le message d'erreur sont réinitialisés.
    # Si le type est "ERR", tous les champs sauf le message d'erreur sont réinitialisés.
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

    # Lorsque l'utilisateur quitte cet écran on réinitialiser tous les champs de saisie
    def on_leave(self):
        self.reset("ALL")

    # Lorsque l'utilisateur clique sur le bouton "Ajouter",
    # on vérifie que tous les champs sont remplis et que l'étudiant n'existe pas déjà dans la base de données.
    # Si tout est valide, on enregistre les informations de l'étudiant dans la base de données.
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

    # Juste avant que l'utilisateur entre sur cet écran,
    # on remplit la liste d'étudiants en utilisant les options de tri et de recherche sélectionnées par l'utilisateur.
    def on_pre_enter(self):
        self.populate()
    
    # Lorsque l'utilisateur quitte cet écran,
    # on réinitialise les champs de recherche et de tri.
    def on_leave(self):
        self.ids.list_key_search.text = ""
        self.ids.list_sort_by.text = "Trier par"
    
    # Détermine la requête SQL à utiliser en fonction de l'option de tri sélectionnée par l'utilisateur.
    def sort_list(self, search):
        search_list = {"1A": "AND year = '1A'", "2A": "AND year = '2A'",
                        "Prénoms A-Z": "ORDER BY surname", "Prénoms Z-A": "ORDER BY surname DESC",
                        "Noms A-Z": "ORDER BY name", "Noms Z-A": "ORDER BY name DESC",
                        "Age >": "ORDER BY age", "Age <": "ORDER BY age DESC",
                        "Moyenne G >": "ORDER BY global_moy", "Moyenne G <": "ORDER BY global_moy DESC"}

        if search == "Trier par":
            return ""
        return search_list[search]

    # Détermine la requête SQL à utiliser en fonction de la recherche spécifique saisie par l'utilisateur.
    def sort_specific(self, search):
        if len(search.split(' ')) == 1:
            return "WHERE surname LIKE '" + search + "%' "
        elif len(search.split(' ')) >= 2:
            return "WHERE surname LIKE '" + search.split(' ')[0] + "%' AND name LIKE '" + " ".join(search.split(' ')[1:]) + "%' "

    # Remplie la liste d'étudiants en utilisant les options de tri et de recherche sélectionnées par l'utilisateur.
    # Effectue ensuite une requête SQL pour récupérer les données des étudiants de la base de données,
    # puis met à jour l'affichage de la liste en utilisant ces données.
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

class StudList(BoxLayout):

    # Définit les variables globales choosen_surname et choosen_name lors de la sélection d'un étudiant
    # à partir des données présentes dans les Labels "stud_list_surname" et "stud_list_name" respectivement.
    def stud_choose(self):
        global choosen_surname
        global choosen_name
        choosen_surname = self.ids.stud_list_surname.text
        choosen_name = self.ids.stud_list_name.text
        App.get_running_app().root.current = "StudentView"

class StudentView(Screen):

    # Lorsque l'écran StudentView est affiché pour la première fois ou lorsqu'il est réaffiché,
    # on réinitialise les champs d'erreur, de choix de matière et de moyenne à zéro
    # et on appelle la fonction populate pour mettre à jour l'affichage de l'écran avec les informations de l'étudiant sélectionné,
    # en utilisant les variables choosen_surname et choosen_name pour identifier l'étudiant.
    def on_pre_enter(self):
        self.ids.stud_view_moy_error.text = ""
        self.ids.stud_view_subject_choice_etu.text = "Matière ?"
        self.ids.stud_view_moyenne_etu.text = ""
        self.populate(choosen_surname, choosen_name)

    # Remplie les différents éléments de l'interface avec les informations de l'étudiant sélectionné.
    # Prend en paramètres le nom et le prénom de l'étudiant sélectionné.
    # Récupère les informations de l'étudiant sélectionné (id, age, année, moyenne générale, photo).
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

        # Les données récupérées sont stockées dans un dictionnaire qui est ensuite utilisé pour remplir les éléments de l'interface.
        for moy in data:
            moy_dict = {"subject": moy[0], "moy": round(moy[1], 2)}
            stud_moys_list.append(moy_dict)
        
        # Supprime les moyennes qui pourraient être déjà présentes dans la liste suite à de précédentes requêtes.
        stud_moys_del = [i for i in self.ids.stud_view_moys.children]
        for stud_moy_del in stud_moys_del:
            self.ids.stud_view_moys.remove_widget(stud_moy_del)

        # Récupère les moyennes de l'étudiant pour chaque matière à partir de la table 'matières' en utilisant l'id de l'étudiant récupéré précédemment.
        for stud_moy_i in stud_moys_list:
            cursor.execute("SELECT MAX(moy) FROM matières INNER JOIN etudiants ON matières.id = etudiants.id WHERE subject = '" + stud_moy_i['subject'] + "' AND year = '" + stud_dict['year'] + "' LIMIT 1")
            data = cursor.fetchone()
            best_moy = data[0]

            # Les données récupérées sont utilisées pour remplir les éléments de l'interface.
            stud_moy = EtuMoy()
            stud_moy.ids.stud_view_moy_subject.text = stud_moy_i['subject']
            stud_moy.ids.stud_view_moy_moy.text = str(round(stud_moy_i['moy'], 2))
            stud_moy.ids.stud_view_moy_best_moy.text = str(round(best_moy, 2))
            self.ids.stud_view_moys.add_widget(stud_moy)
        
        # Met à jour les informations de l'étudiant sélectionné dans l'interface et commit les modifications avant de fermer la connexion à la base de données.
        self.ids.stud_view_infos.text = "[b]" + stud_surname + " " + stud_name.upper() + "[/b]\n" + str(stud_dict['age']) + " ans\n" + stud_dict['year'] + "\nMoyenne générale : [b]" + str(round(stud_dict['global_moy'], 2)) + "[/b]"
        db.commit()
        db.close()

    # Permet d'ajouter une moyenne pour un étudiant sélectionné.
    def add_moy(self):

        # Vérifie d'abord que les champs "Matière ?" et "Moyenne" ne sont pas vides ou incorrects.
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

            # Vérifie si la matière saisie existe déjà pour cet étudiant, et si ce n'est pas le cas, l'ajoute avec sa moyenne.
            if subject_exist == 0:
                cursor.execute("INSERT INTO matières (id, subject, moy) VALUES (%s, %s, %s)", moy_add)

                # La moyenne générale de l'étudiant est ensuite mise à jour.
                cursor.execute("UPDATE etudiants SET global_moy = (SELECT AVG (moy) FROM matières WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')) WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')")
                db.commit()
                db.close()

                # La page est rafraîchie pour afficher les nouvelles données.
                App.get_running_app().root.current = "Liste"
                App.get_running_app().root.current = "StudentView"
            else:
                self.ids.stud_view_moy_error.text = "La matière existe déjà"
    
    # Permet de changer l'image de l'étudiant en cliquant sur la photo affichée sur la page
    def image_change(self):

        # Ouvre un sélecteur de fichiers pour choisir une image
        filechooser.open_file(on_selection=self.picture_selected)
        db = sql.connect(**config)
        cursor = db.cursor()

        # Création d'une variable pour stocker l'image convertie
        new_image = [self.convert_pic(self.photo_path)]

        # Mise à jour de l'image dans la base de données pour l'étudiant sélectionné
        cursor.execute("UPDATE etudiants SET photo = %s WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')", new_image)
        
        # Enregistrement des modifications dans la base de données et fermeture de la connexion
        db.commit()
        db.close()

        # La page est rafraîchie pour afficher les nouvelles données
        App.get_running_app().root.current = "Liste"
        App.get_running_app().root.current = "StudentView"

    def picture_selected(self, selection):
        if len(selection) >= 1:
            self.photo_path = selection[0].replace("\\", "/")
    
    def convert_pic(self, file_path):
        with open(file_path, 'rb') as file:
            photo = file.read()
        return photo

class EtuMoy(BoxLayout):

    # Permet de supprimer une moyenne en appuyant sur un bouton de supppression
    def moy_suppr(self):
        db = sql.connect(**config)
        cursor = db.cursor()

        # On supprime la moyenne de la matière sélectionnée pour l'étudiant actuel
        cursor.execute("DELETE FROM matières WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "') AND subject = '" + self.ids.stud_view_moy_subject.text + "'")
        
        # On met à jour la moyenne générale de l'étudiant
        cursor.execute("UPDATE etudiants SET global_moy = (SELECT AVG (moy) FROM matières WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')) WHERE id = (SELECT id FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "')")
        
        # Si l'étudiant n'a plus de moyennes, on le supprime de la base de données
        if len(self.parent.children) <= 1:
            cursor.execute("DELETE FROM etudiants WHERE surname = '" + choosen_surname + "' AND name = '" + choosen_name + "'")
            db.commit()
            db.close()
            App.get_running_app().root.current = "Liste"
        
        # Sinon, on met à jour l'affichage
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