from django.contrib import admin
from .models import Image_Model, Link_Model, File_Model, Field_Model, Link_Model_Decode, Update_Model, Faq_Model

class Image_ModelAdmin(admin.ModelAdmin):
	list_display = ["id","timestamp"]
	list_display_links = ["id"]
	list_filter = ["id","timestamp"]
	class Meta:
		model = Image_Model
admin.site.register(Image_Model, Image_ModelAdmin)



class Link_ModelAdmin(admin.ModelAdmin):
	list_display = ["url","timestamp"]
	list_display_links = ["url"]
	list_filter = ["url","timestamp"]
	class Meta:
		model = Link_Model
admin.site.register(Link_Model, Link_ModelAdmin)


class File_ModelAdmin(admin.ModelAdmin):
	list_display = ["file_field","timestamp"]
	list_display_links = ["file_field"]
	list_filter = ["file_field","timestamp"]
	class Meta:
		model = File_Model
admin.site.register(File_Model, File_ModelAdmin)


class Field_ModelAdmin(admin.ModelAdmin):
	list_display = ["paste","timestamp"]
	list_display_links = ["paste"]
	list_filter = ["paste","timestamp"]
	class Meta:
		model = Field_Model
admin.site.register(Field_Model, Field_ModelAdmin)


class Link_Model_DecodeAdmin(admin.ModelAdmin):
	list_display = ["url","timestamp"]
	list_display_links = ["url"]
	list_filter = ["url","timestamp"]
	class Meta:
		model = Link_Model_Decode
admin.site.register(Link_Model_Decode, Link_Model_DecodeAdmin)


class Update_ModelAdmin(admin.ModelAdmin):
	list_display = ["update_id","version_of_update","updated"]
	list_display_links = ["update_id"]
	list_filter = ["update_id"]
	class Meta:
		exclude = ("updated",)
		model = Update_Model
admin.site.register(Update_Model, Update_ModelAdmin)


class Faq_ModelAdmin(admin.ModelAdmin):
	list_display = ["updated","Q1"]
	list_display_links = ["updated"]
	list_filter = ["Q1"]
	class Meta:
		model = Faq_Model
admin.site.register(Faq_Model, Faq_ModelAdmin)