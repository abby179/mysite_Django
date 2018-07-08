from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist

from .models import LikeCount, LikeRecord


def success_response(liked_num):
    data = {'status': 'SUCCESS', 'liked_num': liked_num}
    return JsonResponse(data)


def error_response(code, message):
    data = {'status': 'ERROR', 'code': code, 'message': message}
    return JsonResponse(data)


@login_required
def update_like(request):
    user = request.user
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_object = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_response(401, 'Object does not exist')

    if request.GET.get('is_liked') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return success_response(like_count.liked_num)
        else:
            return error_response(402, 'You already liked')
    else:
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created & like_count.liked_num != 0:
                like_count.liked_num -= 1
                like_count.save()
                return success_response(like_count.liked_num)
            else:
                return error_response(404, 'Data error')
        else:
            return error_response(403, 'You did not liked')


