"""
Run in folder quotes with the command:
py -m utils.migrate
"""

from utils.models import Quotes  # noqa

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from quoteapp.models import Tag, Author, Quote  # noqa


from mongoengine import connect

from configparser import ConfigParser

config = ConfigParser()
config.read("mongo.ini")

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
    ssl=True,
)

if __name__ == "__main__":
    quotes_mongo = Quotes.objects()

    tags = set()
    authors = list()
    quotes = list()

    for quote in quotes_mongo:

        for tag in quote.tags:
            tags.add(tag)

        new_author = {
            "fullname": quote.author.fullname,
            "born_date": quote.author.born_date,
            "born_location": quote.author.born_location,
            "description": quote.author.description,
        }
        if not (new_author in authors):
            authors.append(new_author)

        new_quote = {
            "quote": quote.quote,
            "author": quote.author.fullname,
            "tags": quote.tags,
        }
        quotes.append(new_quote)

    for author in authors:
        Author.objects.get_or_create(
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"],
        )

    for tag in tags:
        Tag.objects.get_or_create(name=tag)

    for quote in quotes:
        exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))
        if not exist_quote:
            author_in_db = Author.objects.get(fullname=quote["author"])
            new_quote = Quote.objects.create(quote=quote["quote"], author=author_in_db)
            for tag in quote["tags"]:
                new_tag = Tag.objects.get(name=tag)
                new_quote.tags.add(new_tag)
