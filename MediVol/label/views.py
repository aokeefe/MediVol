from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from administration.UserTests import UserTests
from inventory.models import Box, Contents
from label.barcodes import BarcodeGen
from django.utils.html import escape

def create_label(request, box_barcode):

  # Get the box information from db 
  box = Box.objects.get(barcode=box_barcode)
  box_id = box.box_id
  box_category_letter = box.box_category.letter
  box_category_name = box.box_category.name
  box_contents = Contents.objects.filter(box_within=box) 
  box_weight = box.weight
  box_expiration = box.get_expiration_display

  # Get barcode of box 
  box_barcode = BarcodeGen(box_barcode).get_image()

  # Return the label information
  context = { 
      'box_id': box_id,
      'box_category_letter': box_category_letter,
      'box_category_name': box_category_name,
      'box_contents': box_contents,
      'box_weight': box_weight,
      'box_expiration': box_expiration,
      'box_barcode': box_barcode
  }

  return render(request, 'label/label.html', context)
