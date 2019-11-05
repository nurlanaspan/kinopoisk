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

    return render(request, "mainapp/movie.html", {'movie': moviex})

# Create your views here.
