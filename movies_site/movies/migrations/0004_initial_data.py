# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def forwards_func(apps, schema_editor):
    ReviewsSite = apps.get_model("movies", "ReviewsSite")
    db_alias = schema_editor.connection.alias
    ReviewsSite.objects.using(db_alias).bulk_create([
        ReviewsSite(name="IMDb", url="http://www.imdb.com"),
        ReviewsSite(name="Metacritic", url="http://www.metacritic.com"),
        ReviewsSite(name="Rotten Tomatoes", url="https://www.rottentomatoes.com")
    ])

def reverse_func(apps, schema_editor):
    ReviewsSite = apps.get_model("movies", "ReviewsSite")
    db_alias = schema_editor.connection.alias
    ReviewsSite.objects.using(db_alias).filter(name="IMDb").delete()
    ReviewsSite.objects.using(db_alias).filter(name="Metacritic").delete()
    ReviewsSite.objects.using(db_alias).filter(name="Rotten Tomatoes").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20170316_0342'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]