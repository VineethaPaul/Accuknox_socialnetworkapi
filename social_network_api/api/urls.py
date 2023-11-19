from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='user_signup'),
    path('login/', LoginAPI.as_view(), name='user_login'),
	path('search/', UserSearchAPI.as_view(), name='user_search'),
 	path('friend_request/', FriendRequestAPI.as_view(), name='friend_request'),
 	path('friend_request/<int:pk>', FriendRequestAPI.as_view(), name='friend_request'),
 	path('friends_list/', FriendsListAPI.as_view(), name='friends_list'),
 	path('pending_friend_requests/', PendingFriendRequestsAPI.as_view(), name='pending_friend_requests'),
 	path('friend_request_exceed/', FriendRequestExceedAPI.as_view(), name='friend_request_exceed'),
 	
]
