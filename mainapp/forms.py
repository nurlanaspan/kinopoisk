from django import forms
from .models import *


class UploadImageForm(forms.Form):
    image = forms.ImageField()


class CreateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'movie_name',
            'movie_desctiption',
            'movie_url_trailer',
            'movie_country',
            'movie_budjet',
            'movie_duration',
            'movie_date',
            'movie_findings',
            'movie_persons',
            'movie_genres',
            'movie_categories',
            'movie_image',
        ]


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'category_name',
            'category_order_by_parameter',
        ]
