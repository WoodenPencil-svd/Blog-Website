from django.urls import path, include
from API.post import *
from API.profile import *


post_urlpartterns = [ 
    path('list/',PostListApi.as_view(),name='post-list'),
    path('<uuid:pk>/detail/',PostRetriveApi.as_view(),name ='post-detail'),
    path('<int:pk>/user_post/',PostOfUserApi.as_view(),name='post-user'),
    path('create/',PostCreateApi.as_view(),name = 'create-post'),
    path('<uuid:pk>/update/',PostUpdateApi.as_view(),name='post-update'),
    path('<uuid:pk>/delete',PostDeleteApi.as_view,name='post-delete')
                     
]

profile_urlpatterns = [ 
                       
]


api_urlpatterns = [ 
    path('post/', include((post_urlpartterns,'post'))),
    path('profile/',include((profile_urlpatterns,'profile'))),
    
]