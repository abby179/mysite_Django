from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from .models import Comment
from .forms import CommentForm


@login_required
def update_comment(request):
    comment_form = CommentForm(request.POST)
    data = {}

    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp()
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        data['text'] = comment.text
        if parent:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root else None

    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
