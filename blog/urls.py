from django.urls import path
from . import views

urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>/', views.blogs_with_type, name='blogs_with_type'),
    path('manage_blog/', views.manage_blog, name='manage_blog'),
    path('write_blog/', views.write_blog, name='write_blog'),
    path('delete_blog/<int:blog_pk>', views.delete_blog, name='delete_blog'),
    path('edit_blog/<int:blog_pk>', views.edit_blog, name='edit_blog'),
    path('', views.blog_list, name='blog_list'),
]
