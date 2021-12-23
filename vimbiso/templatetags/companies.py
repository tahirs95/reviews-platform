from django import template
from vimbiso.models import *
from django.db.models import Avg, Count

register = template.Library()

@register.simple_tag
def average(user):
    GetAvg = Reviews.objects.filter(company=user).aggregate(Avg('ratings')) or 0 
    avg = GetAvg['ratings__avg']
    return avg

@register.filter(name='times') 
def times(number):
    return range(int(number))

@register.simple_tag
def total_reviews(user):
    total = Reviews.objects.filter(company=user).count()
    return total