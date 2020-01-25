from django.urls import path, re_path, include
from main.views import (
home, 
update,
faq,
detail, 
landing, 
detail_link,
home_decode, 
detail_file_decode, 
detail_paste_decode, 
detail_link_decode,
)

# ?: (2_0.W001) Your URL pattern '(?P<slug>[-\w]+)/' [name='detail2'] has a route that contains '(?P<', begins with a '^', or ends with a '$'. This was likely an oversight when migrating to django.urls.path().
# To prevent this error in Django 2.x upwards (even in Django 3.x), use re_path (using regular expression in path)
urlpatterns = [
		path(r'', landing, name="landing"),
		path(r'encode/', home, name="home"),
		re_path(r'^update/(?P<update_id>[-\w]+)$', update, name="update"),
		path(r'faq/', faq, name="faq"),
		path(r'encode/<int:id>/', detail, name='detail'),
		re_path(r'^encode/(?P<encode_id>[-\w.=+]+)$', detail_link, name='detail2'),
		path(r'decode/', home_decode, name="home_decode"),
		re_path(r'^decode/(?P<id>\d+)/(?P<unique_id>[-\w]+)$', detail_file_decode, name='detail3'),
		re_path(r'^decode/paste/(?P<unique_id_paste>[-\w]+)$', detail_paste_decode, name='detail4'),
		re_path(r'^decode/(?P<link_id>[-\w]+)/(?P<live_id>[-\w.=+]+)$', detail_link_decode, name='detail5'),	

		]
