from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
from random import randint

from .models import *
from .forms import *


def index(request):
    context = dict(create_default_context())
    try:
        error = request.session['error']
        context['error'] = error
        del request.session['error']
    except:
        pass

    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
    except:
        pass
    stars = []
    for movie in context['movies']:
        stars.append(get_rating_in_stars_list(movie.movie_user_rating / 2)[0:5])
    item_list = zip(context['movies'], stars)
    context['item_list'] = item_list
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
               'user': None,
               'error': None}
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
        user_conform_password = request.POST['conform-password']

        if user_password != user_conform_password:
            request.session['error'] = "Пароль и подтверждение пароля не совпадают"
            return HttpResponseRedirect(reverse('mainapp:index'))

        try:
            userx = User.objects.get(user_login=user_login)
            request.session['error'] = "Имя пользователя уже занято"
            return HttpResponseRedirect(reverse('mainapp:index'))
        except:
            pass

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
        try:
            user = User.objects.get(user_login=user_login)
        except:
            request.session['error'] = "Неправильное имя пользователя"
            return HttpResponseRedirect(reverse('mainapp:index'))

        if user_password != user.user_password:
            request.session['error'] = "Неверный пароль"
            return HttpResponseRedirect(reverse('mainapp:index'))

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
    # genres = moviex.movie_genres.all()
    # countries = moviex.movie_country.all()
    # # people = Person.objects.filter()
    # genresx = Genre.objects.all()
    # countriesx = Country.objects.all()
    context = dict(create_default_context())

    producers_raw = PersonMovie.objects.filter(movie=moviex, role='Producer')
    actors_raw = PersonMovie.objects.filter(movie=moviex, role='Actor')

    producers = []
    for producer_raw in producers_raw:
        producers.append(Person.objects.get(pk=producer_raw.person.id))

    actors = []
    for actor_raw in actors_raw:
        actors.append(Person.objects.get(pk=actor_raw.person.id))

    print(producers)
    print(actors)

    comments = Comment.objects.filter(comment_movie=moviex)
    stars = get_rating_in_stars_list(moviex.movie_user_rating)

    context['movie'] = moviex
    context['comments'] = comments
    context['stars'] = stars
    context['favorite'] = None
    context['watchlater'] = None
    context['actors'] = actors
    context['producers'] = producers
    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user
    except:
        pass

    try:
        favorite = Favorite.objects.get(favorite_user=user, favorite_movie=moviex)
        context['favorite'] = '+'
    except:
        pass

    try:
        wl = WatchLater.objects.get(wl_user=user, wl_movie=moviex)
        context['watchlater'] = '+'
    except:
        pass

    return render(request, "mainapp/movie.html", context)


def delete_comment(request, movie_id):
    print('DELETE COMMENT')
    moviex = get_object_or_404(Movie, pk=movie_id)
    genres = moviex.movie_genres.all()
    countries = moviex.movie_country.all()
    comments = Comment.objects.filter(comment_movie=moviex)
    context = {'movie': moviex, 'genres': genres, 'countries': countries, 'comments': comments, 'user': None}
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
    # return render(request, "mainapp/movie.html", context)


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
        userx = comment.comment_liked_users.all().get(pk=user.id)
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
            if movie.movie_name.lower().count(searched_text) > 0 or movie.movie_desctiption.lower().count(
                    searched_text) > 0:
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
    return HttpResponseRedirect(reverse('mainapp:movie', args=(moviex.id,)))


def user(request, userx_id):
    genres = Genre.objects.all()
    countries = Country.objects.all()

    userx = get_object_or_404(User, pk=userx_id)
    reports = Report.objects.filter(report_to_user=userx)

    context = {'userx': userx, 'user': None, 'genres': genres, 'countries': countries, 'reports': reports,
               'reported': None,
               'favorites': None, 'recommends': None, 'watchlater': None}

    user = None

    try:
        favorites = Favorite.objects.filter(favorite_user=userx)
        context['favorites'] = favorites
        recommends = get_recommended_movies(favorites)
        context['recommends'] = recommends
    except:
        pass

    try:
        wl = WatchLater.objects.filter(wl_user=userx)
        context['watchlater'] = wl
    except:
        pass

    try:
        user = User.objects.get(pk=request.session['user_id'])
        context['user'] = user

        for i in reports:
            if i.report_from_user == user:
                context['reported'] = True
    except:
        pass

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get("image")
            user.user_image = image
            user.save()
            return HttpResponseRedirect(reverse('mainapp:user', args=(userx.id,)))
    context['form'] = UploadImageForm()

    comments = Comment.objects.filter(comment_user=userx)
    counter = 0
    for comment in comments:
        counter += 1
        counter += len(comment.comment_liked_users.all()) * 2
    counter -= len(Report.objects.filter(report_to_user=userx)) * 2
    userx.user_score = counter
    userx.save()
    context['counter'] = counter
    return render(request, "mainapp/user.html", context)


def random_movie(request):
    movies = list(Movie.objects.all())
    moviex = movies[randint(0, len(movies) - 1)]
    print(moviex)
    return HttpResponseRedirect(reverse('mainapp:movie', args=(moviex.id,)))


def report_user(request):
    try:
        userx_id = request.GET['user_id']
        userx = get_object_or_404(User, pk=userx_id)
    except:
        return HttpResponse("Error")

    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    report = Report(report_from_user=user, report_to_user=userx)
    report.save()

    return HttpResponse("It's ok!")


def add_to_favorite(request):
    try:
        moviex_id = request.GET['movie_id']
        moviex = get_object_or_404(Movie, pk=moviex_id)
    except:
        return HttpResponse("Error")

    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        return HttpResponse("Error")

    favorite = Favorite(favorite_user=user, favorite_movie=moviex)
    favorite.save()

    return HttpResponse("It's ok!")


