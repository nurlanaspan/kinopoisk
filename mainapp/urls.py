from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name="index"),
    path('movie/<int:movie_id>', views.movie, name='movie'),
    path('search/', views.search, name="search"),
    path('registration', views.registration, name="registration"),
    path('authentication', views.authentication, name="authentication"),
    path('exit_from_account', views.exit_from_account, name="exit_from_account"),
    path('post_comment', views.post_comment, name="post_comment")
]
