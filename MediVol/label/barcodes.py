from base64 import b64encode
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPM

"""
Used to get code128 type barcodes, text_vale is barcode string, width, height, and fontSize defalt to values that work with printer
"""
class BarcodeGen(Drawing):
    def __init__(self, text_value, width=2.2, height=80, fontSize=30):
        barcode = createBarcodeDrawing('Code128', quiet=False, value=text_value, barWidth=width, barHeight=height, fontSize=fontSize, humanReadable=True)
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