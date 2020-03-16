from django.db.models import FileField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django import forms


class ContentTypeRestrictedFileField(FileField):
    def __init__(self, *args, **kwargs):
            self.content_types = kwargs.pop('content_types', [])
            self.max_upload_size = kwargs.pop("max_upload_size", [])

            super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            # Lucky's Comment
            # Initially for some reasons the "file._size" that once worked on Django 1.11
            # Failed to work on Django 3.0, I needed to remove the underscore.(it works!)
            if content_type in self.content_types:
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(_('@Please keep file-size under %s. Current file-size is %s') % (filesizeformat(self.max_upload_size), filesizeformat(file.size)))
            else:
                raise forms.ValidationError(_('@Filetype not supported.'))
        except AttributeError:
            pass

        return data
