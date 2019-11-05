from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name="index"),
    path('movie/<int:movie_id>', views.movie, name='movie'),
]
