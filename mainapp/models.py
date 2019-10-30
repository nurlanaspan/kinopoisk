from django.db import models

# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name


class Person(models.Model):
    person_name = models.CharField(max_length=100)
    person_url_image = models.CharField(max_length=1000)
    person_rating_av_from_films = models.FloatField()
    #person_roles_in_film


class User(models.Model):
    user_name = models.TextField()
    user_login = models.TextField()
    user_login = models.IntegerField()
    #comments
    #favarites
    #watch_later
    #ratings


class Movie(models.Model):
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
    movie_persons = models.ManyToManyField(Person, through="Person_Movie")
    movie_rated_users = models.ManyToManyField(User, through="Rating")
    movie_commented_users = models.ManyToManyField(User, through="Comment", related_name="Comments")
    movie_genres = models.ManyToManyField(Genre)


class Person_Movie(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)


class Rating(models.Model):
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating_number = models.IntegerField()


class Comment(models.Model):
    comment_description = models.TextField()
    comment_date = models.DateTimeField()
    #likes
    #dislikes
    comment_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
