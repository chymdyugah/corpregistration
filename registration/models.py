from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class CorpMember(models.Model):
    BATCH_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    call_up = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255)
    batch = models.CharField(max_length=255, choices=BATCH_CHOICES)
    stream = models.SmallIntegerField()
    ppa = models.CharField(max_length=355)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
