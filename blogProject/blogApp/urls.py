from django.urls import path
from blogApp import views

app_name ='blog_app'

urlpatterns = [
    path('', views.postListView.as_view(),name='post-list'),
    path('about', views.aboutView.as_view(),name='about' ),
    path('post-detail/<int:pk>', views.postDetails.as_view(),name='post-detail' ),
    path('create-post', views.createPost.as_view(),name='create-post' ),
    path('update-post/<int:pk>', views.updatePost.as_view(),name='update-post' ),
    path('delete-post/<int:pk>', views.deletePost.as_view(),name='delete-post' ),
    path('draft-list', views.draftListView.as_view(),name='draft-list' ),
    path('post/<int:pk>/add-comment', views.add_comment_post,name='add-comment' ),
    path('post/<int:pk>/approve-comment', views.approve_comment,name='approve-comment' ),
    path('post/<int:pk>/reject-comment', views.reject_comment,name='reject-comment' ),
    path('post/<int:pk>/publish-post', views.publish_post,name='publish-post' ),
    path('chat-api/', views.chat_with_gpt, name='chat_api'),
    path('chat/', views.chat_page, name='chat'),
]

