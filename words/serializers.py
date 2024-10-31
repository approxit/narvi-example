from rest_framework import serializers
from words.models import Word, Folder


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Folder
        fields = ("id", "name")


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ("id", "content", "folder")


class WordGroupingSerializer(serializers.Serializer):
    words = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=255)
    )
