from django import template
from ..models import University

register = template.Library()


# this is used for rankings of individual programs to take value from a template tag in for
# and extract the parent university for that program
# http://www.pfinn.net/custom-django-filter-tutorial.html
# https://stackoverflow.com/questions/1591712/how-to-use-nested-template-tags-with-arguments


@register.filter(name='get_parent_university')
def get_parent_university(value):
    return University.objects.filter(program__university_id=value).first().name
