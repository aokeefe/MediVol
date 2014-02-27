from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.core.mail import send_mail

NAME_LENGTH = 80
ABBREV_LENGTH = 4
ADDRESS_LENGTH = 200

RESET_CODE_LENGTH = 20

class Warehouse(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    abbreviation = models.CharField(max_length=ABBREV_LENGTH)
    address = models.CharField(max_length=ADDRESS_LENGTH)
    
    def __unicode__(self):
        return self.name

class ResetCode(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=RESET_CODE_LENGTH)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            # this is a new ResetCode. we need to delete the old ones
            codes_for_this_user = ResetCode.objects.filter(user=self.user)
        
            for reset_code_to_delete in codes_for_this_user:
                reset_code_to_delete.delete()
        
        super(ResetCode, self).save(*args, **kwargs) 
    
    @classmethod
    def generate_code(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(RESET_CODE_LENGTH))
    
    def send_reset(self):
        # TODO: how do i get the base URL of our site?
        message = 'Please follow the link below to reset the InterVol password for ' + self.user.username + '.\n\n' + 'http://localhost:8888/administration/reset_password/' + self.code
        
        # TODO: switch to mandrill?
        # TODO: change webmaster@intervol.org
        return send_mail('InterVol Password Reset', message, 'webmaster@intervol.org', 
            [ self.user.email ], fail_silently=False)
    
    def do_reset(self, password, confirm):
        
        
        return True
    
    def __unicode__(self):
        return self.code