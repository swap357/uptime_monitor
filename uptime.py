import smtplib
from threading import Thread

import datetime
import requests
import time

clients = {"http://auberginesolutions.com":["swapnil@auberginesolutions.com","sarthak@auberginesolutions.com"],
           "http://www.octaviuspharma.com":["swapnil@auberginesolutions.com", "kirtanpadia@gmail.com", "sarthak@auberginesolutions.com"],
           "http://www.travel-zone.ca":["swapnil@auberginesolutions.com","sarthak@auberginesolutions.com"]}
clients_down = {}

def site_up():
    while True:
        for client, emails in clients.items():
            try:
                r = requests.get(client, timeout = 60)
                if r.status_code == 200:
                    print client, ": Site is Up!"
                    time.sleep(60)
                else:
                    print client, ": Site down!"
                    clients_down[client] = emails
                    del clients[client]
                    for email in emails:
                        send_email("The monitor for "+client+" is down.", email, client)
                        # send email
            except requests.ConnectionError:
                print client, ": Site down!"
                clients_down[client] = emails
                del clients[client]
                for email in emails:
                    send_email("The monitor for "+client+" is down.[Connection Error]", email, client)
                    # send email

def site_down():
    while True:
        for client, emails in clients_down.items():
            time.sleep(60)
            try:
                r = requests.get(client, timeout = 60)
                if r.status_code == 200:
                    print client, ": Site is back up!"
                    clients[client] = emails
                    del clients_down[client]
                    for email in emails:
                        send_email("The monitor for "+client+" is back up.[200 OK]", email, client)
                        # send email
                else:
                    print client, ": Site still down!"
            except requests.ConnectionError:
                print client, ": Site still down!"

def send_email(input_message, email_to, client):
    print "send_mail ", input_message, " for ",client, " to ",email_to
    try:
        to = email_to
        gmail_user = 'username@domain.com'
        gmail_pwd = 'password'
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail_user,gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:[Alert] Site update ! \n'
        current_time = str(datetime.datetime.now())
        input_message = "\n" + input_message + " \nCurrent time: "+ current_time + "\n"
        print input_message
        # msg = header + input_message
        msg = header + input_message
        print msg
        smtpserver.sendmail(gmail_user, to, msg)
    except Exception as e:
        print e
    smtpserver.close()

try:
    t1 = Thread(target = site_up)
    t2 = Thread(target= site_down)
    t1.start()
    t2.start()
except Exception as e:
    print "Exception: ",e
    send_email("Monitor Script Exception: \n"+e,"swapnil@auberginesolutions.com","")