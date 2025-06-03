from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(widget_bound_field, css_class: str):
    """
    Usage  →  {{ form.username|add_class:"form-control" }}
    """
    return widget_bound_field.as_widget(attrs={"class": css_class})
