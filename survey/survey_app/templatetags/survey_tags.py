from django import template

register = template.Library()


@register.filter(name="by_key")
def by_key(dictlike, key):
    return dictlike[key]
