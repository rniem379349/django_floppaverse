from django.template import Library

from shared.mixins.helper import get_time_elapsed_humanized

register = Library()


@register.simple_tag(takes_context=True)
def add_get_param(context, param, val):
    request = context.get("request")
    params = request.GET.copy()
    params[param] = val
    return "?%s" % params.urlencode()


@register.filter(name="get_class")
def get_class(value):
    return value.__class__.__name__


@register.filter(name="get_time_elapsed_human")
def get_time_elapsed_human(value):
    return get_time_elapsed_humanized(value)
