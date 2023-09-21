from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_shareable_link(context, link):
    """Creates a full link so you can share it on external sites."""
    request = context.get("request")
    return request.build_absolute_uri(link)
