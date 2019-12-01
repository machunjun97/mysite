from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # 评论文章

    text = models.TextField()  # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 评论者
