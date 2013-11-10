import uuid
from django.db import models

class Notification(models.Model): 
        
    notification_id = models.CharField(max_length=50) 
    sent_date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000) 
    subject = models.CharField(max_length=200)
    recipient_email = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=50) 

    @classmethod 
    def create(cls, email_message, email_subject, recipient_mail, recipient_name1):
        
        id = str(uuid.uuid4())
        notification = cls(notification_id=id, message=email_message, subject=email_subject, recipient_email=recipient_mail, recipient_name=recipient_name1)

        return notification
          
