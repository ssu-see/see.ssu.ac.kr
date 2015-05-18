import hashlib
from seeseehome.settings.settings import BASE_DIR, STATIC_URL
from django import template
from os.path import join, exists

register = template.Library()

@register.filter
def linkboard_image(url):
	m = hashlib.md5()
	m.update(url)
	file_digest = m.hexdigest()

	path = join(BASE_DIR, 'static', 'link_img', file_digest + ".png")
	
	image_url = STATIC_URL + 'img/loading.gif'
	
	if exists(path):
		image_url = STATIC_URL + 'link_img' + '/' + file_digest + '.png'

	return image_url
