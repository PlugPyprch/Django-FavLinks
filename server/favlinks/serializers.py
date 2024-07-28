from .models import Category, Tag, FavoriteURL
from rest_framework import serializers

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'user']


class FavoriteSerializer(serializers.ModelSerializer):
    category = CatSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), source='tags', write_only=True, required=False
    )

    class Meta:
        model = FavoriteURL
        fields = [
            'id', 'user', 'url', 'title', 'category', 'category_id', 'tags', 'tag_ids',
            'created_at', 'updated_at', 'is_valid'
        ]