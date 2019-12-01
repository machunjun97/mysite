from django.urls import path
from . import views


urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name="date")
]

