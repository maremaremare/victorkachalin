import random
from django import template
register = template.Library()

@register.filter

def shuffle(arg):
    tmp = [i for i in arg]
    random.shuffle(tmp)
    return tmp