from django.urls import path
from .views import post_detail, post_list, post_share, post_comment

app_name = 'main'

urlpatterns = [
  path('', post_list, name='post_list'),
  path('<slug:post>/', post_detail, name='post_detail'),
  path('<int:post_id>/share/', post_share, name='post_share'),
  path('<int:post_id>/comment/', post_comment, name='post_comment')
]
