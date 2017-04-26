"""
This is a version of the email project that
does NOT have printing and is clean of comments/etc.
Enjoy
"""
import imaplib, smtplib, email
from random import randint
from os import system

def login(username, password):
    global mail
    """
Login function. uses gmail IMAP server. Does not take keyboard interrupt exceptions.
    """
    smtp_server = "imap.gmail.com"
    smtp_port = 993
    mail = imaplib.IMAP4_SSL(smtp_server)
    mail.login(username, passwowrd)

def mailRead():
    try:
        names_pictures = {}
        mail.select('inbox')
    
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
    
        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(str(i), '(RFC822)')
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    maintype = msg.get_content_maintype()                    
                    email_attatchment = msg.get_payload()[1]

                    if maintype == 'multipart':
                        for part in msg.get_payload():
                            if part.get_content_maintype() == 'image':
                                for dataPeice in msg.get_payload():
                                    if part.get_content_maintype()[0] == 'text' and str(part.get_payload())[0:4] != "<div" and len(str(part.get_payload())) <= 32:
                                        body = str(part.get_payload())
                                        name = 'H:/turnin-images/image' + body.replace(" ", "_") + '.png'
                                        names_pictures[body] = name
                                        with open(name, 'wb') as file:
                                            file.write(email_attatchment.get_payload(decode=True))
                                    else:
                                        with open('H:/turnin-images/image' + str(randint(1, 10000)) + 'error.png', 'wb') as file:
                                            file.write(email_attatchment.get_payload(decode=True))
        return names_pictures
    except KeyboardInterrupt:
        mail.close()
        mail.logout()

if __name__ == '__main__':
    login()
    mailRead()
    input('Press enter to continue...')
