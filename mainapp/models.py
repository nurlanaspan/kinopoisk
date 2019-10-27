from django.db import models

# Create your models here.
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
    #genres
    #comments
