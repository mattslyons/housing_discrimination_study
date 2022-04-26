#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: MTLS
"""

import smtplib, datetime, pandas as pd, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pandas._libs.missing import NA

protonmail_pw = 'NqXlgJoaA-V9ejKxCaJu1A'
port_number = 1025

# See also data flow overview: https://docs.google.com/presentation/d/1ug_iXh5ZUFRYexmZSmq_uq3TI7Yvbh03kgC_SBAobmU/edit

# Import metadata extracted from individual posts, including contact emails
# and post update times:
metadata_from_individual_posts = \
    pd.read_csv('../../data/raw/posts_metadata_from_individual_posts.csv',
                parse_dates = ['updated','request_datetime'])
# this path string works on Linux machines but might need
# to be changed on other OS

# Import posts metadata extracted from per-region lists
# This includes some additional fields like price or the region,
# but can be omitted here if we use none of those in determining
# what emails to sent to whom
posts_metadata_from_lists = \
    pd.read_csv('../../data/raw/posts_metadata_from_lists.csv',
                parse_dates = ['posted'])
# this path string works on Linux machines but might need
# to be changed on other OS

# filter to posts that
# * have a valid "updated" time values
# * have a successfully extracted contact email
# * were updated less than 1 day ago
metadata_from_eligible_posts = \
    metadata_from_individual_posts[\
        ~metadata_from_individual_posts.updated.isna() &\
        ~metadata_from_individual_posts.contact_email.isna() &\
        (metadata_from_individual_posts.updated < \
            (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(1)) )]
# NB: right now (Dec 1) this shouldn't contain duplicates
# (multiple rows for the same URL) because the "scrape individual
# posts" script checks whether a contact email has already been
# extracted for that URL.

eligible_contact_emails = list(metadata_from_eligible_posts.contact_email)


data_path = os.path.realpath('../../data/Interim/rental_response_data.csv')
# version that works on Linux machines:
# data_path = os.path.realpath('data\\Interim\\rental_response_data.csv')

# read the list of email addresses and gender/race codings
rental_response_data = pd.read_csv(data_path, index_col = 0)

# keep only rows which do have an email address
recipient_list = rental_response_data.dropna(subset=['email'])

# keep only rows which no not have a sent_timestamp
recipient_list = recipient_list[recipient_list['sent_timestamp'].isnull()]

# create recipient lists for each sender
wm_list = recipient_list[(recipient_list["female"] == False) & (recipient_list["black"] == False)]
wf_list = recipient_list[(recipient_list["female"] == True) & (recipient_list["black"] == False)]
bm_list = recipient_list[(recipient_list["female"] == False) & (recipient_list["black"] == True)]
bf_list = recipient_list[(recipient_list["female"] == True) & (recipient_list["black"] == True)]

# function to compose a message based on race/gender coding
def compose_msg(sender, gender, name, recipient):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Responding to your Craiglist ad'
    message = 'Hello! Is your room on Craigslist still available for rent?'
    message += '\nI’m in my 20s, ' + gender
    message += ', and looking for a new place now that I’ve graduated and work full time. '
    message += 'If it’s possible for us to meet and for me to see the room, please be in touch.'
    message += '\n\nThanks!'
    message += '\n\n' + name

    msg.attach(MIMEText(message))
    return msg

# function to login, send messages to multiple recipients, and logout
def send_mail(sender_login, sender, gender, name, lists):
    mailserver = smtplib.SMTP('localhost', port_number)
    mailserver.login(sender_login, protonmail_pw)

    for recipient in lists["email"]:
        message = compose_msg(sender, gender, name, recipient)
        mailserver.sendmail(sender, recipient, message.as_string())
        now = datetime.datetime.now()
        print('sent to '+recipient+' from '+sender+' at '+now.strftime("%H:%M:%S"))
        
        # re-save the file after each send
        idx = lists[lists['email'] == recipient].index
        recipient_list.loc[idx,'sent_timestamp'] = now
        rental_response_data.update(recipient_list)
        rental_response_data.to_csv(data_path, index = True)
    
    mailserver.quit()

senders_login = ['ebonycwilliams@protonmail.com','isaiahjrobinson@protonmail.com','jenniferhnelson@protonmail.com','josephpbailey@protonmail.com']
senders = ['Ebony Williams <ebonycwilliams@protonmail.com>','Isaiah Robinson <isaiahjrobinson@protonmail.com>','Jennifer Nelson<jenniferhnelson@protonmail.com>','Joseph Bailey <josephpbailey@protonmail.com>']
names = ['Ebony Williams','Isaiah Robinson','Jennifer Nelson','Joseph Bailey']
genders = ['female','male','female','male']
lists = [bf_list, bm_list, wf_list, wm_list]

for i in range(len(senders)):
    send_mail(senders_login[i], senders[i], genders[i], names[i],  lists[i])
