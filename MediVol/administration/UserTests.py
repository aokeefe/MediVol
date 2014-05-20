from django.contrib.auth.models import User, Group

class UserTests:
    @classmethod
    def user_is_admin(self, user):
        if user.is_authenticated() and len(user.groups.all()) > 0:
            return user.groups.all()[0].name == 'Admin'
        return False

    @classmethod
    def user_can_create_box(self, user):
        if user.is_authenticated() and len(user.groups.all()) > 0:
            return user.groups.all()[0].name == 'Admin' or user.groups.all()[0].name == 'Guest'
        return False

    @classmethod
    def user_can_see_box_info(self, user):
        if user.is_authenticated() and len(user.groups.all()) > 0:
            return user.groups.all()[0].name == 'Admin' or user.groups.all()[0].name == 'Box Transfer'
        return False

    @classmethod
    def user_can_see_inventory(self, user):
        if user.is_authenticated() and len(user.groups.all()) > 0:
            return user.groups.all()[0].name == 'Admin' or \
                user.groups.all()[0].name == 'Box Transfer' or \
                user.groups.all()[0].name == 'Read Only'
        return False

    @classmethod
    def user_can_transfer_boxes(self, user):
        if user.is_authenticated() and len(user.groups.all()) > 0:
            return user.groups.all()[0].name == 'Admin' or user.groups.all()[0].name == 'Box Transfer'
        return False
