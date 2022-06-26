from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.Home, name="home"),
    path('blog/',views.Blog, name="blog"),
    path('create_post/',views.post_create, name="post_create"),
    path('post/<pk>/',views.post_detail,name="post_detail"),
    path('post/<pk>/update',views.post_update,name="post_update"),
    path('post/<pk>/delete',views.post_delete,name="post_delete"),
    path('topic/<pk>/detail',views.Topic_detail,name="topic_detail"),
    path('login/',views.login_page,name="login_page"),
    path('logout/',views.logout_page,name="logout_page"),
    path('register/',views.register_page,name="register_page"),
]
# path('post/<int:pk>/delete-comment', views.delete_comment, name='delete_comment'),