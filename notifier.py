import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import simplejson

class Notifier:
    """MTA Notifier Class"""

    def __init__(self):
        # Get secrets
        if os.path.exists('api_secrets.json.nogit'):
            with open("api_secrets.json.nogit") as f:
                secrets = simplejson.loads(f.read())
            self.mailgun_url = secrets['MAILGUN_URL']
            self.mailgun_key = secrets['MAILGUN_KEY']
            self.my_email = secrets['MY_EMAIL']
        else:
            self.mailgun_url = os.environ.get('MAILGUN_URL')
            self.mailgun_key = os.environ.get('MAILGUN_KEY')
            self.my_email = os.environ.get('MY_EMAIL')

        self.message_to_send = ''

    def __call__(self):
        self.get_status()

    def get_status(self, line_to_consider=['123','ACE'], status_to_consider=['DELAYS','PLANNED WORK']):
        """Get MTA Subway status and return delay messages for lines 123, ACE"""

        self.message_to_send = ''
        send_message = False

        mta_status_url = 'http://web.mta.info/status/serviceStatus.txt'
        r = requests.get(mta_status_url)

        root = ET.fromstring(r.content)

        # Loop through the lines to grab the relevant information
        for line in root.findall('subway/line'):
            name = list(line.iterfind('name'))[0].text
            line_status = list(line.iterfind('status'))[0].text
            line_message = list(line.iterfind('text'))[0].text
            line_time = list(line.iterfind('Time'))[0].text
            print name, line_status, line_time

            if (name in line_to_consider) and line_status in status_to_consider:
                send_message = True
                soup = BeautifulSoup(line_message, 'html.parser')
                soup_parsed = ' '.join([y.strip() for y in soup.strings])
                self.message_to_send = self.message_to_send + 'Line: ' + name + '\n' + soup_parsed + '\n'

        if send_message:
            return self.message_to_send

    def send_email_message(self):
        """Send an email message
        See https://documentation.mailgun.com/api-sending.html#sending for more details on the Mailgun API
        Mailgun's sandbox domain is limited to 300/day (and free is 10000/month)
        """
        if self.message_to_send=='':
            print('No message to send. Run get_status()')
            return

        url = "https://api.mailgun.net/v3/" + self.mailgun_url + "/messages"
        from_text = "Mailgun Sandbox <postmaster@" + self.mailgun_url + ">"
        print url, from_text, self.my_email, self.mailgun_key
        return requests.post(
            url,
            auth=("api", self.mailgun_key),
            data={"from": from_text,
                  "to": self.my_email,
                  "subject": "MTA Notifier",
                  "text": self.message_to_send}) # can also be html for HTML text
