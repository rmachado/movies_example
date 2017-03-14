from django.contrib import admin
from movies.models import *

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(ReviewsSite)
admin.site.register(MovieReview)