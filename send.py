from urllib import request , parse
from db_controller import MySqlConnection
from time import gmtime , strftime , sleep
import csv
import sys
import argparse

# Constants
AUTH_KEY = '144872AoGnBaVgqLh59f59619'
BASE_URL = 'http://sms.globehost.com/api/sendhttp.php?'


class Logger:
    """
    Custom Logger to log activities to the stdout
    """
    ERROR_MSG = 'MESSAGE FILE NAME OR CONTACTS FILE NAME WAS NOT PROVIDED'
    SUCCESS_MSG = 'ALL MESSAGES SENT SUCCESSFULLY'

    def info(self,message):
        # Information level logging
        print('{} : {}'.format(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),message))

    def err(self,message,error):
        # Error level logging
        sys.stderr.write('{} : {}'.format(message,error))


class GlobehostSMS:
    """
    Python wrapper over Globehost SMS Service API
    """

    def __init__(self, options , *args, **kwargs):
        self.message_file_name = options['message_file_name']
        self.contacts_file_name = options['contacts_file_name']
        self.remove_redundant = options['remove_redundant']
        self.logger = Logger()

    def _send_request(self,url):
        """
        Sends the request to the url and returns a Response object.
        """
        req = request.Request(url , method='GET')
        res = request.urlopen(req)
        return res

    
    def _get_contacts_from_db(self , options):
        """
        Connects to the MySQL Database , queries for contacts and
        returns a list of contacts.
        """
        connection = MySqlConnection(options['username'],options['password'],options['db'])
        connection.connect_to_database()
        connection.use_table_and_column(options['table_name'],options['column_name'])
        return connection.get_contacts_from_database()


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


    def read_contacts_from_database(self,options):
        """
        Reads contacts from database
        """
        return self._get_contacts_from_db(options)


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
        r = self._send_request(BASE_URL + data_encoded)
        self.logger.info('Sent to {} with status {}'.format(contact,r.status_code))
        return r.status_code


    def send_bulk_message(self,contacts_list,message,sleep_time):
        """
        Sends the sms to all the contacts in the list
        """
        for contact in contacts_list:
            self.send_message(contact,message)
            sleep(min(10,sleep_time))

        self.logger.info(self.logger.SUCCESS_MSG)

