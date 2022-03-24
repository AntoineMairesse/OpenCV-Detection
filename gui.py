from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import cv2

from detection import *
import platform

bgColor = "#222831"
color2 = "#393E46"
color3 = "#00ADB5"
color4 = "#EEEEEE"
window = Tk()


class UserData(object):
    webcam = 0
    filename = None
    faces = StringVar()
    faces.set('0')
    colors = StringVar()
    colors.set('0')
    texts = StringVar()
    texts.set('0')
    shapes = StringVar()
    shapes.set('0')


user_choices = UserData()

# menu 1 = choix de départ
menu1 = Frame(window, bg=bgColor)

# menu 2 & 3 = choix des éléments à détecter
# (menu 2 = titres, menu 3 = checkbox + boutton)
menu2 = Frame(window, bg=bgColor)
menu3 = Frame(menu2, bg=bgColor)


# Cette fonction produit un espacement sur la frame passée en paramètre
def space(frame):
    espace = Label(frame, text='', font=("Courrier", 15), bg=bgColor, fg=bgColor)
    espace.pack()


def open_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Selectionnez un fichier",
                                          filetypes=[("image png", "*.png"), ("image jpg", "*.jpg"),
                                                     ("image jpeg", "*.jpeg"), ("video mp4", "*.mp4")])
    user_choices.filename = filename

    # si un fichier est sélectionné alors on change les menus
    if filename != "":
        menu1.forget()
        menu2.pack(expand=YES)
        menu3.pack(expand=YES)


def build_canvas(img):
    canvas = img
    if user_choices.faces.get() == '1':
        canvas = detect_faces(img)
    if user_choices.shapes.get() == '1':
        canvas = detect_shapes(img)
    if user_choices.texts.get() == '1':
        canvas = detect_text(img)
    if user_choices.colors.get() == '1':
        canvas = detect_colors(img)
    return canvas


def launch_detection():
    window.destroy()
    # Si l'utilisateur a choisi la webcam
    if user_choices.webcam == 1:
        video_capture = cv2.VideoCapture(0)
        while video_capture.isOpened():
            # Capture la video image par image
            _, frame = video_capture.read()
            canvas = build_canvas(frame)

            # Nouvelle fenetre 'Video' qui affiche le résultat
            print(frame.shape[0], frame.shape[1])
            cv2.putText(canvas, 'Appuyez sur Q pour fermer le programme', (10, 35),
                        font, 0.9, (0, 0, 255), 2)
            cv2.imshow('Video', canvas)

            # Si l'utilisateur appuies sur la touche q, le programme s'arrête
            if cv2.waitKey(1) & 0xff == ord('q'):
                return

        # On ferme la capture vidéo et on détruit les fenêtres.
        video_capture.release()
        cv2.destroyAllWindows()
    else:
        # Si l'utilisateur a bien choisi un fichier
        if user_choices.filename is not None:

            # On récupère l'extension du fichier
            length = len(user_choices.filename)
            extension = user_choices.filename[length - 4:length]

            # Si le fichier est une vidéo
            if extension == ".mp4":

                video = cv2.VideoCapture(user_choices.filename)
                frame_counter = 0.0

                while video.isOpened():

                    # On loop sur la vidéo
                    if frame_counter == video.get(cv2.CAP_PROP_FRAME_COUNT):
                        frame_counter = 0
                        video.set(cv2.CAP_PROP_FRAME_COUNT, 0)
                        video.release()
                        video = cv2.VideoCapture(user_choices.filename)

                    # On prend la frame de la vidéo puis on build le canvas à partir de celle-ci
                    _, frame = video.read()
                    frame_counter += 1
                    canvas = build_canvas(frame)

                    ratio = frame.shape[1] / frame.shape[0]

                    # Nouvelle fenetre 'Video' qui affiche le résultat
                    cv2.putText(canvas, 'Appuyez sur Q pour fermer le programme', (10, 35),
                                font, 0.4*ratio, (0, 0, 255), 2)
                    cv2.imshow('Video', canvas)

                    # Si l'utilisateur appuies sur la touche q, le programme s'arrête
                    if cv2.waitKey(1) & 0xff == ord('q'):
                        return

                    # On ferme la capture vidéo et on détruit les fenêtres.
                video.release()
                cv2.destroyAllWindows()

            # Si le fichier est une image
            else:

                # On build le canvas à partir de l'image
                img = cv2.imread(user_choices.filename)
                canvas = build_canvas(img)

                # Nouvelle fenetre 'Image' qui affiche le résultat
                cv2.putText(canvas, 'Appuyez sur une touche pour fermer le programme', (10, 35),
                            font, 1.4, (0, 0, 255), 2)
                cv2.imshow('Image', canvas)

                # Si l'utilisateur appuies sur une touche, le programme s'arrête
                cv2.waitKey(0)
                # On détruit les fenêtres.
                cv2.destroyAllWindows()


