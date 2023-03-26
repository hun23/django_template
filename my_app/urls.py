from django.urls import path
from . import views

app_name = "my_app"
urlpatterns = [
    path("index/", views.index, name="index"),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
]
