from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

    def blog_count(self):
        return self.blog_set.count()


class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']



