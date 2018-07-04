from django import forms
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': 'Comment content cannot be none.'})

    def clean(self):
        try:
            content_type = self.cleaned_data['content_type']
            object_id = self.cleaned_data['object_id']
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('Comment object does not exist')
        except KeyError:
            raise Http404('Page does not exist')

        return self.cleaned_data
