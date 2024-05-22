from django import template

register = template.Library()

@register.filter(name='range_filter')
def range_filter(start, end):
    return range(start, end)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)