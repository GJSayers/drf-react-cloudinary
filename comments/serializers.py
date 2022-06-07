from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model, Adding 3 extra on returning list of Comments
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)
    
    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'post', 'created_at', 'updated_at', 'is_owner',
            'profile_id', 'profile_image', 'content',
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model in Detail View, post is a read only field 
    that does not resetting on each update
    """
    post = serializers.ReadOnlyField(source='post.id')
    