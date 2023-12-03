from django.urls import path
from App import views

urlpatterns = [
    path('create/',views.postCreate, name='postcreate'),
    path('',views.Home, name='home'),
    path('detail/<int:post_id>/',views.postDetail,name='postdetail'),
    path('update/<int:post_id>/',views.postUpdate,name='postupdate'),
    path('delete/<int:post_id>/',views.postDelete, name='postdelete'),
    path('login/',views.signin, name='login'),
    path('logout/', views.singout, name='logout'),
    path('cmtcreate/<int:post_id>/',views.cmtcreate,name='cmtcreate'),
    path('cmtupdate/<int:cmt_id>/<int:post_id>/', views.cmtupdate, name='cmtupdate'),
    path('cmtdelete/<int:cmt_id>/<int:post_id>/', views.cmtdelete, name='cmtdelete'),
    path('search_by/', views.search_by),
    path('profile/<int:id>/',views.profile,name='profile'),
    path('register/',views.register,name='register'),
    path('editprofile/<int:user_id>/',views.editprofile, name='editprofile')
]