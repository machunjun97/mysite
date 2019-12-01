from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Comment


def update_comment(request):

    referer = request.META.get('HTTP_REFERER', reverse('home'))

    try:  # 判断输入是否有错误
        user = request.user
        text = request.POST.get('text', '').strip()
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_object = model_class.objects.get(pk=object_id)
    except Exception :
        return render(request, 'error.html', {'massage': '评论对象不存在', 'redirct_to': referer})

    comment = Comment()  # 写入对象
    comment.user = user
    comment.text = text
    comment.content_object = model_object
    comment.save()

    if text == '':
        return render(request, 'error.html', {'message', "评论内容为空！"})

    return redirect(referer)


