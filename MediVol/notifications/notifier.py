import mandrill
import uuid
import datetime
from notification import Notification

#All emails come from the system so setting the email address here.
#NOTE: The email below will need to be changed to InterVols production email once deployed.
sender_email = 'sxb5828@rit.edu'

#TODO: Need to complete this
#Method to log notification to DB 
#Stores each notification that comes in in the DB
def log_notification(subject, message, recipient_email, recipient_name):

    id = uuid.uuid1()
      
#TODO: 
#Fetches message from Mandrill using the 
#tag attribute to search for the specific email.
def fetch_message(tag):
    pass 
    
#This method communicates to Mandrill via their API to send out emails  
def send_message(notification): 
    
    #The API key will need to be changed to InterVols own account. Currently it is using my API key
    api_key = 'x9AjbnyiNKtL0Avv1N7oCw'
    subject = notification.subject
    recipient_email = notification.recipient_email
    recipient_name = notification.recipient_name
    email_id = notification.id 
    message = notification.message
    
    try:
        mandrill_client = mandrill.Mandrill(api_key)
        message = {'from_email': sender_email,
            'from_name': 'MediVol Test User',
            'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}],
            'headers': {'Reply-To': sender_email},
            'html': message,
            'important': False,
            'inline_css': None,
            'subject': subject,
            'to': [{'email': recipient_email,
                    'name': recipient_name,
                    'type': 'to'}],
            'track_clicks': None,
            'track_opens': None,
            'tracking_domain': None,
            'url_strip_qs': None,
            'view_content_link': None,
                'tags':[email_id]}
            
        result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
        print('Resposne from Mandrill API')        
        print (result)
           
    except mandrill.Error, e:
        print 'Mandrill Error Occurred: %s - %s' % (e.__class__, e)
        raise 

#This method can be removed next PR as it is only for testing 
def main(): 
    subject_input = raw_input('Enter Email Subject: ')
    email_message = raw_input('Enter Email Message: ')
    recipient_email2 = raw_input('Enter Recipient Email: ')
    recipient_name2 = raw_input('Enter Recipient Name: ')
    
    notifier = Notification(email_message, subject_input, recipient_email2, recipient_name2)
    send_message(notifier)
	                           
if __name__ == '__main__':
        main()
