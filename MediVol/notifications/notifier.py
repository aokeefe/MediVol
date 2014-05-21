import mandrill
import os
import sys

#Executing from DJango shell kept complaining about indentation error so I just
#did it this way. The path is relative to whats on the vagrant VM.
sys.path.append('/var/www/MediVol')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")

#All emails comes from the system so setting the email address here.
#Note: The email below will need to be changed to Intervols production email once deployed
sender_email = 'sxb5828@rit.edu'

#This method communicates with Mandrill via their API to send out emails
def send_message(subject, recipient_email, recipient_name, message):

    #The API key will need to be changed to InterVols own account. Currently it is using my API key
    api_key = 'x9AjbnyiNKtL0Avv1N7oCw'

    try:
        mandrill_client = mandrill.Mandrill(api_key)
        message = {'from_email': sender_email, 'from_name': 'Intervol automation bot', 'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}], 'headers': {'Reply-To': sender_email}, 'html': message, 'important': False, 'inline_css': None, 'subject': subject, 'to': [{'email': recipient_email, 'name': recipient_name, 'type': 'to'}], 'track_clicks': None, 'track_opens': None, 'tracking_domain': None, 'url_strip_qs': None, 'view_content_link': None}

        response = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
        print('Response from Mandrill API')
        print(response)

    except mandrill.Error, e:
        #TODO: need to raise this to fatal exception
        print 'Mandrill Error Occurred: %s - %s' % (e.__class__, e)
        raise

#This method can be removed next PR as it is only for testing
def main():

    subject_input = raw_input('Enter Email Subject: ')
    email_message = raw_input('Enter Email Message: ')
    recipient_email2 = raw_input('Enter Recipient Email: ')
    recipient_name2 = raw_input('Enter Recipient Name: ')

    send_message(subject_input, recipient_email2, recipient_name2, email_message)

if __name__ == '__main__':
    main()
