from django import template

register = template.Library()


def tags(quote_tags):
    return [str(name) for name in quote_tags.all()]


def tags_exist(quote_tags):
    return bool(len(quote_tags.all()))


register.filter('tags', tags)
register.filter('tags_exist', tags_exist)
