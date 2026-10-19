"""
Compteur de doigts en temps réel (webcam) - version MediaPipe récent (API Tasks)
--------------------------------------------------------------------------------
Dépendances : pip install opencv-python mediapipe
Lancer      : python compteur_doigts_v2.py
Quitter     : touche 'q'

Au premier lancement, le modèle hand_landmarker.task (~8 Mo) est téléchargé
automatiquement à côté du script.
"""

import math
import os
import time
import urllib.request

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

URL_MODELE = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
CHEMIN_MODELE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

# Indices des points (landmarks)
POIGNET = 0
POUCE_IP, POUCE_BOUT = 3, 4
PETIT_MCP = 17
DOIGTS = [(6, 8), (10, 12), (14, 16), (18, 20)]  # (PIP, bout) : index, majeur, annulaire, auriculaire

# Connexions pour dessiner le squelette de la main
CONNEXIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
]


def telecharger_modele():
    if not os.path.exists(CHEMIN_MODELE):
        print("Téléchargement du modèle de détection de main...")
        urllib.request.urlretrieve(URL_MODELE, CHEMIN_MODELE)
        print("Modèle téléchargé.")


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def compter_doigts(points):
    """Nombre de doigts levés (0 à 5) pour une main."""
    total = 0

    # Pouce : levé si son bout est plus loin de la base du petit doigt que son articulation IP
    if distance(points[POUCE_BOUT], points[PETIT_MCP]) > distance(points[POUCE_IP], points[PETIT_MCP]):
        total += 1

    # Autres doigts : levés si le bout est plus loin du poignet que l'articulation PIP
    for pip, bout in DOIGTS:
        if distance(points[bout], points[POIGNET]) > distance(points[pip], points[POIGNET]):
            total += 1

    return total


def dessiner_main(image, points):
    h, w = image.shape[:2]
    coords = [(int(p.x * w), int(p.y * h)) for p in points]
    for a, b in CONNEXIONS:
        cv2.line(image, coords[a], coords[b], (255, 200, 0), 2)
    for c in coords:
        cv2.circle(image, c, 4, (0, 0, 255), -1)


def main():
    telecharger_modele()

    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=CHEMIN_MODELE),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise SystemExit("Impossible d'ouvrir la webcam.")

    debut = time.time()

    with vision.HandLandmarker.create_from_options(options) as detecteur:
        while True:
            ok, image = camera.read()
            if not ok:
                break

            image = cv2.flip(image, 1)  # effet miroir
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            horodatage_ms = int((time.time() - debut) * 1000)
            resultat = detecteur.detect_for_video(image_mp, horodatage_ms)

            total = 0
            for points in resultat.hand_landmarks:
                dessiner_main(image, points)
                total += compter_doigts(points)

            cv2.putText(image, f"Doigts : {total}", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
            cv2.imshow("Compteur de doigts", image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
