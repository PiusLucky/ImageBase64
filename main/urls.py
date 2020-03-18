from django.urls import path, re_path, include
from main.views import (
<<<<<<< HEAD
<<<<<<< HEAD
update,
faq,
detail,
my_contact,
post_contact_view, 
=======
home, 
update,
detail, 
landing, 
>>>>>>> 03e218cf9638771148b7fc638f13fc66fa822b6e
=======
home, 
update,
faq,
my_contact,
post_contact_view,
detail, 
landing, 
>>>>>>> eee8e180e0a87a6e3b46c614cdc8f61d3df6d0ff
detail_link,
home_decode, 
detail_file_decode, 
detail_paste_decode, 
detail_link_decode,
<<<<<<< HEAD
<<<<<<< HEAD
# Class Based Views
LandingView,
HomeView,
=======
>>>>>>> 03e218cf9638771148b7fc638f13fc66fa822b6e
=======
>>>>>>> eee8e180e0a87a6e3b46c614cdc8f61d3df6d0ff
)

# ?: (2_0.W001) Your URL pattern '(?P<slug>[-\w]+)/' [name='detail2'] has a route that contains '(?P<', begins with a '^', or ends with a '$'. This was likely an oversight when migrating to django.urls.path().
# To prevent this error in Django 2.x upwards (even in Django 3.x), use re_path (using regular expression in path)
urlpatterns = [
<<<<<<< HEAD
<<<<<<< HEAD
		# path(r'', landing, name="landing"),
		path(r'', LandingView.as_view(), name="landing"),
		path(r'encode/', HomeView.as_view(), name="home"),
=======
		path(r'', landing, name="landing"),
		path(r'encode/', home, name="home"),
>>>>>>> eee8e180e0a87a6e3b46c614cdc8f61d3df6d0ff
		re_path(r'^update/(?P<update_id>[-\w]+)$', update, name="update"),
		path(r'faq/', faq, name="faq"),
		path(r'contact/', my_contact, name="cnt"),
		path(r'post/contact/', post_contact_view, name="cnt_submit"),
		path(r'encode/<int:id>/', detail, name='detail'),
		re_path(r'^encode/(?P<encode_id>[-\w.=+]+)$', detail_link, name='detail2'),
<<<<<<< HEAD
=======
		path(r'', landing, name="landing"),
		path(r'encode/', home, name="home"),
		re_path(r'^update/(?P<update_id>[-\w]+)$', update, name="update"),
		path(r'encode/<int:id>/', detail, name='detail'),
		re_path(r'^(?P<slug>[-\w]+)/(?P<unique_id>[-\w]+)$', detail_link, name='detail2'),
>>>>>>> 03e218cf9638771148b7fc638f13fc66fa822b6e
=======
>>>>>>> eee8e180e0a87a6e3b46c614cdc8f61d3df6d0ff
		path(r'decode/', home_decode, name="home_decode"),
		re_path(r'^decode/(?P<id>\d+)/(?P<unique_id>[-\w]+)$', detail_file_decode, name='detail3'),
		re_path(r'^decode/paste/(?P<unique_id_paste>[-\w]+)$', detail_paste_decode, name='detail4'),
		re_path(r'^decode/(?P<link_id>[-\w]+)/(?P<live_id>[-\w.=+]+)$', detail_link_decode, name='detail5'),	

		]
