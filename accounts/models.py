from django.db import models
from django.contrib.auth. models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .emails import send_account_activation_email
import uuid

# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
        
        
class profile(BaseModel):
    
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name="profile")
    email_token = models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)


@receiver(post_save, sender = User)
def send_email_token(sender, instance, created, **kwargs):
    try:   
        if created:
            email_token = str(uuid.uuid4())
            profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
        
    except Exception as e:
        print(e)
        
        
        

