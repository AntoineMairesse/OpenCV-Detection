import cv2
import pytesseract
import pytesseract as pyt

face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('resources/haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier('resources/haarcascade_eye.xml')
# couleur du rectangle & texte
green = (36, 255, 12)
font = cv2.FONT_HERSHEY_SIMPLEX


def detect_faces(frame):
    # Image en noir et blanc
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # retourne les 4 points qui entourent le visage.
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # On entoure le visage d'un rectangle vert et on met un label 'Tete' sur ce rectangle
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), green, 2)
        cv2.putText(frame, 'Tete', (x, y - 10), font, 0.9, green, 2)

    return frame


def detect_shapes(frame):
    return frame


def detect_colors(frame):
    return frame


def detect_text(frame):
    # on récupère les data de l'image
    d = pytesseract.image_to_data(frame)
    # on découpe la data dans une liste puis on itère dessus
    for count, data in enumerate(d.splitlines()):
        # 1ère itération = nom des colonnes
        if count != 0:
            data = data.split()
            # si data contient un mot
            if len(data) == 12:
                # on récupère les coordonnées du rectangle qui entoure le mot puis on affiche celui-ci avec le mot.
                x, y, w, h = int(data[6]), int(data[7]), int(data[8]), int(data[9])
                cv2.rectangle(frame, (x, y), (w + x, h + y), green, 3)
                cv2.putText(frame, data[11], (x, y), font, 1, green, 2)
    return frame
