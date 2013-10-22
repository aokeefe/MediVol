from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def get_box_names(request):
    return simplejson.dumps( { 'message': 'test' } )