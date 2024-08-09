from django import template

from goods.models import Categories

register = template.Library()


@register.simple_tag  # регистрация темплейта
def tag_categories():
    return Categories.objects.all()
