from django.urls import path
from .views import post_detail, post_list, post_share, post_comment, add_post
from .feeds import LatestPostsFeed


app_name = 'main'

urlpatterns = [
  path('', post_list, name='post_list'),
  path('add/', add_post, name='add'),
  path('feed/', LatestPostsFeed(), name='post_feed'),
  path('<slug:post>/', post_detail, name='post_detail'),
  path('<int:post_id>/share/', post_share, name='post_share'),
  path('<int:post_id>/comment/', post_comment, name='post_comment'),
  path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
]
