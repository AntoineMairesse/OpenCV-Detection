import cv2
import pytesseract
import numpy as np

face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
# couleur du rectangle & texte
green = (36, 255, 12)
font = cv2.FONT_HERSHEY_SIMPLEX


def detect_faces(frame):
    # Image en noir et blanc
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Retourne les 4 points qui entourent le visage.
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)

    for (x, y, w, h) in faces:
        # On entoure le visage d'un rectangle vert et on met un label 'Tete' sur ce rectangle
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), green, 4)
        cv2.putText(frame, 'Tete', (x, y - 10), font, 1.6, green, 2)
    return frame


def detect_shapes(frame):
    polygones = ['Triangle', 'Quadrilatere', 'Pentagone', 'Hexagone', 'Heptagone', 'Octogone', 'Enneagone', 'Decagone',
                 'Hendecagone', 'Dodecagone']

    # On floute l'image
    blur = cv2.GaussianBlur(frame, (5, 5), 1)

    # Image en noir et blanc
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    # On détecte les bords des formes
    canny = cv2.Canny(gray, 23, 22)

    # On dilate l'image pour rendre les bords plus gros
    dil = cv2.dilate(canny, np.ones((5, 5)), iterations=1)

    # On trouve les contours des formes
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:

        # Si la surface de la forme est plus grande que 5000 unités
        if cv2.contourArea(contour) > 5000:

            # On dessine le contour de la forme en vert
            cv2.drawContours(frame, contours, -1, green, 4)

            # Perimètre de la forme
            peri = cv2.arcLength(contour, True)

            # Retourne une forme aproximative (simplifiée) de la forme originale (Algorithme de Douglas-Peucker)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

            # On récupère les coordonées du rectangle qui engloble la forme
            x, y, w, h = cv2.boundingRect(approx)

            # On donne un nom au polygone ou alors son nombre de points
            if 2 < len(approx) < 13:
                cv2.putText(frame, polygones[len(approx)-3], (x, y-20), font, 1.4, green, 2)
            else:
                cv2.putText(frame, "Points : " + str(len(approx)), (x, y-20), font, 1.4, green, 2)
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
                cv2.putText(frame, data[11], (x, y - 5), font, 1, green, 2)
    return frame
