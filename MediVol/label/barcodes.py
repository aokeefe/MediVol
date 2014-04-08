import os, sys
import time
sys.path.append('/var/www/MediVol/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from base64 import b64encode
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPM
from inventory.models import Box

class BoxLabel(Drawing):
    def __init__(self, barcode_value, width=200, height=320, fontSize=30):
        barcode = BarcodeGen(barcode_value)
        barcode.translate((width-barcode.width)/2, 0)

        Drawing.__init__(self, width, height)
        self.add(barcode, name='barcode')

        box = Box.objects.get(barcode=barcode_value)

        box_category = String(10, 275, box.box_category.letter)
        box_category.fontSize = 55

        box_id = String(10, 230, box.box_id)
        box_id.fontSize = 55

        expiration = String(12, 195, "Exp: " + box.get_printable_expiration())
        expiration.fontSize = 30

        category = String(12, 165, box.box_category.name)
        category.fontSize = 15

        weight = String(12, 150, "Weight: " + "%.1f" % box.weight + ' lbs.')
        weight.fontSize = 15 

        contents = String(12, 135, "Contents:")
        contents.fontSize = 15

        count = 120

        for content in box.contents_set.all():
            item = String(17, count, content.item.name)
            item.fontSize = 15
            self.add(item, "item")
            count = count - 15

        self.add(box_category, "box_category")
        self.add(box_id, "boxId")
        self.add(category, "category")
        self.add(expiration, "expiration")
        self.add(weight, "weight")
        self.add(contents, name="contents_of_box")

    def save_img(self, fileName, Dir='.'):
        self.save(formats=['png'], fnRoot=fileName)

    """
    Returns barcode as html img
    """
    def get_image(self):
        data = b64encode(renderPM.drawToString(self, fmt = 'PNG'))
        return '<img src="data:image/png;base64,{0}">'.format(data)

"""
Used to get code128 type barcodes, text_vale is barcode string, width, height, and fontSize defalt to values that work 
with printer
"""
class BarcodeGen(Drawing):
    def __init__(self, text_value, width=2.2, height=60, fontSize=15):
        barcode = createBarcodeDrawing('Code128', quiet=False, value=text_value, barWidth=width, barHeight=height, 
                                       fontSize=fontSize, humanReadable=True)
        Drawing.__init__(self,barcode.width,barcode.height)
        self.add(barcode, name='barcode')

    """
    Returns barcode as html img
    """
    def get_image(self):
        data = b64encode(renderPM.drawToString(self, fmt = 'PNG'))
        return '<img src="data:image/png;base64,{0}">'.format(data)
    
    """
    Saves barcode to filesystem
    """
    def save_img(self, fileName, Dir='.'):
        self.save(formats=['png'], fnRoot=fileName)
