import cv2

face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('resources/haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier('resources/haarcascade_eye.xml')


def detect_faces(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # retourne les 4 points qui entourent le visage.
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

    # couleur du rectangle & texte
    green = (36, 255, 12)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), green, 2)
        cv2.putText(frame, 'Tete', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, green, 2)

    return frame
