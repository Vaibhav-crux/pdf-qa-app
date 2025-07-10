from rest_framework import serializers
from .models import Document
from drf_spectacular.utils import extend_schema_field

class DocumentSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(max_length=255, help_text="Name of the PDF file")
    file = serializers.FileField(help_text="PDF file to upload (max 10MB)")

    class Meta:
        model = Document
        fields = ['file_name', 'file']

    def validate_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        if value.size > 10 * 1024 * 1024:  # Limit to 10MB
            raise serializers.ValidationError("File size exceeds 10MB limit.")
        return value

    def validate_file_name(self, value):
        if not value:
            raise serializers.ValidationError("File name is required.")
        return value

class AskQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000, help_text="Question to query the knowledge base")