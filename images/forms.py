from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'title']
        
class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['tags', 'description']
        widgets = {
            'tags': forms.Textarea(attrs={'rows': 2, 'placeholder': 'ex: cat, sunset, anime'}),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'ex: Image générée par IA représentant...'}),
        }
