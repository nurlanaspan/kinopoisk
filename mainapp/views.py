from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import *
from django.shortcuts import render, get_object_or_404


def index(request):
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
            try:
                exit_performed = request.POST['exit']
                if exit_performed == 'yes':
                    print('exit was performed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    del request.session['user_id']
                return render(request, "mainapp/index.html", context)
            except:
                pass
            user = User.objects.get(pk=request.session['user_id'])
            context['user'] = user
            return render(request, "mainapp/index.html", context)
    except:
        pass

    if request.method == 'POST':
        try:
            # checking if login was perfomed
            try:
                login_performed = request.POST['login_performed']
                user_login = request.POST['user_login']
                user_password = request.POST['user_password']
                user = User.objects.get(user_login=user_login)
                if user and user_password == user.user_password:
                    request.session['user_id'] = user.id;
                    context['user'] = user
                    return render(request, "mainapp/index.html", context)
            except:
                pass
            user_name = request.POST['name']
            user_surname = request.POST['surname']
            user_login = request.POST['login']
            user_password = request.POST['password']
            user = User(user_name=user_name, user_surname=user_surname, user_login=user_login, user_password=user_password)
            user.save()
            request.session['user_id'] = user.id
            context['user'] = user
            return render(request, "mainapp/index.html", context)
            # return HttpResponseRedirect("mainapp/index.html", {'movies': movies, 'genres': genres, 'countries': countries, 'new_movies': new_movies}, 
            #     context_instance=RequestContext(request))
        except:
            registration_error='error'
            return render(request, "mainapp/index.html", context)

    return render(request, "mainapp/index.html", context)


def movie(request, movie_id):
    moviex = get_object_or_404(Movie, pk=movie_id)
    genres = moviex.movie_genres.all()
    context = {'movie': moviex, 'genres': genres, 'user': None}
    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
        print("user id barrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    except:
        pass
    print(context)
    return render(request, "mainapp/movie.html", context)


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

# Create your views here.
