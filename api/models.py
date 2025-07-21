from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class InteractionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

class TTSState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    position = models.IntegerField(default=0)
    voice_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TTS for {self.user.username} at position {self.position}"