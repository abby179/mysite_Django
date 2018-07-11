from django import forms
from django.db.models import ObjectDoesNotExist

from ckeditor.widgets import CKEditorWidget
from .models import BlogType


def get_all_blog_types():
    blog_types = BlogType.objects.all()
    result = []
    for blog_type in blog_types:
        result.append((blog_type.type_name, blog_type.type_name))
    return result


class BlogForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    blog_type = forms.ChoiceField(choices=get_all_blog_types())
    content = forms.CharField(widget=CKEditorWidget(config_name='blog_ckeditor'),
                              error_messages={'required': 'Blog content cannot be none.'})

    def clean(self):
        if self.cleaned_data['content'][:3] == '<p>':
            self.cleaned_data['content'] = self.cleaned_data['content'][3:-4]

        try:
            self.cleaned_data['blog_type'] = BlogType.objects.get(type_name=self.cleaned_data['blog_type'])
        except ObjectDoesNotExist:
            raise forms.ValidationError('Blog type does not exist')

        return self.cleaned_data
