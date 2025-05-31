from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from analysis.services.classifier import guess_category
from django.contrib.postgres.fields import ArrayField  # si PostgreSQL
import numpy as np
from analysis.services.clip import get_clip_embedding

def image_upload_path(instance, filename):
    return f'uploads/{timezone.now().date()}/{filename}'

class Image(models.Model):
    file = models.ImageField(upload_to=image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True)
    
    # Résultats IA
    tags = models.JSONField(default=list, blank=True)  # tags auto (ex: CLIP)
    nsfw_score = models.FloatField(null=True, blank=True)  # NSFW
    faces_detected = models.IntegerField(null=True, blank=True)
    dominant_color = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)  # Générée ou manuelle
    category = models.CharField(max_length=100, blank=True, null=True)
    
    favorite = models.BooleanField(default=False)
    
    # Métadonnées
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)  # En octets
    mime_type = models.CharField(max_length=50, blank=True)
    
    embedding = JSONField(null=True, blank=True)
    clip_embedding = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title or f'Image {self.id}'

    @property
    def file_name(self):
        return self.file.name.split('/')[-1]
    
def save(self, *args, **kwargs):
    if not self.clip_embedding and self.file:
        self.clip_embedding = get_clip_embedding(self.file.path)
    super().save(*args, **kwargs)
