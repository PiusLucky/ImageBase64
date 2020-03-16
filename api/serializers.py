#api/serializers.py
from rest_framework import serializers
from main.models import Link_Model, Field_Model
		
class LinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Link_Model
		fields = ('id', 'url', 'unique_id_link', 'timestamp')
		read_only_fields = ('unique_id_link',)

class LinkDecodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Field_Model
		fields = ('id', 'paste', 'unique_id_paste', 'timestamp')
		read_only_fields = ('unique_id_paste',)