from django.shortcuts import render_to_response

#Display the main page of ordering 
def orders_main(request):
    return render_to_response('orders/index.html')
