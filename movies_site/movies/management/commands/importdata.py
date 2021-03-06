import json
from django.core.management.base import BaseCommand
from django.db import transaction
from twisted.internet.abstract import _LogOwner

from movies.models import *

class Command(BaseCommand):
    help = 'Imports data from scrapers output'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        # transaction.set_autocommit(False)

        created = 0
        reviews = 0

        for file in options['file']:
            entries = []

            with open(file) as f:
                entries = json.load(f)

            for entry in entries:
                movie = Movie.objects.filter(title=entry['title'], year=entry['year']).first()
                is_imdb = entry['website'] == 'IMDb'

                if is_imdb and not movie:
                    movie = Movie()
                    movie.title = entry['title']
                    movie.year = entry['year']
                    movie.duration = entry['duration']
                    movie.description = entry['description']
                    movie.storyline = entry['storyline']
                    movie.cover = entry['cover']
                    movie.save()

                    for genre_name in entry['genres']:
                        genre, created = Genre.objects.get_or_create(name=genre_name)
                        movie.genres.add(genre)
                        if created:
                            print("Created genre", genre_name)

                    for name in entry['directors']:
                        director, created = Person.objects.get_or_create(first_name=name[0], last_name=name[1])
                        movie.directors.add(director)
                        if created:
                            print("Created director", name)

                    for name in entry['actors']:
                        actor, created = Person.objects.get_or_create(first_name=name[0], last_name=name[1])
                        movie.actors.add(actor)
                        if created:
                            print("Created actor", name)

                    created += 1
                    print("Created movie", movie)

                elif not is_imdb and not movie:
                    print("Unknown movie: {0} ({1})".format(entry['title'], entry['year']))
                    continue
                else:
                    print("Using movie", movie)

                site = ReviewsSite.objects.filter(name=entry['website']).first()

                if movie and site and entry['score'] and entry['num_reviews']:
                    review = MovieReview(movie=movie, site=site, score=entry['score'], users=entry['num_reviews'])
                    review.save()

                    reviews += 1
                    print("Created review", review)

            # transaction.commit()
            print("FINISHED. Created: {0}, Reviews: {1}, Processed: {2}".format(created, reviews, len(entries)))
