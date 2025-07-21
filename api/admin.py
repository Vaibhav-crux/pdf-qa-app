from django.contrib import admin
from .models import Document, InteractionLog, TTSState

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_at']
    search_fields = ['file_name']

@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'timestamp']
    search_fields = ['question', 'answer']
    list_filter = ['timestamp']

@admin.register(TTSState)
class TTSStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'voice_id', 'updated_at']
    search_fields = ['user__username']
    list_filter = ['updated_at']