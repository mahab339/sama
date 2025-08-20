import uuid
from django.db import models
from django.utils import timezone

class ClientType(models.TextChoices):
    WEB = 'web', 'Web'
    ANDROID = 'android', 'Android'
    IOS = 'ios', 'iOS'
    API = 'api', 'API'

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_type = models.CharField(
        max_length=20,
        choices=ClientType.choices,
        default=ClientType.API
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'client_type']),
        ]
        unique_together = ('id', 'client_type')

class Calculation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='calculations')
    expression = models.TextField()
    result = models.FloatField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client', 'created_at']),
            models.Index(fields=['created_at']),
        ]
