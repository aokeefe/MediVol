import uuid
import datetime

class Notification: 

    def __init__(self, message, subject, recipient_email, recipient_name):
        
        self.id = str(uuid.uuid4())
        self.sent_date = datetime.datetime.now()
        self.message = message
        self.subject = subject 
        self.recipient_email = recipient_email
        self.recipient_name = recipient_name 
