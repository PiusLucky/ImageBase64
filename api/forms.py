from rest_framework import serializers

#forms.py
import re

from django import forms
from main.models import Image_Model


# class UploadFormSerialized(serializers.ModelSerializer):
# 	image = serializers.ImageField(
# 	help_text=" @Upload image(PNG, Jpeg and GIF only) with size of 1MB or less",
# 	content_types=['image/jpeg','image/png', 'image/gif','image/webp'],
# 	max_upload_size= 1048576, blank=False, null=False, max_length=1000
# 	)
# 	timestamp = serializers.DateTimeField(auto_now=False, auto_now_add=True)

# 	def get_absolute_url(self):
# 		return reverse("main:detail",
# 		args = [self.id
# 		])
# 	def imgs(self):
# 		return self.image
# 	def __str__(self):
# 	    return str(self.id)
		
# 	class Meta:
# 		ordering = ["-timestamp"]



class UploadFormSerialized(serializers.Serializer):
	image = serializers.ImageField(max_length=9000, allow_empty_file=False )
	class Meta:
	    model = Image_Model
	    fields = (
	        "image",
	    )