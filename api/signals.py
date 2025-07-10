from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document
from .utils import process_document

@receiver(post_save, sender=Document)
def process_uploaded_document(sender, instance, created, **kwargs):
    if created:
        process_document(instance.id)