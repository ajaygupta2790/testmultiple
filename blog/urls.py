from django.urls import path, register_converter
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentView
)
from . import views
from updown.views import AddRatingFromModel



class NegativeIntConverter:
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value

register_converter(NegativeIntConverter, 'negint')


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('comment/', CommentView.as_view(), name='comment-create'),
    path('delete_comment/', views.delete_comment, name='comment-delete'),
    path('like_count/<int:post_id>', views.post_like_count, name='post-like-count'),
    path('comment_like_count/<int:post_id>', views.comment_like_count, name='coment-like-count'),
    path('post/<int:object_id>/rate/<negint:score>', AddRatingFromModel(), 
        {'app_label': 'blog',
        'model': 'Post',
        'field_name': 'rating',
    }, name="post_rating"),
    path('comment/<int:object_id>/rate/<negint:score>', AddRatingFromModel(), 
        {'app_label': 'blog',
        'model': 'Comment',
        'field_name': 'rating',
    }, name="post_rating")
]
