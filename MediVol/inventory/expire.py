import sys, os, pytz
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from inventory.models import Box
from notifications.notifier import send_message
from datetime import datetime

now = datetime.now(pytz.UTC)
next_month = now.replace(now.year, (now.month % 12) + 1)
in_two_months = now.replace(now.year, (next_month.month % 12) + 1)
NO_EXP = datetime(1970,1,1,0,0,0,0,pytz.UTC)

boxes_with_no_expiration = []
boxes_unknown_expiration = []
boxes_expired = []
boxes_expiring_next_month = []
boxes_expiring_in_2_months =[]
boxes_not_expiring = []

for box in Box.objects.all():
    expiration = box.get_expiration()

    if expiration is None:
        boxes_with_no_expiration.append(box)

    elif expiration == NO_EXP:
        boxes_unknown_expiration.append(box)

    elif expiration < now:
        boxes_expired.append(box)

    elif expiration < next_month:
        boxes_expiring_next_month.append(box)

    elif expiration < in_two_months:
        boxes_expiring_in_2_months.append(box)

    else:
        boxes_not_expiring.append(box)

#maintains a record on the server
export = file(('/var/www/MediVol/records/'+str(now)).replace(' ', '_').replace(':', '_').replace('.', '_')+'.txt', 'w')
#placeholder for if someone wants to make this more pretty
message = ''

export.write('Boxes that have already expired:\n')
message += ('<p>Boxes that have already expired:<ul>')
for box in boxes_expired:
    export.write(str(box)+'\n')
    message += ('<li><a href=http://107.161.21.242/inventory/view_box_info/' + str(box) + '>' + str(box) + '</a>' + '</li>')
message += '</ul></p>'

export.write('Boxes expiring next month:\n')
message += ('<p>Boxes expiring next month:<ul>')
for box in boxes_expiring_next_month:
    export.write(str(box)+'\n')
    message += ('<li><a href=http://107.161.21.242/inventory/view_box_info/' + str(box) + '>' + str(box) + '</a>' + '</li>')
message += '</ul></p>'

export.write('\nBoxes expiring in 2 months:\n')
message += ('<p>Boxes expiring in 2 months:<ul>')
for box in boxes_expiring_in_2_months:
    export.write(str(box)+'\n')
    message += ('<li><a href=http://107.161.21.242/inventory/view_box_info/' + str(box) + '>' + str(box) + '</a>' + '</li>')
message += '</ul></p>'

send_message('Automated: Monthly Expiring Boxes Update', 'sxb5828@rit.edu', 'Shun', message)
#send_message('Automated: Monthly Expiring Boxes Update', 'shunmok@me.com', 'Shun', message)
#send_message('Automated: Monthly Expiring Boxes Update', 'nothingatall544@gmail.com', 'Bill', message)
#send_message('Automated: Monthly Expiring Boxes Update', 'Mike@mikelentini.com', 'Mike', message)
