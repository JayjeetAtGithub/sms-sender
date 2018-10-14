import sys
import urllib
import csv
import time
import requests

AUTH_KEY = '144872AoGnBaVgqLh59f59619'
BASE_URL = 'http://sms.globehost.com/api/sendhttp.php?'
ERROR_MSG = "MESSAGE FILE NAME OR CONTACTS FILE NAME WAS NOT PROVIDED"
SUCCESS_MSG = "ALL MESSAGES SENT SUCCESSFULLY"


def read_message(file_name):
    """
    Reads the message content from file
    and returns the message as a string.
    """
    message_body = None
    with open(file_name , 'r') as f:
        message_body = str(f.read())
    return message_body


def read_contacts_from_text_file(file_name):
    """
    Reads the contacts from a text file and
    stores in an array
    """
    contacts_array = []
    with open(file_name) as f:
        for line in f:
            contacts_array.append(int(line))
    return contacts_array


def read_contacts_from_csv(file_name , column_number):
    """
    Reads contacts numbers from CSV files into array and
    returns the array.
    """
    contacts_array = []
    with open(file_name , 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            contacts_array.append(row[column_number])
    return contacts_array



def remove_redundant_contacts(contacts):
    """
    Removes the duplicats contacts from the array.
    """
    contacts.sort()
    visited = 0
    aux = []
    for contact in contacts:
        if visited != contact:
            aux.append(contact)
            visited = contact
    return aux



def send_message(contact,message):
    """
    Sends the message to the contact
    """
    data = {
        'authkey': AUTH_KEY,
        'mobiles': contact,
        'message': message,
        'sender': 'GNULUG',
        'route': '4',
    }

    data_encoded = urllib.urlencode(data)
    r = requests.get(BASE_URL + data_encoded)
    print('Message Sent Successfully to ', contact, r.status_code)
    return r.status_code



def sms_sender(message_file_name,contacts_file_name,remove_redundant):
    """
    Sends sms with message given in message_file
    to all contacts in contacts file and
    also removes redundant contacts
    """
    if message_file_name and contacts_file_name:
        contacts_array = read_contacts_from_csv(contacts_file_name,2)
        message_content = read_message(message_file_name)
        if remove_redundant:
            contacts_array = remove_redundant_contacts(contacts_array)
        
        for c in contacts_array:
            send_message(c,message_content)
            time.sleep(2)

        print(SUCCESS_MSG)
    else:
        print(ERROR_MSG)



if __name__ == "__main__":
    message_file_name = None
    contacts_file_name = None
    remove_redundant = False

    if sys.argv.count("--message") == 1:
        index = sys.argv.index("--message")
        message_file_name = str(sys.argv[index+1])

    if sys.argv.count("--contacts") == 1:
        index = sys.argv.index("--contacts")
        contacts_file_name = str(sys.argv[index+1])

    if sys.argv.count("--unique") == 1:
        remove_redundant = True

    sms_sender(message_file_name,contacts_file_name,remove_redundant)



"""
python send.py --message msg.txt --contacts cnt.csv
"""
