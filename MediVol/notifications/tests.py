"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from notifications.models import Notification
import notifications.notifier as send_api

class SimpleTestSend(TestCase):

    def test_basic_send(self):
    
        test_message = 'test message' 
        test_subject = 'test subject' 
        test_recipient_email = 'sxb5828@rit.edu'
        test_recipient_name = 'shun'
        notifier = Notification(message = test_message, subject = test_subject, recipient_email=test_recipient_email, recipient_name=test_recipient_name) 
 
        response = send_api.send_message(notifier)