def add_to_wl(request):
    try:
        moviex_id = request.GET['movie_id']
        moviex = get_object_or_404(Movie, pk=moviex_id)
    except:
        return HttpResponse("Error")

    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        return HttpResponse("Error")

    wl = WatchLater(wl_user=user, wl_movie=moviex)
    wl.save()

    return HttpResponse("It's ok!")


def delete_from_wl(request):
    try:
        moviex_id = request.GET['movie_id']
        moviex = get_object_or_404(Movie, pk=moviex_id)
    except:
        return HttpResponse("Error")

    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        return HttpResponse("Error")

    try:
        wl = WatchLater.objects.get(wl_user=user, wl_movie=moviex)
        wl.delete()
        return HttpResponse("It's okay")
    except:
        return HttpResponse("Error")


def ban_user(request, userx_id):
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
    return HttpResponseRedirect(reverse('mainapp:user', args=(userx_id,)))
    # return render(request, "mainapp/user.html", context)


def rate_movie(request, movie_id):
    moviex = get_object_or_404(Movie, pk=movie_id)
    try:
        ratings = Rating.objects.filter(rating_movie=moviex)
        userx = User.objects.get(pk=request.session['user_id'])
        for i in ratings:
            if i.rating_user == userx:
                return HttpResponseRedirect(reverse('mainapp:movie', args=(movie_id,)))
        rating_number = int(request.POST['new_rating'])
        new_rating = Rating(rating_user=userx, rating_movie=moviex, rating_number=rating_number)
        new_rating.save()
        sum_of_rating = moviex.movie_user_rating * len(ratings) + rating_number
        moviex.movie_user_rating = sum_of_rating / (len(ratings) + 1)
        moviex.save()
    except:
        pass
    return HttpResponseRedirect(reverse('mainapp:movie', args=(movie_id,)))


def movies_by_genre(request, genre_id):
    context = dict(create_default_context())
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    genre = Genre.objects.get(pk=genre_id)
    found_movies = Movie.objects.filter(movie_genres=genre)
    context['found_movies'] = found_movies
    context['user'] = user
    return render(request, "mainapp/search.html", context)


def movies_by_country(request, country_id):
    context = dict(create_default_context())
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    country = Country.objects.get(pk=country_id)
    found_movies = Movie.objects.filter(movie_country=country)
    context['found_movies'] = found_movies
    context['user'] = user
    return render(request, "mainapp/search.html", context)


def movies_by_category(request, category_id):
    context = dict(create_default_context())
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    category = Category.objects.get(pk=category_id)
    found_movies = Movie.objects.filter(movie_categories=category)
    context['found_movies'] = found_movies
    context['user'] = user
    return render(request, "mainapp/search.html", context)


def movies_by_person(request, person_id):
    context = dict(create_default_context())
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    persons = Person.objects.get(pk=person_id)
    found_movies = Movie.objects.filter(movie_persons=persons)
    context['found_movies'] = found_movies
    context['user'] = user
    return render(request, "mainapp/search.html", context)


def add_new_movie(request):
    form = CreateMovieForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, "mainapp/add_movie.html", {'form': form})
    context = dict(create_default_context())
    persons = Person.objects.all()
    context['persons'] = persons
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    context['user'] = user
    context['form'] = form
    return render(request, "mainapp/add_movie.html", context)


def add_new_category(request):
    form = CreateCategoryForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'mainapp/add_category.html', {'form': form})
    context = dict(create_default_context())
    persons = Person.objects.all()
    context['persons'] = persons
    user = None
    try:
        user = User.objects.get(pk=request.session['user_id'])
    except:
        pass
    context['user'] = user
    context['form'] = form
    return render(request, 'mainapp/add_category.html', context)


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


def get_recommended_movies(favorites):
    genres = {}
    for f in favorites:
        f_m = f.favorite_movie
        for g in f_m.movie_genres.all():

            if g in genres:
                genres[g] += 1
            else:
                genres[g] = 1

    movies = Movie.objects.all()
    list_movies = []
    list_rating = []
    for m in movies:
        m_rate = 0
        b = True
        for f in favorites:
            if m == f.favorite_movie:
                b = False

        if not b:
            continue

        for g in m.movie_genres.all():
            if g in genres:
                m_rate += genres[g]
        if len(list_movies) < 5:
            list_movies.append(m)
            list_rating.append(m_rate)
            for i in range(len(list_movies)):
                for j in range(i):
                    if list_rating[i] > list_rating[j] or list_rating[i] == list_rating[j] and list_movies[
                        i].movie_user_rating > list_movies[j].movie_user_rating:
                        list_rating[i], list_rating[j] = list_rating[j], list_rating[i]
                        list_movies[i], list_movies[j] = list_movies[j], list_movies[i]
        elif m_rate > list_rating[4]:
            list_rating[4] = m_rate
            list_movies[4] = m
            for i in range(len(list_movies)):
                for j in range(i):
                    if list_rating[i] > list_rating[j]:
                        list_rating[i], list_rating[j] = list_rating[j], list_rating[i]
                        list_movies[i], list_movies[j] = list_movies[j], list_movies[i]

    return list_movies


def create_default_context():
    movies = Movie.objects.order_by('movie_main_rating')
    genres = Genre.objects.all()
    countries = Country.objects.all()
    categories = Category.objects.all()
    new_movies = Movie.objects.order_by('movie_date')[:2]
    movies_category_1 = Movie.objects.filter(movie_categories=categories[0])
    context = {'movies': movies,
               'genres': genres,
               'countries': countries,
               'new_movies': new_movies,
               'categories': categories,
               'movies_category_1': movies_category_1,
               'user': None,
               'error': None}
    return context
