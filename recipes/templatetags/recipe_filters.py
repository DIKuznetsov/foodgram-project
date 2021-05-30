from django import template

register = template.Library()


@register.simple_tag
def page_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name,
                                      querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


@register.simple_tag
def recipe_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    tag = '{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        if querystring.count(tag) >= 1:
            querystring.remove(tag)
            filtered_querystring = filter(lambda p: p.split('=')[1] != value,
                                          querystring)
            encoded_querystring = '&'.join(filtered_querystring)
            url = '?{}'.format(encoded_querystring)
            return url

        filtered_querystring = filter(lambda p: p.split('=')[1] != value,
                                      querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url
