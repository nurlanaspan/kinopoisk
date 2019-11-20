from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime

from .models import *


def index(request):
    movies = Movie.objects.order_by('movie_main_rating')
    genres = Genre.objects.all()
    countries = Country.objects.all()
    categories = Category.objects.all()
    first_category = Category.objects.all()[0]
    print(categories)
    new_movies = Movie.objects.order_by('movie_date')[:2]
    movies_category_1 = Movie.objects.filter(movie_categories=categories[0])
    context = {'movies': movies,
               'genres': genres,
               'countries': countries,
               'new_movies': new_movies,
               'categories': categories,
               'movies_category_1': movies_category_1,
               'user': None}
    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
    except:
        pass
    return render(request, "mainapp/index.html", context)


def registration(request):
    movies = Movie.objects.order_by('movie_main_rating')
    genres = Genre.objects.all()
    countries = Country.objects.all()
    new_movies = Movie.objects.order_by('movie_date')[:2]
    context = {'movies': movies,
               'genres': genres,
               'countries': countries,
               'new_movies': new_movies,
               'user': None}
    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
        return render(request, "mainapp/index.html", context)
    except:
        pass
    try:
        user_name = request.POST['name']
        user_surname = request.POST['surname']
        user_login = request.POST['login']
        user_password = request.POST['password']
        user = User(user_name=user_name, user_surname=user_surname, user_login=user_login, user_password=user_password)
        user.save()
        request.session['user_id'] = user.id
        context['user'] = user
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:index'))


def authentication(request):
    movies = Movie.objects.order_by('movie_main_rating')
    genres = Genre.objects.all()
    countries = Country.objects.all()
    new_movies = Movie.objects.order_by('movie_date')[:2]
    context = {'movies': movies,
               'genres': genres,
               'countries': countries,
               'new_movies': new_movies,
               'user': None}
    try:
        user_login = request.POST['user_login']
        user_password = request.POST['user_password']
        user = User.objects.get(user_login=user_login)
        if user and user_password == user.user_password:
            request.session['user_id'] = user.id
            context['user'] = user
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:index'))


def exit_from_account(request):
    movies = Movie.objects.order_by('movie_main_rating')
    genres = Genre.objects.all()
    countries = Country.objects.all()
    new_movies = Movie.objects.order_by('movie_date')[:2]
    context = {'movies': movies,
               'genres': genres,
               'countries': countries,
               'new_movies': new_movies,
               'user': None}
    try:
        if request.session['user_id']:
            del request.session['user_id']
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:index'))


def movie(request, movie_id):
    moviex = get_object_or_404(Movie, pk=movie_id)
    genres = moviex.movie_genres.all()
    countries = moviex.movie_country.all()
    comments = Comment.objects.filter(comment_movie=moviex)
    stars = get_rating_in_stars_list(moviex.movie_user_rating)
    context = {'movie': moviex, 'genres': genres, 'countries': countries, 'comments': comments,
               'user': None, 'stars': stars}
    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
    except:
        pass
    return render(request, "mainapp/movie.html", context)


def delete_comment(request, movie_id):
    print('DELETE COMMENT')
    moviex = get_object_or_404(Movie, pk=movie_id)
    genres = moviex.movie_genres.all()
    countries = moviex.movie_country.all()
    comments = Comment.objects.filter(comment_movie=moviex)
    context = {'movie': moviex, 'genres': genres, 'countries': countries, 'comments': comments,'user': None}
    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
        print("user id barrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    except:
        pass

    try:
        comment_id = request.POST['comment_id']
        Comment.objects.get(pk=comment_id).delete()
    except:
        pass

    return HttpResponseRedirect(reverse('mainapp:movie', args=(movie_id,)))
    #return render(request, "mainapp/movie.html", context)


def like_comment(request):
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass

    try:
        comment_id = request.GET['comment_id']
        comment = Comment.objects.get(pk=comment_id)

        print("Its ok!!!!!!!!!")
        comment.comment_liked_users.add(user)
        comment.save()
        print(comment)
        return HttpResponse("Success!")
    except:
        return HttpResponse("Error!")

def delete_like_comment(request):
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass

    try:
        comment_id = request.GET['comment_id']
        comment = Comment.objects.get(pk=comment_id)

        print("Its ok!!!!!!!!!")
        userx = comment.comment_liked_users.all().get(pk = user.id)
        print(userx)
        comment.comment_liked_users.remove(user)
        comment.save()
        print(comment)
        return HttpResponse("Success!")
    except:
        return HttpResponse("Error!")

def search(request):
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
        print("user id barrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    except:
        pass
    try:
        searched_text = request.POST['searched_text'].lower()
        found_movies = []
        movies = Movie.objects.all()
        for movie in movies:
            if movie.movie_name.lower().count(searched_text) > 0 or movie.movie_desctiption.lower().count(searched_text) > 0:
                found_movies.append(movie)
        return render(request, "mainapp/search.html", {'found_movies': found_movies, 'user': user})
    except:
        pass


def post_comment(request):
    user = None
    moviex = get_object_or_404(Movie, pk=request.POST['movie_id'])
    genres = moviex.movie_genres.all()
    context = {'movie': moviex, 'genres': genres, 'user': None}
    try:
        user = User.objects.get(pk=request.session['user_id'])
        moviex = Movie.objects.get(pk=request.POST['movie_id'])
        if user:
            comment_text = request.POST['comment_text']
            comment = Comment(comment_description=comment_text, comment_date=datetime.datetime.now(),
                              comment_movie=moviex, comment_user=user)
            comment.save()
        context['user'] = user
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:movie', args=(moviex.id, )))


def user(request, userx_id):
    userx = get_object_or_404(User, pk=userx_id)
    reports = Report.objects.filter(report_to_user = userx)
    context = {'userx': userx, 'user': None, 'reports': reports}

    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
        print("user id barrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    except:
        pass
    return render(request, "mainapp/user.html", context)


def ban_user(request, userx_id):
    print('sdsddskdkgmlskdjflksdljfklsjdfjsd')
    context = {'user': None}

    try:
        userx = get_object_or_404(User, pk=request.POST['banuser'])
        context['userx'] = userx
        userx.user_status = 'banned'
        userx.save()
    except:
        pass

    try:
        userx = get_object_or_404(User, pk=request.POST['notbanuser'])
        context['userx'] = userx
        userx.user_status = 'not banned'
        userx.save()
    except:
        pass

    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
        print("user id barrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:user', args=(userx_id, )))
    #return render(request, "mainapp/user.html", context)


def rate_movie(request, movie_id):
    moviex = get_object_or_404(Movie, pk=movie_id)
    try:
        ratings = Rating.objects.filter(rating_movie=moviex)
        userx = User.objects.get(pk=request.session['user_id'])
        for i in ratings:
            if i.rating_user == userx:
                return HttpResponseRedirect(reverse('mainapp:movie', args=(movie_id, )))
        rating_number = int(request.POST['new_rating'])
        new_rating = Rating(rating_user=userx, rating_movie=moviex, rating_number=rating_number)
        new_rating.save()
        sum_of_rating = moviex.movie_user_rating * len(ratings) + rating_number
        moviex.movie_user_rating = sum_of_rating / (len(ratings) + 1)
        moviex.save()
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:movie', args=(movie_id, )))


def get_rating_in_stars_list(rating):
    counter = int(rating)
    stars = [2 for i in range(counter)]
    if counter < rating:
        stars.append(1 if rating >= float(counter) + 0.5 else 0)
    if counter < rating:
        counter += 1
    for i in range(10 - counter):
        stars.append(0)
    return stars

# Create your views here.
