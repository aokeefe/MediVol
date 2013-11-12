import uuid
from django.db import models

class Notification(models.Model): 
 
    sent_date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000) 
    subject = models.CharField(max_length=200)
    recipient_email = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=50)
           
