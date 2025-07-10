from django.urls import path
from .views import AskQuestionView, DocumentUploadView

urlpatterns = [
    path('ask-question/', AskQuestionView.as_view(), name='ask-question'),
    path('upload-document/', DocumentUploadView.as_view(), name='upload-document'),
]