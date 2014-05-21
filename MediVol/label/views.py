from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from administration.UserTests import UserTests
from inventory.models import Box, Contents
from label.barcodes import BarcodeGen
from django.utils.html import escape

def create_label(request, box_barcode):

    # Get the box information from db 
    box = Box.objects.get(barcode=box_barcode)
    box_contents = Contents.objects.filter(box_within=box) 

    # Get barcode of box 
    box_barcode = BarcodeGen(box_barcode).get_image()

    # Return the label information
    context = { 
      'box': box,
      'box_contents': box_contents,
      'box_barcode': box_barcode
    }

    return render(request, 'label/label.html', context)
