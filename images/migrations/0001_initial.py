# Generated by Django 5.0.3 on 2025-05-30 23:24

import images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to=images.models.image_upload_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('nsfw_score', models.FloatField(blank=True, null=True)),
                ('faces_detected', models.IntegerField(blank=True, null=True)),
                ('dominant_color', models.CharField(blank=True, max_length=20)),
                ('description', models.TextField(blank=True)),
                ('favorite', models.BooleanField(default=False)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('mime_type', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
