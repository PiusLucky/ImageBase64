import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from .formatChecker import ContentTypeRestrictedFileField
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from .utils import (
    generate_unique_id,
	generate_unique_id_field,
	generate_unique_id_file,
	generate_unique_id_link,
	update_unique_id,
)
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timezone


##########################################################################################
				# ENCODE SECTION BY LUCKY P. (JUST ANOTHER PROGRAMMER)
##########################################################################################


# Recall 1024 bytes = 1 kilobyte
# 1024 x 300 = 300 kilobyte
# 1048576 Bytes = 1MB
# Use www.gbmb.org and use bytes in binary. (perfect!)
class Image_Model(models.Model):
	image = ContentTypeRestrictedFileField(
	help_text=" @Upload image(PNG, Jpeg and GIF only) with size of 1MB or less",
	content_types=['image/jpeg','image/png', 'image/gif','image/webp'],
	max_upload_size= 1048576, blank=False, null=False, max_length=1000
	)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def get_absolute_url(self):
		return reverse("main:detail",
		args = [self.id
		])
	def imgs(self):
		return self.image
	def __str__(self):
	    return str(self.id)
		
	class Meta:
		# abstract = True #if the model Post is abstract,it cannot be registered with admin.
		ordering = ["-timestamp"]


class Link_Model(models.Model):
	url = models.URLField(blank=False, null=False, max_length=2000, help_text="https://www.google.com/example.jpg")
	unique_id_link = models.CharField(
	verbose_name=_('unique_link_encode'), max_length=28,
	default = generate_unique_id_link
	)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def get_absolute_url(self):
		encode_id = u"encoded_link_{0}".format(self.unique_id_link)
		return reverse("main:detail2",
		args = [encode_id
		])
	def __str__(self):
		# This will basically return the the objects ID(s) in cases like
		# print(Link_Model_Decode.objects.all()) --- when called in view.py
	    return str(self.url)
	class Meta:
		# abstract = True #if the model Post is abstract,it cannot be registered with admin.
		ordering = ["-timestamp"]


##########################################################################################
				# DECODE SECTION BY LUCKY P. (JUST ANOTHER PROGRAMMER)
##########################################################################################
# Recall 1MB = 1048576 bytes (in Binary)

class File_Model(models.Model):
	file_storage = FileSystemStorage(location=settings.FILE_ROOT)
	file_field = ContentTypeRestrictedFileField( storage=file_storage,
	help_text=" @Upload .txt and .html file of 2MB or Less.",
	content_types=['text/plain', 'text/html' ],
	max_upload_size= settings.DATA_UPLOAD_MAX_MEMORY_SIZE, blank=False, null=False,
	)
	unique_id = models.CharField(
	verbose_name=_('unique_id'), max_length=20,
	default = generate_unique_id_file
	)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	# REMOVING THESE LINES PREVENT FILE NOT FOUND/PERMISSION ERRORS
	# Lets delete files in the file_root
	# def delete(self, *args, **kwargs):
	# 	os.remove(os.path.join(settings.FILE_ROOT, self.file_field.name ))
	# 	super(File_Model,self).delete(*args,**kwargs)
	def get_absolute_url(self):
		return reverse("main:detail3",
		args = [self.id, self.unique_id
		])

	def __str__(self):
	    return str(self.file_field)
		
	class Meta:
		# abstract = True #if the model Post is abstract,it cannot be registered with admin.
		ordering = ["-timestamp"]

class Field_Model(models.Model):
	paste = models.TextField()
	unique_id_paste = models.CharField(
	verbose_name=_('unique_id'), max_length=29,
	default = generate_unique_id_field
	)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	@property
	def get_absolute_url_paste(self):
		return reverse("main:detail4",
		args = [self.unique_id_paste
		])
	def the_unique_id_paste(self):
		return self.unique_id_paste
	def __str__(self):
		# This will basically return the the objects ID(s) in cases like
		# print(Link_Model.objects.all()) --- when called in view.py
	    return str(self.paste)
	class Meta:
		# abstract = True #if the model Post is abstract,it cannot be registered with admin.
		ordering = ["-timestamp"]

class Link_Model_Decode(models.Model):
	url = models.URLField(blank=False, null=False, max_length=2000, help_text='<small><div align="left" >\
	 \
	<b><span style="color:#57b894">INFO:</span>&nbsp;https://www.google.com/example.txt or http://www.abc.com/example.html</b></span></div></small>')
	unique_id_link = models.CharField(
	verbose_name=_('unique_id'), max_length=28,
	default = generate_unique_id_link
	)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	def get_absolute_url(self):
		link_id = u"link_{0}".format(self.id) 
		live_id = u"live={0}".format(self.unique_id_link)
		return reverse("main:detail5",
		args = [link_id, live_id
		])
	def __str__(self):
		# This will basically return the the objects ID(s) in cases like
		# print(Link_Model_Decode.objects.all()) --- when called in view.py
	    return str(self.url)
	class Meta:
		# abstract = True #if the model Post is abstract,it cannot be registered with admin.
		ordering = ["-timestamp"]



##########################################################################################
				# UPDATE SECTION BY LUCKY P. (JUST ANOTHER PROGRAMMER)
##########################################################################################
# Recall 1MB = 1048576 bytes (in Binary)

class Update_Model(models.Model):
	top_update = models.TextField(
	verbose_name=_('topUpdate'), max_length=99999,
	)
	quote = models.TextField(
	verbose_name=_('Quote'), max_length= 10000,
	)
	bottom_update = models.TextField(
	verbose_name=_('bottomUpdate'), max_length=999999999,
	)
	added_feature = models.TextField(
	verbose_name=_('Features'), max_length= 9999999,
	)
	version_of_update =  models.CharField(
	verbose_name=_('version_of_update'), max_length= 9999999,
	)
	contributor = models.TextField(
	verbose_name=_('contributors'), max_length=99999999, default= "PIUS LUCKY"
	)
	authenticate = models.CharField(
	verbose_name=_('authenticate'), max_length=10,
	)
	update_id = models.CharField(
	verbose_name=_('update_id'), max_length=17,
	default = update_unique_id
	)
	updated = models.DateTimeField(default= datetime.now())
	def get_absolute_url(self):
		return reverse("main:update",
		args = [self.update_id
		])

	def __str__(self):
	    return str(self.update_id)
		
	class Meta:
		# abstract = True #if the model Post is abstract,it cannot be registered with admin.
		ordering = ["-updated"]
