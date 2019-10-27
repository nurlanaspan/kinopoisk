from django.db import models

# Create your models here.
class Genre(models.Model):
    genre_id = models.CharField(max_length=9999)
    genre_name = models.CharField(max_length=100)


class Movie(models.Model):
    movie_id = models.CharField(max_length=9999)
    movie_name = models.CharField(max_length=100)
    movie_desctiption = models.TextField()
    movie_main_rating = models.FloatField()
    movie_user_rating = models.FloatField()
    movie_critics_raing = models.FloatField()
    movie_url_image = models.CharField(max_length=1000)
    movie_url_trailer = models.CharField(max_length=1000)
    movie_country = models.CharField(
        max_length=100,
        choices=[
            ("KZ", "Kazakhstan"),
            ("RU", "Russia"),
            ("USA", "USA"),
            ("UK", "Unighted Kingdom"),
            ("China", "China")
        ]
    )
    movie_budjet = models.FloatField()
    movie_duration = models.TextField()
    movie_date = models.DateField('Date of Premiere')
    movie_findings = models.FloatField()
    #actors = models.
    #produccer
    movie_genres = models.ManyToManyField(Genre)
    #comments


class Person(models.Model):
    person_id = models.CharField(max_length=9999)
    person_name = models.CharField(max_length=100)
    person_url_image = models.CharField(max_length=1000)
    person_rating_av_from_films = models.FloatField()
    #person_roles_in_film


class Person_Movie(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)


class User(models.Model):
    user_id = models.CharField(max_length=9999)
    user_name = models.TextField()
    user_login = models.TextField()
    user_login = models.IntegerField()
    #comments
    #favarites
    #watch_later
    #ratings


class Rating(models.Model):
    rating_id = models.CharField(max_length=9999)
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating_number = models.IntegerField()


class Comment(models.Model):
    comment_id = models.CharField(max_length=9999)
    comment_description = models.TextField()
    comment_date = models.DateTimeField()
    #likes
    #dislikes
    #comment_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    #comment_user = models.ForeignKey(Movie, on_delete=models.CASCADE)
