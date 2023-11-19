from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    from_user 	= 	models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user 	= 	models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status 		= 	models.CharField(max_length=20,default='pending')
    created_at 	= 	models.DateTimeField(auto_now_add=True)
