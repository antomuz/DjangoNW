from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import Image
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import ImageEditForm
from django.db.models import Q
from collections import Counter
from itertools import chain
from django.db.models import Count
from images.utils import find_similar_images
from django.http import JsonResponse
from analysis.services import nsfw, clip
import json

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageUploadForm()
    
    return render(request, 'images/upload.html', {'form': form})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    similar = find_similar_images(image)
    return render(request, 'images/detail.html', {
        'image': image,
        'similar_images': similar,
    })

def toggle_favorite(request, pk):
    image = get_object_or_404(Image, pk=pk)
    image.favorite = not image.favorite
    image.save()
    return redirect('image_detail', pk=pk)

def edit_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    
    if request.method == 'POST':
        form = ImageEditForm(request.POST, instance=image)
        if form.is_valid():
            # Nettoyage simple : split string en liste si besoin
            tags = form.cleaned_data['tags']
            if isinstance(tags, str):
                image.tags = [tag.strip() for tag in tags.split(',')]
            form.save()
            return redirect('image_detail', pk=pk)
    else:
        form = ImageEditForm(instance=image)

    return render(request, 'images/edit.html', {'form': form, 'image': image})

def image_list(request):
    query = request.GET.get('q', '')
    images = Image.objects.all()

    if query:
        images = images.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'images/list.html', {'images': images, 'query': query})


def explore_tags(request):
    all_tags = Image.objects.values_list('tags', flat=True)
    flat_tags = list(chain.from_iterable(all_tags))  # liste unique
    tag_counts = Counter(flat_tags)

    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])  # tri par fréquence

    return render(request, 'images/explore_tags.html', {
        'tags': sorted_tags
    })
    
def favorites_view(request):
    images = Image.objects.filter(favorite=True).order_by('-uploaded_at')
    return render(request, 'images/favorites.html', {'images': images})


def image_list(request):
    query = request.GET.get('q', '')
    min_nsfw = request.GET.get('nsfw', '0')
    fav = request.GET.get('favorite')

    images = Image.objects.all()

    if query:
        images = images.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(description__icontains=query)
        )

    try:
        nsfw_val = float(min_nsfw)
        images = images.filter(nsfw_score__gte=nsfw_val)
    except (ValueError, TypeError):
        pass

    if fav is not None:  # ≠ 'on' seulement — juste présence du champ
        images = images.filter(favorite=True)

    return render(request, 'images/list.html', {
        'images': images,
        'query': query,
        'min_nsfw': min_nsfw,
        'fav': fav,
    })
    
def category_list(request):
    categories = Image.objects.values('category').annotate(count=Count('id')).order_by('-count')
    return render(request, 'images/categories.html', {'categories': categories})


def category_detail(request, slug):
    images = Image.objects.filter(category__iexact=slug)
    return render(request, 'images/category_detail.html', {
        'category': slug,
        'images': images
    })

def dashboard(request):
    total_images = Image.objects.count()
    unique_tags = Image.objects.values_list('tags', flat=True).distinct().count()

    tag_distribution = (
        Image.objects.values('tags')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    category_distribution = (
        Image.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    nsfw_bins = {
        '0–0.2': Image.objects.filter(nsfw_score__lt=0.2).count(),
        '0.2–0.5': Image.objects.filter(nsfw_score__gte=0.2, nsfw_score__lt=0.5).count(),
        '0.5–0.8': Image.objects.filter(nsfw_score__gte=0.5, nsfw_score__lt=0.8).count(),
        '0.8–1.0': Image.objects.filter(nsfw_score__gte=0.8).count(),
    }

    nsfw_count = Image.objects.filter(nsfw_score__gte=0.5).count()
    sfw_count = total_images - nsfw_count

    dominant_colors = (
        Image.objects.values('dominant_color')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    with_embedding = Image.objects.filter(clip_embedding__isnull=False).count()
    without_embedding = total_images - with_embedding

    context = {
        'total_images': total_images,
        'unique_tags': unique_tags,
        'tag_distribution': tag_distribution,
        'category_distribution': category_distribution,
        'nsfw_bins': nsfw_bins,
        'nsfw_count': nsfw_count,
        'sfw_count': sfw_count,
        'dominant_colors': dominant_colors,
        'with_embedding': with_embedding,
        'without_embedding': without_embedding,
    }
    return render(request, 'dashboard.html', context)

def regenerate_embeddings(request):
    if request.method == "POST":
        from analysis.services import clip  # ton module IA
        for image in Image.objects.filter(clip_embedding__isnull=True):
            clip.analyze(image)
            image.save()
        return JsonResponse({'status': 'done'})
    return JsonResponse({'status': 'invalid'})