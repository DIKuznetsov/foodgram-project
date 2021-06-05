from django import template
from recipes.models import Tag


register = template.Library()


@register.filter
def get_tags(request):
    return request.getlist("tag")


@register.filter
def tag_link(request, tag):
    request_copy = request.GET.copy()
    request_copy["page"] = "1"
    tags = request_copy.getlist("tag")
    if tag.title in tags:
        tags.remove(tag.title)
        request_copy.setlist("tag", tags)
    else:
        request_copy.appendlist("tag", tag.title)
    return request_copy.urlencode()


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def pagination(request, page):
    request_copy = request.GET.copy()
    request_copy["page"] = page
    return request_copy.urlencode()


@register.filter
def change_word_ending(n):
    ending = ''
    if n <= 0:
        return 'Это все рецепты'
    if ((n == 0) or (5 <= n <= 20) or ((21 <= n) and (
            (5 <= (n % 10) <= 9) or (n % 10 == 0) or (
            11 <= (n % 100) <= 14)))):
        ending = 'ов'
    elif (n == 1) or ((21 <= n) and (n % 10 == 1) and (n % 100 != 11)):
        ending = ''
    elif 2 <= n <= 4 or ((21 <= n) and (2 <= (n % 10) <= 4)):
        ending = 'а'
    return f'Еще {n} рецепт{ending}'
