from django.contrib.auth.models import User, Group

class UserTests:
    @classmethod
    def user_is_admin(self, user):
        if user.is_authenticated() and len(user.groups.all()) > 0:
            return user.groups.all()[0].name == 'Admin'
        return False
