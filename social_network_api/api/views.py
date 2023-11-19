from django.shortcuts import render
from rest_framework import status,generics,permissions,serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# User Signup API
class SignUpAPI(APIView):
    def post(self, request):
        email 		=	request.data.get('email')
        password 	=	request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user 		= 	User.objects.create_user(username=email, email=email, password=password)
        serializer 	= 	UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# User Login API
class LoginAPI(APIView):
    def post(self, request):
        email 		= 	request.data.get('email')
        password 	= 	request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user 		= 	User.objects.filter(email__iexact=email).first()

        if user and user.check_password(password):
            refresh = 	RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Search API with email and name
class UserSearchAPI(generics.ListAPIView):
    serializer_class 	= 	UserSerializer
    permission_classes 	= 	[IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search_keyword', '')
        try:
            return [User.objects.get(email=search_keyword)]
        except User.DoesNotExist:
            return User.objects.filter(Q(username__icontains=search_keyword) | Q(email__icontains=search_keyword))

# To send , accept or reject friend requests
class FriendRequestAPI(generics.CreateAPIView, generics.UpdateAPIView):
    queryset 			= 	FriendRequest.objects.all()
    serializer_class 	= 	FriendRequestSerializer
    permission_classes 	= 	[IsAuthenticated]


    def post(self, request, *args, **kwargs):
        # Sending friend requests
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Accepting or rejecting friend requests
        # partial = kwargs.pop('partial', True)
        instance 		= 	self.get_object()
        print(instance,'insssssss',request.data)
        if request.data['status'] == 'accept':
            # Accept the friend request
            instance.status = 'accepted'
            # instance.is_accepted = True
            instance.save()
            return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)
        elif request.data['status'] == 'reject' :
            # Reject the friend request
            instance.status = 'rejected'
            # instance.is_rejected = True
            instance.save()
            return Response({'detail': 'Friend request rejected.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

# To get friends list 
class FriendsListAPI(APIView):
    serializer_class 	= 	FriendRequestSerializer
    permission_classes 	= 	[IsAuthenticated]
    
    def get(self,request):
        friendsQuery 	= 	FriendRequest.objects.filter(status='accepted')
        friendsList 	= 	[]
        for i in friendsQuery:
            k = i.from_user + ' and ' + i.to_user
            friendsList.append(k)
        return Response(friendsList)

# Pending friend requests
class PendingFriendRequestsAPI(generics.ListAPIView):
    serializer_class 	= 	FriendRequestSerializer
    permission_classes 	= 	[IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(status='pending')
                    
# Not more than 3 requests in a minute
class FriendRequestExceedAPI(generics.CreateAPIView, generics.UpdateAPIView):
    queryset 			= 	FriendRequest.objects.all()
    serializer_class 	= 	FriendRequestSerializer
    permission_classes 	= 	[IsAuthenticated]

    def perform_create(self, serializer):
        user 			= 	self.request.user
        last_minute 	= 	timezone.now() - timedelta(minutes=1)
        recent_requests = 	FriendRequest.objects.filter(from_user=user, created_at__gte=last_minute).count()

        # Check if the user has sent more than 3 friend requests within the last minute
        if recent_requests >= 3:
            raise serializers.ValidationError("You cannot send more than 3 friend requests within a minute.")
        
        serializer.save()
