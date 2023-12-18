from django import template
from django.utils.itercompat import is_iterable

register = template.Library()


@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    query_dict = context["request"].GET
    query_dict = query_dict.copy()

    for key, value in kwargs.items():
        if value is not None:
            if key in query_dict:
                del query_dict[key]
        elif is_iterable(value) and not isinstance(value, str):
            query_dict.setlist(key, value)
        else:
            query_dict[key] = value
    if not query_dict:
        return ""
    query_string = query_dict.urlencode()
    return f"?{query_string}"
