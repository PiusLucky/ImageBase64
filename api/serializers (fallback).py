#api/serializers.py
from rest_framework import serializers
from rest_framework.fields import FileField
from main.models import   (Image_Model,
					Link_Model,
					File_Model,
					Field_Model,
					Link_Model_Decode,
					)

from django.forms import ImageField
from django.utils.translation import gettext_lazy as _
from main.formatChecker import ContentTypeRestrictedFileField

class ImageFieldCustom(FileField):
    default_error_messages = {
        'invalid_image': _(
            'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'
        ),
    }

    def __init__(self, *args, **kwargs):
        self._ImageField = kwargs.pop('_ImageField', ImageField)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        # Image validation is a bit grungy, so we'll just outright
        # defer to Django's implementation so we don't need to
        # consider it, or treat PIL as a test dependency.
        file_object = super().to_internal_value(data)
        django_field = self._ImageField()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)



class MainSerializer(serializers.ModelSerializer):
	image = ImageFieldCustom(max_length=None, use_url=False, required=True)
	class Meta:
		model = Image_Model
		fields = ('id', 'image', 'timestamp')

class LinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Link_Model
		fields = ('id', 'url', 'unique_id_link', 'timestamp')

class FileSerializer(serializers.ModelSerializer):
	class Meta:
		model = File_Model
		fields = ('id', 'file_storage', 'file_field','unique_id', 'timestamp')

class FieldSerializer(serializers.ModelSerializer):
	class Meta:
		model = Field_Model
		fields = ('id', 'paste', 'unique_id_paste', 'timestamp')

class LinkDecodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Link_Model_Decode
		fields = ('id', 'url', 'unique_id_link', 'timestamp')

