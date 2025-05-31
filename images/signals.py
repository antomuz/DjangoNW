from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Image
from analysis.services import nsfw, clip

@receiver(post_save, sender=Image)
def run_image_analysis(sender, instance, created, **kwargs):
    if created:
        print(f"[IA] Analyse de l'image : {instance.file.name}")

        # Analyse NSFW
        instance.nsfw_score = nsfw.get_nsfw_score(instance.file.path)
        print(f"[NSFW] Score : {instance.nsfw_score}")

        # Analyse CLIP (tags)
        instance.tags = clip.generate_tags(instance.file.path)
        print(f"[CLIP] Tags : {instance.tags}")

        instance.save()
