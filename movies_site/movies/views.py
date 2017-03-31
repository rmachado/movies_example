from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum, Avg
from django.http import Http404
from django.shortcuts import render

from movies.models import Movie


def movies_list(request):
    movie_set = Movie.objects.all()

    search = request.GET.get('search')
    search_param = ''
    if search:
        for term in search.split():
            movie_set = movie_set.filter(
                Q(title__contains=term) | Q(genres__name__contains=term) |
                Q(description__contains=term) | Q(actors__first_name__contains=term) |
                Q(actors__last_name__contains=term) | Q(directors__first_name__contains=term) |
                Q(directors__last_name__contains=term)
            ).distinct()
        search_param = "search={0}&".format(search.replace(' ', '+'))
    else:
        search = ''

    movie_set = movie_set\
        .annotate(score=Avg('reviews__score'))\
        .annotate(num_reviews=Sum('reviews__users'))\
        .order_by('-score')

    paginator = Paginator(movie_set, 30)

    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    page_range = range(max(1, movies.number - 5), min(movies.number + 5, movies.paginator.num_pages) + 1)
    return render(request, 'movies/list.html', dict(movies=movies, page_range=page_range,
                                                    search=search, search_param=search_param))

def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")

    reviews = movie.reviews.all()
    score = sum([review.score for review in reviews]) / len(reviews)

    if score >= 7:
        score_class = 'green'
    elif score >= 5:
        score_class = 'orange'
    else:
        score_class = 'red'

    return render(request, 'movies/detail.html', dict(movie=movie, reviews=reviews, score=score, score_class=score_class))