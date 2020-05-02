from django import template

register = template.Library()

@register.simple_tag
def remove_uderscore(text):
    return text.replace('_',' ')