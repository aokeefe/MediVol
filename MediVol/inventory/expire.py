import sys, os, pytz
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from inventory.models import Box
from notifications.notifier import send_message
from datetime import datetime
from django.contrib.auth.models import Group

now = datetime.now(pytz.UTC)
in_six_months = now.replace(now.year, (now.month + 6) % 12)
NO_EXP = datetime(1970,1,1,0,0,0,0,pytz.UTC)

boxes_expired = []
boxes_expiring_in_6_months = []

for box in Box.objects.all():
    expiration = box.get_expiration()

    if expiration is not None:
        if expiration < now:
            boxes_expired.append(box)
    
        elif expiration < in_six_months:
            boxes_expiring_in_6_months.append(box)

#maintains a record on the server
export = file(('/var/www/MediVol/records/'+str(now)).replace(' ', '_').replace(':', '_').replace('.', '_')+'.txt', 'w')
#placeholder for if someone wants to make this more pretty
message = ''

export.write('Boxes that have already expired:\n')
message += ('<p>Boxes that have already expired:<ul>')
for box in boxes_expired:
    export.write(str(box)+'\n')
    message += ('<li><a href="http://inventory.intervol.org/inventory/view_box_info/' + str(box) + '">' + str(box) + '</a>' + '</li>')
message += '</ul></p>'

export.write('\nBoxes expiring in 6 months:\n')
message += ('<p>Boxes expiring in 6 months:<ul>')
for box in boxes_expiring_in_6_months:
    export.write(str(box)+'\n')
    message += ('<li><a href="http://inventory.intervol.org/inventory/view_box_info/' + str(box) + '">' + str(box) + '</a>' + '</li>')
message += '</ul></p>'

admins = Group.objects.get(name='Admin').user_set.all()

for admin in admins: 
  send_message('Automated: Monthly Expiring Boxes Update', admin.email, 'Admin', message)


