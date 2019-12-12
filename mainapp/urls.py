from django.urls import path
from . import views
from kinopoisk import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'mainapp'


urlpatterns = [
    path('', views.index, name="index"),
    path('movie/<int:movie_id>', views.movie, name='movie'),
    path('search/', views.search, name="search"),
    path('registration', views.registration, name="registration"),
    path('authentication', views.authentication, name="authentication"),
    path('exit_from_account', views.exit_from_account, name="exit_from_account"),
    path('post_comment', views.post_comment, name="post_comment"),
    path('user/<int:userx_id>', views.user, name='user'),
    path('user/ban/<int:userx_id>', views.ban_user, name="ban_user"),
    path('movie/delete_comment/<int:movie_id>', views.delete_comment, name="delete_comment"),
    path('rate_movie/<int:movie_id>', views.rate_movie, name="rate_movie"),
    path('movie/like_comment/', views.like_comment, name="like_comment"),
    path('movie/delete_like_comment/', views.like_comment, name="delete_like_comment"),
    path('user/report_user', views.report_user, name="report_user"),
    path('movie/add_to_favorite', views.add_to_favorite, name="add_to_favorite"),
    path('movie/add_to_wl', views.add_to_wl, name="add_to_wl"),
    path('movie/delete_from_wl', views.delete_from_wl, name="delete_from_wl"),
    path('movies_by_genre/<int:genre_id>', views.movies_by_genre, name="movies_by_genre"),
    path('movies_by_country/<int:country_id>', views.movies_by_country, name="movies_by_country"),
    path('movies_by_category/<int:category_id>', views.movies_by_category, name="movies_by_category"),
    path('movies_by_person/<int:person_id>', views.movies_by_person, name="movies_by_person"),
    path('random_movie', views.random_movie, name="random_movie"),
    path('add_new_movie', views.add_new_movie, name='add_new_movie'),
    path('add_new_category', views.add_new_category, name='add_new_category'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
