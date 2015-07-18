from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from .models import User, Business, Review


class UserSerializer(MongoEngineModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class ReviewSerializer(MongoEngineModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        depth = 2
        fields = ['created', 'author', 'comment', 'rating']
        read_only_fields = ['created']


class BusinessSerializer(MongoEngineModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Business
        depth = 3
        read_only_fields = ['overall_rating', 'tags']



