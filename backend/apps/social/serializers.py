from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    owner_email = serializers.EmailField(source="owner.email", read_only=True)
    owner_name = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "excerpt",
            "owner_id",
            "owner_email",
            "owner_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "owner_id", "owner_email", "owner_name",
            "excerpt", "created_at", "updated_at"
        ]

    def owner_name(self, obj):
        if obj.owner.first_name or obj.owner.last_name:
            return f"{obj.owner.first_name or ''} {obj.owner.last_name or ''}".strip()
        return obj.owner.email

    def get_excerpt(self, obj):
        return obj.content[:120] + "..." if len(obj.content) > 120 else obj.content

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Заголовок должен быть не менее 3 символов")
        return value

    def validate_content(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Содержимое должно быть не менее 3 символов")
        return value
