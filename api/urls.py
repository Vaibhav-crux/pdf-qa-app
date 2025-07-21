from django.urls import path
from .views import DocumentUploadView, AskQuestionView, TextToSpeechView

urlpatterns = [
    path('upload-document/', DocumentUploadView.as_view(), name='upload-document'),
    path('ask-question/', AskQuestionView.as_view(), name='ask-question'),
    path('text-to-speech/', TextToSpeechView.as_view(), name='text-to-speech'),
]