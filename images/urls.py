from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('', views.image_list, name='image_list'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('image/<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('image/<int:pk>/edit/', views.edit_image, name='edit_image'),
    path('explore/', views.explore_tags, name='explore_tags'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/regenerate_embeddings/', views.regenerate_embeddings, name='regenerate_embeddings'),

]
