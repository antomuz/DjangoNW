from django.urls import path
from . import views

urlpatterns = [
    path('similar/', views.search_by_image, name='search_by_image'),
    path('tag/<str:tag>/', views.images_by_tag, name='images_by_tag'),
]
