from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class FileListSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField()
