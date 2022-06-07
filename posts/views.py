from django.db.models import Count
from rest_framework import generics, filters, permissions
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    List all posts 
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', disticnt=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View post detail 
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', disticnt=True)
    ).order_by('-created_at')
