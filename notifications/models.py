from django.db import models
from accounts.models import BaseModel, User

# Create your models here.

class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    object_id = models.CharField(max_length=225)

    def __str__(self) -> str:
        return self.title

class Messages(BaseModel):
    receiver = models.CharField(max_length=20)
    message = models.TextField(default="")
    sent = models.BooleanField(default=False)
    response_message = models.CharField(max_length=525)
    message_id = models.CharField(max_length=225)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Messages"
    
    def __str__(self) -> str:
        return self.email

class Emails(BaseModel):
    receiver = models.EmailField()
    message = models.TextField(default="")
    sent = models.BooleanField(default=False)
    response_message = models.CharField(max_length=525, blank=True, null=True)
    status_code = models.CharField(max_length=225)
    subject = models.CharField(max_length=225, default="")
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Emails"
    
    def __str__(self) -> str:
        return self.email