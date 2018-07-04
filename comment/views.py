from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Comment
from .forms import CommentForm


@login_required
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
