from django.urls import path, re_path, include
from api.views import (
LinkEncodeView,
LinkAPIDetailView,
LinkDecodeView,
LinkDecodeDetailView,
)



urlpatterns = [
        path(r'link/encode/', LinkEncodeView.as_view(), name="api_link_encode"),
        re_path(r'link/encode/(?P<encode_id>[-\w.=+]+)/', LinkAPIDetailView.as_view(), name='api_link_detail'),
        path(r'link/decode/', LinkDecodeView.as_view(), name="api_link_decode"),
        re_path(r'link/decode/(?P<unique_id_paste>[-\w.=+]+)/', LinkDecodeDetailView.as_view(), name='api_decode_detail'),
		]


		