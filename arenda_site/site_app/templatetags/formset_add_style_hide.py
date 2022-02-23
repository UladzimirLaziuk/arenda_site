from django import template

register = template.Library()

@register.filter
def add_attr_style_non_display(iter_forms):
    iter_forms = iter_forms
    return iter_forms