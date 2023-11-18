from django.contrib import admin
from django.urls import path
from . import views

app_name='fefi'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('feed/',views.feed,name='feed'),
    path('profiles/',views.profiles,name='profiles'),
    path('edit/',views.edit,name='edit'),
    path('edit2/',views.edit2,name='edit2'),
    path('profiles/<int:profile_id>/',views.profile,name='profile'),
    path('profile/followers/<int:profile_id>/',views.followers,name='followers'),
    path('profile/follows/<int:profile_id>/',views.follows,name='follows'),
    path('fef_like/<int:fef_id>/',views.fef_like,name='fef_like'),
    path('fef_like2/<int:fef_id>/',views.fef_like2,name='fef_like2'),
    path('new_fef/<int:profile_id>/',views.new_fef,name='new_fef'),
    path('photo/<int:pk>/',views.photo,name='photo'),
    path('unfollow/<int:pk>/',views.unfollow,name='unfollow'),
    path('follow/<int:pk>/',views.follow,name='follow'),
    path('unfollow2/<int:pk>/',views.unfollow2,name='unfollow2'),
    path('follow2/<int:pk>/',views.follow2,name='follow2'),
    path('delete_fef/<int:fef_id>/',views.delete_fef,name='delete_fef'),
    path('search/',views.search,name='search'),
    path('reply/<int:fef_id>/',views.reply,name='reply'),
    path('reply_delete/<int:reply_id>/',views.reply_delete,name='reply_delete'),
    path('reply_like/<int:reply_id>/',views.reply_like,name='reply_like'),
   
    



    
]