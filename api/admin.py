from django.contrib import admin
from .models import Document, InteractionLog

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_at']

@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']