import os
import uuid
from django.shortcuts import render
from images.models import Image
from analysis.services.clip import get_clip_embedding
import torch
from torch.nn.functional import cosine_similarity
from django.conf import settings

def save_temp_image(uploaded_file):
    temp_name = f"temp_{uuid.uuid4()}.jpg"
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp", temp_name)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    
    with open(temp_path, 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    return temp_path

def search_by_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        query_image = request.FILES['image']
        temp_path = save_temp_image(query_image)
        query_vector = torch.tensor(get_clip_embedding(temp_path))

        results = []
        for img in Image.objects.exclude(embedding=None):
            db_vector = torch.tensor(img.embedding)
            score = cosine_similarity(query_vector, db_vector, dim=0).item()
            results.append((img, score))

        results.sort(key=lambda x: x[1], reverse=True)
        top_images = [img for img, _ in results[:12]]

        return render(request, 'search/results.html', {'images': top_images})

    return render(request, 'search/upload.html')

def images_by_tag(request, tag):
    images = Image.objects.filter(tags__icontains=tag)
    return render(request, 'images/by_tag.html', {
        'images': images,
        'tag': tag
    })
