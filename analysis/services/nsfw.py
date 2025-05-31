from PIL import Image as PILImage
import numpy as np

# Exemple très simple avec un modèle dummy (à remplacer par vrai NSFW model plus tard)
def get_nsfw_score(image_path):
    # TODO: utiliser un modèle pré-entraîné comme Yahoo OpenNSFW ou NudeNet
    import random
    return round(random.uniform(0, 1), 2)
