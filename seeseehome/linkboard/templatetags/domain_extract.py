from django import template
from urlparse import urlparse

register = template.Library()

@register.filter
def domain_extract(url):
	parsed_uri = urlparse(url)
	domain = '{uri.netloc}'.format(uri=parsed_uri)

	return domain
