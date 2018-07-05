from django import forms
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': 'Comment content cannot be none.'})
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def clean(self):
        try:
            if self.cleaned_data['text'][:3] == '<p>':
                self.cleaned_data['text'] = self.cleaned_data['text'][3:-4]
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

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('Error on reply')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('Error on reply')
        return reply_comment_id

