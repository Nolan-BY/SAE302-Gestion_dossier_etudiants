"""
SAE
Nolan Ben Yahya
"""

import socket, sys, json
import mysql.connector as sql

class Serveur():
    def __init__(self):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serveur.bind(('', 9999))
        except socket.error:
            print("La connexion du socket a échoué !")
            sys.exit()
        self.connexion()

    def connexion(self):
        while True:
            print("Serveur prêt ! En attente de requêtes...")
            self.serveur.listen(5)
            connexion, adresse = self.serveur.accept()
            print("Client connecté. Adresse : " + adresse[0])
            while True:
                requete = connexion.recv(1024)
                print("\nClient>", requete.decode("utf-8"))
                if requete.decode("utf-8").upper() == "FIN":
                    break
                elif requete.decode("utf-8").upper() in ["LOGIN", "ADD_STUD", "GET_STUDS"]:
                    format = requete.decode("utf-8").lower()
                    if format == "LOGIN":
                        db = sql.connect(host="127.0.0.1", database='bdetu', user="etuadmin", password="etuadmin")
                        cursor = db.cursor()
                        cursor.execute("SELECT identifiant, password FROM users LIMIT 1")
                        data = cursor.fetchone()
                        reponse = '{"id": data[0], "pass": data[1]}'
                    connexion.send(reponse.encode("utf-8"))

            connexion.send("Connexion fermée ! Au revoir".encode("utf-8"))
            print("Connexion interrompue.")
            connexion.close()

if __name__ == "__main__":
    Serveur()