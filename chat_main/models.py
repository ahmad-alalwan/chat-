from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Messages(models.Model):
    auther=models.ForeignKey(User,related_name='auther_messages',on_delete=models.CASCADE)    
    content=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.auther.username
    def last_30_messages(self):
        return Messages.objects.order_by('-time').all()[:30]   