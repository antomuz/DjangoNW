from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at', 'nsfw_score', 'faces_detected', 'favorite')
    search_fields = ('title',)