def set_webcam():
    user_choices.webcam = 1
    menu1.forget()
    menu2.pack(expand=YES)
    menu3.pack(expand=YES)


def create_button(menu, text, variable):
    if platform.system() == 'Darwin':
        Checkbutton(menu, text=text, background=bgColor, foreground=color4,
                    font=("Courrier", 20), pady=10, variable=variable, onvalue=1, offvalue=0).pack(anchor='w')
    elif platform.system() == 'Windows':
        ttk.Checkbutton(menu, text=text, onvalue=1, offvalue=0, variable=variable, style='A.TCheckbutton').pack(
            anchor='w')
    pass


def main():
    # On définit les propriétés de la fenêtre (titre, taille, couleur de fond)
    window.title('Reconnaissance de texte')
    window.geometry("800x800")
    window.minsize(800, 800)
    window.maxsize(800, 800)
    window.config(background=bgColor)

    # On définit un style pour les widgets, ici un style "A" qui est appliqué aux boutons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('A.TButton', font=('Courrier', 20), background=color2, foreground='white', padding=15)
    style.map('A.TButton', background=[('active', bgColor)])
    style.configure('A.TCheckbutton', background=bgColor, foreground=color4, font=("Courrier", 20), pady=10)
    style.map('A.TCheckbutton', background=[('active', bgColor)])

    # Titre + espace
    Label(menu1, text="Reconnaissance d'éléments", font=("Courrier", 40), bg=bgColor, fg="white").pack()
    space(frame=menu1)

    # Texte + espace
    Label(menu1, text="Quelle source voulez vous utiliser ?", font=("Courrier", 30), bg=bgColor, fg="white").pack()
    space(frame=menu1)

    # Bouton webcam
    webcam_button = ttk.Button(menu1, text="Webcam", style='A.TButton', command=set_webcam)
    webcam_button.pack(side=LEFT, expand=YES)

    # Bouton choix de fichier
    file_button = ttk.Button(menu1, text="Fichier vidéo / image", style='A.TButton', command=open_file)
    file_button.pack(side=LEFT, expand=YES)

    # Titre + espace
    Label(menu2, text="Reconnaissance d'élements", font=("Courrier", 40), bg=bgColor, fg="white").pack()
    space(frame=menu2)

    # Texte + espace
    Label(menu2, text="Que voulez-vous détecter ?", font=("Courrier", 30), bg=bgColor, fg="white").pack()
    space(frame=menu2)

    # Boutons de choix + espace
    create_button(menu3, "Reconnaissance Faciale", user_choices.faces)
    create_button(menu3, "Couleurs", user_choices.colors)
    create_button(menu3, "Texte", user_choices.texts)
    create_button(menu3, "Formes", user_choices.shapes)
    space(frame=menu3)

    # Bouton pour lancer la détection
    ttk.Button(menu3, text="Go !", style='A.TButton', command=launch_detection).pack(expand=YES)

    menu1.pack(expand=YES)
    # afficher la fenetre
    window.mainloop()
