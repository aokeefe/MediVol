from django.db import models

class Notification(models.Model): 
        
        notification_id = models.CharField(max_length=50, null=True) 
        sent_date = models.DateTimeField(auto_now_add=True, blank=False)
        message = models.CharField(max_length=2000, null=False) 
        subject = models.CharField(max_length=200, null=False)
        recipient_email = models.CharField(max_length=100, null=False)
        recipient_name = models.CharField(max_length=50, null=False)         
