from django.db import models


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_name_russian = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name


class Person(models.Model):
    person_name = models.CharField(max_length=100)
    person_url_image = models.CharField(max_length=1000)
    person_rating_av_from_films = models.FloatField()
    # person_roles_in_film


class User(models.Model):
    user_name = models.CharField(max_length=64)
    user_surname = models.CharField(max_length=64, default="UNKNOWN")
    user_login = models.CharField(max_length=64)
    user_password = models.CharField(max_length=64, default="qwe123ASD")
    user_url_image = models.CharField(max_length=1000, default='mainapp\images\defaultuser.png')
    user_role = models.CharField(max_length=32, default='user')
    user_status = models.CharField(max_length=16, default='not banned')
    user_image = models.ImageField(blank=True, null=True, default=None, upload_to="images/users")
    user_score = models.IntegerField(blank=True, null=True, default=0)


class Report(models.Model):
    report_from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")


class Category(models.Model):
    PARAMETERS = (
        ('movie_main_rating', 'movie_main_rating'),
        ('movie_critics_raing', 'movie_critics_raing'),
        ('movie_user_rating', 'movie_user_rating'),
        ('movie_date', 'movie_date')
    )
    category_name = models.CharField(max_length=100)
    category_order_by_parameter = models.CharField(max_length=32, choices=PARAMETERS, default='movie_main_rating')


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    movie_desctiption = models.TextField(default=0.0)
    movie_main_rating = models.FloatField(default=0.0)
    movie_user_rating = models.FloatField(default=0.0)
    movie_critics_raing = models.FloatField(default=0.0)
    movie_url_image = models.CharField(max_length=1000, blank=True, null=True, default=None)
    movie_url_trailer = models.CharField(max_length=1000)
    movie_country = models.ManyToManyField(Country)
    movie_budjet = models.FloatField()
    movie_duration = models.TextField()
    movie_date = models.DateField('Date of Premiere')
    movie_findings = models.FloatField()
    movie_persons = models.ManyToManyField(Person, through="PersonMovie")
    movie_rated_users = models.ManyToManyField(User, through="Rating")
    movie_commented_users = models.ManyToManyField(User, through="Comment", related_name="Comments")
    movie_genres = models.ManyToManyField(Genre)
    movie_categories = models.ManyToManyField(Category)
    movie_image = models.ImageField(blank=True, null=True, default=None, upload_to="images/movies")

    def __str__(self):
        return self.movie_name


class PersonMovie(models.Model):
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
    comment_liked_users = models.ManyToManyField(User)
    # dislikes
    comment_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")


class Favorite(models.Model):
    favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    favorite_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None)


class WatchLater(models.Model):
    wl_user = models.ForeignKey(User, on_delete=models.CASCADE)
    wl_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
