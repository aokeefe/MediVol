from django.shortcuts import render_to_response

#Display main page of notifications
def notifications_main(request): 
    return render_to_response('notifications/index.html')

