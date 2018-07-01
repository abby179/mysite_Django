from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ckeditor.fields import RichTextField
from read_count.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

    def blog_count(self):
        return self.blog_set.count()


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']



