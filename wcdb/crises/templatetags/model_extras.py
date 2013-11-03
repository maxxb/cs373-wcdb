from django import template

register = template.Library()

@register.filter
def get_model_name(links_list):
    return links_list[0].__class__.__name__