from django.db import models
import uuid

def movie_cover_path(instance, filename):
    # Calculates the file path where to upload a movie's cover
    extension = filename.split('.')[-1]
    return "covers/{0}.{1}".format(uuid.uuid4(), extension)


class Genre(models.Model):
    # A Movie genre
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Person(models.Model):
    # General class for representing actors, directors, etc. May be an abstract model in the future
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Movie(models.Model) :
    # Represents a Movie on the site
    title = models.CharField(max_length=100)
    year = models.IntegerField(help_text="Release year", null=True, blank=True)
    duration = models.IntegerField(help_text="Movie duration in minutes", null=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    storyline = models.TextField(blank=True)
    cover = models.ImageField(upload_to=movie_cover_path)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Person, related_name="acting_movies")
    directors = models.ManyToManyField(Person, related_name="directing_movies")

    class Meta:
        unique_together = ('title', 'year')

    def __str__(self):
        return "{0} ({1})".format(self.title, self.year)


class ReviewsSite(models.Model):
    # Represents a movie reviews website
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class MovieReview(models.Model):
    # The review of a movie on a reviews site
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
    site = models.ForeignKey(ReviewsSite, on_delete=models.CASCADE)
    score = models.FloatField(null=False, blank=False, help_text="A score between 0 and 100")
    users = models.IntegerField(help_text="The number of users which produced this review's score")

    def __str__(self):
        return "{0} ({1})".format(self.score, self.site.name)
