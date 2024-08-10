from tkinter import *
import tkinter as tk
from tkcalendar import *
from tkinter import ttk,messagebox,PhotoImage
import pymysql
import os 
from const import *
import hashlib
import re 
import subprocess
class Auth:
    def __init__(self,root):
       self.root=root
       self.root.title("Formulaire d'inscription")
       self.root.geometry("800x900+570+60")

       # Créer un Canvas qui couvre toute la fenêtre
       self.canvas = Canvas(self.root, bg="grey16", width=800, height=900)

        # Charger l'image
       self.background_image = PhotoImage(file="assets/images/bg33auth.png")

        # Afficher l'image sur le Canvas
       self.canvas.create_image(0, 0, anchor=NW, image=self.background_image)

        # Pack le Canvas
       self.canvas.pack(fill=BOTH, expand=True)

        #champ de useranme
       self.login_entry = Entry(self.root,justify="center")
       self.login_entry.insert(0, "User name")

       self.login_entry.place(x=272, y=300, height=50,width=300)
       self.login_entry.bind("<FocusIn>", self.clear_placeholder)

          #champ de mot de passe 
       self.code_entry = Entry(self.root, justify="center")
       self.code_entry.insert(0, "mot de passe")
        
       self.code_entry.place(x=272, y=360, height=50,width=300)
       self.code_entry.bind("<FocusIn>", self.clear_placeholder)

        # botton
       self.btn = Button(self.root,text="se connecter", cursor="hand2", command=self.message, bg="#d0ad9f").place(x=272, y=440, height=50,width=300)
        # botton
       self.btn = Button(self.root,text="s'inscrire", cursor="hand2", command=self.open_inscription, bg="#d0ad9f").place(x=272, y=495, height=50,width=300)

    def clear_placeholder(self,event):
             if event.widget==self.login_entry and self.login_entry.get() == "User name":
                self.login_entry.delete(0, END)

             if event.widget==self.code_entry and self.code_entry.get() == "mot de passe":
                self.code_entry.delete(0, END)
                event.widget.config(show="*")
    def open_inscription(self):
         # Fermer la fenêtre principale
         self.root.destroy()
          # Si les informations sont correctes, ouvrir l'interface Pygame
         subprocess.run(["python","src//test_fi.py"])
          
    def message(self):
        message=True
        if  self.login_entry.get() in ["","User name"] or self.code_entry.get() in ["","mot de passe"]:
            message=False
            messagebox.showerror("Erreur","attention un champ est vide!")
        if message:
            con = pymysql.connect(host="localhost", port=3307, user="root", password="", database="chess")
                        
            cur=con.cursor()
            cur.execute("select * from players where username=%s ",self.login_entry.get())
            row_login=cur.fetchone()
            var=True
            
            if row_login is None:
                 var=False
                 messagebox.showerror("Erreur","ce username n'existent pas!")
                 # si ya pas de username correspon je dois sortir  et ne pas vérifier mdp  
                 exit()             
      
            hashed_password_db=row_login[5]
           
            # Vérifier si le mot de passe entré correspond au mot de passe haché dans la base de données
            if hashed_password_db !=self.hash_password(self.code_entry.get()):
               var=False

               messagebox.showerror("Erreur", "Mot de passe incorrect !")
            if var:
               # Si les informations sont correctes, ouvrir l'interface Pygame
               self.root.destroy()
                                                            
               subprocess.run(["python","src//main.py"])
               
     # hashage de mot de passe
    def hash_password(self, password):
        # Hasher le mot de passe en utilisant SHA-256
        return hashlib.sha256(password.encode()).hexdigest()       
      
root = Tk()
obj =Auth(root)
root.mainloop()
