#forms.py
import re

from django import forms
from .models import Image_Model, Link_Model, File_Model, Field_Model, Link_Model_Decode, Contact_Me_Model
from .models import Image_Model, Link_Model, File_Model, Field_Model, Link_Model_Decode
from .models import Image_Model, Link_Model, File_Model, Field_Model, Link_Model_Decode, Contact_Me_Model





class UploadForm(forms.ModelForm):
    class Meta:
        model = Image_Model
        fields = (
            "image",
        )
class LinkUpload(forms.ModelForm):
    class Meta:
        model = Link_Model
        fields = (
            "url",
        )

class LinkDecodeForm(forms.ModelForm):
    class Meta:
        model = Link_Model_Decode
        fields = (
            "url",
        )

 

class Contact_Me_Form(forms.ModelForm):
    class Meta:
        model = Contact_Me_Model
        fields = (
            "name",
            "email",
            "whatsapp_contact",
            "query",
            "ticket_id",
            "seven_digit_auth_code",
            "seven_digit_auth_code_enter",
            "updated",
        )


class FieldForm(forms.ModelForm):
    paste = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'data:image/png;base64,iVr....'}), required=True, label="", help_text='<small><div align="left" >\
	 \
	<b><span style="color:#57b894">INFO:</span>&nbsp;Pasting in large chunk of base64 string takes 10 seconds or less</b></span></div></small>')
    class Meta:
        model = Field_Model
        fields = (
            "paste",
        )

class FileForm(forms.ModelForm):
    class Meta:
        model = File_Model
        fields = (
            "file_field",
        )