# photo_gallery/urls.py
from django.urls import path
from . import views

app_name = 'photo_gallery'
urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('create/', views.photo_create, name='photo_create'),
    path('<int:pk>/', views.photo_detail, name='photo_detail'),
    path('<int:pk>/edit/', views.photo_update, name='photo_update'),
    path('<int:pk>/delete/', views.photo_delete, name='photo_delete'),
    path('<int:pk>/like/', views.photo_like, name='photo_like'),
    path('my/', views.my_photos, name='my_photos'),
]
