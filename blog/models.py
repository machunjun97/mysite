from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from reading_count.models import ReadNumExpandMethod


class BlogType(models.Model):  # 博客类型
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.type_name}"


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=60)  # 文章标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)  # 博客类型
    context = RichTextUploadingField(null=True)  # 文章内容
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 文章作者
    create_time = models.DateTimeField(auto_now_add=True)  # 文章创建时间
    last_updated_time = models.DateTimeField(auto_now_add=True)  # 文章修改时间

    def __str__(self):
        return f"{self.title}"  # 定义对象名称为title

    class Meta:
        ordering = ['-create_time']  # 默认以日期从小到大排序
