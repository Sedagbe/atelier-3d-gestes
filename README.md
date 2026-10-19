# Atelier 3D piloté par la main

Visualiseur 3D de 10 équipements (avion, voiture, appareils biomédicaux dont l'IRM…) contrôlé **uniquement avec la main devant une webcam** : rotation, vue éclatée, vue rayons X, détail des pièces, zoom à deux mains.

Projet de 3ᵉ année Cybersécurité & IA, ESEO Vélizy.

## Fonctionnement

- Détection de la main : MediaPipe Hand Landmarker (21 points par main), exécuté dans le navigateur.
- Scène 3D : Three.js.
- Les images de la caméra restent sur l'ordinateur, rien n'est envoyé à un serveur.
- Les scripts et le modèle sont chargés depuis un CDN : une connexion internet est nécessaire.

## Lancer la démo

```bash
python -m http.server 8000
```

Puis ouvrir <http://localhost:8000/> et autoriser la caméra (la page doit être servie en `localhost`, pas ouverte en `file://`).

## Gestes

| Geste | Action |
| --- | --- |
| Pointer un doigt, immobile ~1,1 s | Cliquer (choisir un équipement, une pièce) |
| Balayage de la main | Tourner / changer d'équipement |
| Poing maintenu ~0,6 s | Vue éclatée / rayons X |
| Deux paumes qui s'écartent | Zoom |

## Compteur de doigts (point de départ)

```bash
cd compteur_doigts
pip install -r requirements.txt
python compteur_doigts.py
```

Le modèle `hand_landmarker.task` est téléchargé au premier lancement. Quitter avec `q`.

## Contenu

- `index.html` : application 3D gestuelle.
- `compteur_doigts/` : compteur de doigts (API Tasks de MediaPipe).
- `docs/presentation.pptx` : support de présentation.

## Limites connues

Détection sensible à la lumière et aux mains partiellement cachées ; modèles 3D simplifiés (formes de base), à but illustratif.
