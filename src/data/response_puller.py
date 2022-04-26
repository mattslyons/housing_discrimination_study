#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email, traceback, getpass, imaplib

def read_email():
    try:
        mail = imaplib.IMAP4('127.0.0.1',1143)
        mail.login('mattslyons@protonmail.com','JyhAuQmptEo9Myn0tJRLvw')
        mail.select('All Mail')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))

                    # extract timestamp
                    # extract 'sent to' email address for matching with original request email
                    # extract 'from' email for follow up
        
        # Loop to send follow-up emails
        # log sending of follow up emails so we only do it once for everyone                    

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

read_email()

