import sys
from urllib import request , parse
import csv
import time
import argparse

AUTH_KEY = '144872AoGnBaVgqLh59f59619'
BASE_URL = 'http://sms.globehost.com/api/sendhttp.php?'

class Messages:
    ERROR_MSG = 'MESSAGE FILE NAME OR CONTACTS FILE NAME WAS NOT PROVIDED'
    SUCCESS_MSG = 'ALL MESSAGES SENT SUCCESSFULLY'


class GlobeHostMessanger:

    def __init__(self, message_file_name , contacts_file_name , remove_redundant , *args, **kwargs):
        self.message_file_name = message_file_name
        self.contacts_file_name = contacts_file_name
        self.remove_redundant = remove_redundant

    def send_request(self,url):
        req = request.Request(url , method='GET')
        res = request.urlopen(req)
        return res


    def read_message(self):
        """
        Reads the message content from file
        and returns the message as a string.
        """
        message_body = None
        with open(self.message_file_name , 'r') as f:
            message_body = str(f.read())
        return message_body


    def read_contacts_from_csv_file(self , column_number):
        """
        Reads contacts numbers from CSV files into array and
        returns the array.
        """
        contacts_array = []
        with open(self.contacts_file_name , 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                contacts_array.append(row[column_number])
        return contacts_array


    def read_from_database(self):
        pass


    def remove_redundant_contacts(self,contacts):
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



    def send_message(self,contact,message):
        """
        Sends the message to the contact.
        """
        data = {
            'authkey': AUTH_KEY,
            'mobiles': contact,
            'message': message,
            'sender': 'GNULUG',
            'route': '4',
        }

        data_encoded = parse.urlencode(data)
        r = self.send_request(BASE_URL + data_encoded)
        print('Message Sent Successfully to ', contact, r.status_code)
        return r.status_code



    def sms_sender(self):
        """
        Sends sms with message given in message_file
        to all contacts in contacts file and
        also removes redundant contacts.
        """
        if self.message_file_name and self.contacts_file_name:
            contacts_array = self.read_contacts_from_csv_file(2)
            message_content = self.read_message()
            if self.remove_redundant:
                contacts_array = self.remove_redundant_contacts(contacts_array)
            
            for c in contacts_array:
                self.send_message(c,message_content)
                time.sleep(2)

            print(Messages.SUCCESS_MSG)
        else:
            print(Messages.ERROR_MSG)




