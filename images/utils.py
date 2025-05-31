from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_similar_images(image, top_n=4):
    if not image.clip_embedding:
        return []

    all_images = image.objects.exclude(id=image.id).exclude(clip_embedding=None)

    similarities = []
    for other in all_images:
        sim = cosine_similarity(
            [image.clip_embedding],
            [other.clip_embedding]
        )[0][0]
        similarities.append((other, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [img for img, score in similarities[:top_n]]
