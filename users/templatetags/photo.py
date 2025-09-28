from django import template

register = template.Library()


@register.filter()
def photo_tag(path):
    if path:
        return f"/media/{path}"
    return "#"
