from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Message(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]

    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(default=now, editable=False)
    content = models.CharField(max_length=1000)
