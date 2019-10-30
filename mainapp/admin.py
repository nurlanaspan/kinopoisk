from django.contrib import admin
from .models import Movie
from .models import Person
from .models import Genre
from .models import User
from .models import Person_Movie
from .models import Rating
from .models import Comment

# Register your models here.
admin.site.register(Person)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Person_Movie)
admin.site.register(Rating)
admin.site.register(Comment)
