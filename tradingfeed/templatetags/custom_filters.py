from django import template
from django.forms import BoundField

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name="add_class")
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter(name="disable_field")
def disable_field(field):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"disabled": "disabled"})
    return field
