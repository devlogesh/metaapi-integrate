from django.urls import path
from .views import *

urlpatterns = [
    path('post_on_fb_screen/',post_on_fb_screen,name='post_on_fb_screen'),
    path('post_on_fb/',FBpost.as_view(),name='post_on_fb'),
    path('get_post_on_fb/',GetFBpost.as_view(),name='get_post_on_fb'),
    path('get_post_on_fb_screen/',get_post_on_fb_screen,name='get_post_on_fb_screen'), 
    path('get_insights/',GetPostInsights.as_view(),name='get_post_on_fb_screen'), 
    path('get_comments/',GetPostComments.as_view(),name='get_post_on_fb_screen'), 
]