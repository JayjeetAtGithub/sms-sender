import os
try:
    import requests
except ImportError:
    os.system('pip install requests')

import requests
import urllib
import csv
import time

auth_key = '144872AoGnBaVgqLh59f59619'
url = 'http://sms.globehost.com/api/sendhttp.php?'


def send_message(contact):

    message = """
        Warm up everyone! The wait for JCC is over. 
        We are all set to begin it this evening at 5:45 PM in LG 11,12 and 13. 
        Pull up your socks, pick up your pens, set your mind straight and put down your logic.
        May the best team win. 
        Note : On spot Registrations are welcome. Please carry a pen with yourselves.

        Register at jcc.nitdgplug.org
        """

    data = {
        'authkey': auth_key,
        'mobiles': contact,
        'message': message,
        'sender': 'GNULUG',
        'route': '4',
    }

    data_encoded = urllib.urlencode(data)
    r = requests.get(url + data_encoded)
    print('Message Sent Successfully to ', contact, r.status_code)
    return r.status_code



"""Array of contacts"""
contacts_array = [8436500886]

contacts_array.sort()

visited = 0

non_redundant_array = []

for contact in contacts_array:
    if visited != contact:
        non_redundant_array.append(contact)
        visited = contact

print(len(non_redundant_array))

for contact in non_redundant_array:
    send_message(contact)
    time.sleep(2)

