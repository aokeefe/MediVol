from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.core.mail import send_mail
from notifications.notifier import send_message

RESET_CODE_LENGTH = 20

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

    def send_reset(self, reset_url):
        # TODO: how do i get the base URL of our site?
        message = 'Please follow the link below to reset the InterVol password for ' + self.user.username + '.\n\n' + reset_url + '/' + self.code

        send_message('InterVol Password Reset', self.user.email, self.user.username, message)

        return True

    def do_reset(self, password):
        self.user.set_password(password)
        self.user.save()

        return self.user.check_password(password)
