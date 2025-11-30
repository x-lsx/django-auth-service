from django.shortcuts import render
from rest_framework import generics

from .models import Post
from .serializers import PostSerializer
from apps.permissions.permissions import CustomPermission

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("owner")
    serializer_class = PostSerializer
    permission_classes = [CustomPermission]
    resource_code = "posts"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("owner")
    serializer_class = PostSerializer
    permission_classes = [CustomPermission]
    resource_code = "posts"
