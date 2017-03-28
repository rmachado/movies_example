# -*- coding: utf-8 -*-
import re
from scrapy.exceptions import DropItem

class IMDbPipeline(object):
    """ Processes IMDb movies fields and create related items."""

    def process_item(self, item, spider):
        if item["website"] != "IMDb":
            return item

        item["title"] = item["title"].strip()
        item["description"] = item["description"].strip()
        item["storyline"] = item["storyline"].strip()
        item["duration"] = convert_duration_to_minutes(item["duration"].strip())

        if item["year"]:
            item["year"] = int(item["year"])
        else:
            raise DropItem("Missing year")

        if item["score"]:
            item["score"] = float(item["score"])

        if item["num_reviews"]:
            item["num_reviews"] = int(item["num_reviews"].replace(',', ''))

        # A little hack to get the full sized image from IMDb
        if item["cover"] and "@._V1_UX182_CR0,0,182,268_AL_" in item["cover"]:
            item["cover"] = item["cover"].replace("@._V1_UX182_CR0,0,182,268_AL_", "@._V1_SY1000_SX675_AL_")

        item["directors"] = [split_person_name(name) for name in item["directors"]]
        item["actors"] = [split_person_name(name) for name in item["actors"]]

        return item

class MetacriticPipeline(object):
    """ Processes Metacritic movies fields and create related items."""

    def process_item(self, item, spider):
        if item["website"] != "Metacritic":
            return item

        item["title"] = item["title"].strip()
        item["year"] = int(item["year"])
        item["score"] = float(item["score"]) / 10
        item["num_reviews"] = int(re.search(r"\d+", item["num_reviews"])[0])

        return item


class RottenTomatoesPipeline(object):
    """ Processes RottenTomatoes movies fields and create related items."""

    def process_item(self, item, spider):
        if item["website"] != "Rotten Tomatoes":
            return item

        item["title"] = item["title"].strip()
        item["year"] = int(item["year"])
        item["score"] = float(re.search(r"\d+", item["score"])[0]) / 10
        item["num_reviews"] = int(item["num_reviews"])

        return item


def convert_duration_to_minutes(text):
    """Converts a duration text in the form '1h 20min' to minutes."""
    minutes = 0

    match = re.search(r'(\d+)h', text)
    if match:
        minutes += int(match.group(1)) * 60

    match = re.search(r'(\d+)min', text)
    if match:
        minutes += int(match.group(1))

    return minutes

def split_person_name(full_name):
    """Very naive way to split first and last name."""
    space = full_name.find(' ')
    first = full_name[:space]
    last = full_name[space + 1:]
    return (first, last)