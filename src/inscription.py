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

class formulaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire d'inscription")
        self.root.geometry("800x900+570+60")

        # Créer un Canvas qui couvre toute la fenêtre
        self.canvas = Canvas(self.root, bg="grey16", width=800, height=900)

        # Charger l'image
        self.background_image = PhotoImage(file="assets/images/bg33inscription.png")

        # Afficher l'image sur le Canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.background_image)

        # Pack le Canvas
        self.canvas.pack(fill=BOTH, expand=True)


        #champ de nom
        self.nom_entry = Entry(self.root,justify="center")
        self.nom_entry.insert(0, "Nom")

        self.nom_entry.place(x=272, y=280, height=50,width=300)
        self.nom_entry.bind("<FocusIn>", self.clear_placeholder)

        #champ de prénom
        self.prenom_entry = Entry(self.root,justify="center")
        self.prenom_entry.insert(0, "Prénom")

        self.prenom_entry.place(x=272, y=340, height=50,width=300)
        self.prenom_entry.bind("<FocusIn>", self.clear_placeholder)



        #champ de useranme
        self.login_entry = Entry(self.root,justify="center")
        self.login_entry.insert(0, "User name")

        self.login_entry.place(x=270, y=400, height=50,width=300)
        self.login_entry.bind("<FocusIn>", self.clear_placeholder)

         #champ de l'email
        self.email_entry = Entry(self.root, justify="center")
        self.email_entry.insert(0, "Email")
        
        self.email_entry.place(x=272, y=460, height=50,width=300)
        self.email_entry.bind("<FocusIn>", self.clear_placeholder)

         #champ de mot de passe 
        self.code_entry = Entry(self.root, justify="center")
        self.code_entry.insert(0, "mot de passe")
        
        self.code_entry.place(x=272, y=520, height=50,width=300)
        self.code_entry.bind("<FocusIn>", self.clear_placeholder)

        # Button for "s'inscrire"
        self.btn_inscrire = Button(self.root, text="s'inscrire", cursor="hand2", command=self.message, bg="#d0ad9f")
        self.btn_inscrire.place(x=272, y=600, height=50, width=300)

        # Button for "se connecter"
        self.btn_connecter = Button(self.root, text="se connecter", cursor="hand2", command=self.open_auth, bg="#d0ad9f")
        self.btn_connecter.place(x=272, y=660, height=50, width=300)


    # quand je clique sur un champ ce qui existe déjà doit disparaitre

    def clear_placeholder(self,event):
        if event.widget==self.prenom_entry and self.prenom_entry.get() == "Prénom":
            self.prenom_entry.delete(0, END)


        if event.widget==self.nom_entry and self.nom_entry.get() == "Nom":
            self.nom_entry.delete(0, END)

        if event.widget==self.email_entry and self.email_entry.get() == "Email":
            self.email_entry.delete(0, END)

        if event.widget==self.login_entry and self.login_entry.get() == "User name":
            self.login_entry.delete(0, END)

        if event.widget==self.code_entry and self.code_entry.get() == "mot de passe":
            self.code_entry.delete(0, END)
            event.widget.config(show="*")
    
    def open_auth(self):
        self.root.destroy()
        subprocess.run(["python", "src/auth.py"])

    # gérer les messages d'erreurs       
    def message(self):
        message=True
        if self.nom_entry.get() in ["","Nom"] or self.prenom_entry.get() in ["","Prénom"] or self.login_entry.get() in ["","User name"] or self.email_entry.get() in ["","Email"]  or self.code_entry.get() in ["","mot de passe"]:
            message=False
            messagebox.showerror("Erreur","attention un champ est vide!")


        # mot de passe :validation
       # if not self.validate_password(self.code_entry.get()):
        #    message=False
         #   messagebox.showerror("Erreur","attention mot de passe non sécurisé")
        # email:validation
        if not self.validate_email(self.email_entry.get()):
           message=False
           messagebox.showerror("Erreur","attention email!")
        if message:
            try:
                msg=True
                
                con = pymysql.connect(host="localhost", port=3307, user="root", password="", database="chess")
               
                
                cur=con.cursor()
                cur.execute("select * from players where email=%s ",self.email_entry.get())
                row_email=cur.fetchone()
                if row_email!=None:
                    msg=False
                    messagebox.showerror("erreur","ce email existe déjà!")
                cur.execute("select * from players where username=%s",self.login_entry.get())
                row_login=cur.fetchone()

                if row_login!=None:
                    msg=False
                    messagebox.showerror("erreur","ce Username existe déjà!")
                if msg:
                
                    cur.execute("insert into players(nom,prenom,username,email,motdepasse) values(%s,%s,%s,%s,%s)",
                                (self.prenom_entry.get(),
                                self.nom_entry.get(),
                                self.login_entry.get(),
                                self.email_entry.get(),
                                self.hash_password(self.code_entry.get()))
                                )
                    

                    
                    
                con.commit()
                con.close()
                messagebox.showinfo("sucess","inscription avec succès")
                self.open_auth()
                    
            except Exception as es:
                 messagebox.showerror("Erreur",f"Erreur de connexion:{str(es)}")
    # hashage de mot de passe
    def hash_password(self, password):
        # Hasher le mot de passe en utilisant SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self,password):
        # Vérifier si le mot de passe respecte les critères requis
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
        return re.match(regex, password)
       
    def validate_email(self,email):
        if "@" in email and "." in email :
            return True
        


root = Tk()
obj = formulaire(root)
root.mainloop()
