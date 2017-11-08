# -*- coding: utf-8 -*-

import smtplib
import email.message
import email.utils


class Mailer(object):
    def __init__(self, hostname, port, sender='brain@nerve.com'):
        self.smtp = smtplib.SMTP(host=hostname, port=port)
        self.sender = sender

    def get_msg(self, client, data):
        msg = email.message.Message()
        msg.add_header('Content-Type', 'text')
        msg['From'] = self.sender
        msg['To'] = client.email
        msg['Subject'] = f"Nerve Sense Logs for {client.hostname}"
        msg.set_payload("Health Check: \n" + data)

        return msg

    def send(self, client, data):
        msg = self.get_msg(client, data)

        try:
            self.smtp.sendmail(self.sender, [client.email], msg.as_string())
            print("Successfully sent email")
        except smtplib.SMTPException as e:
            print(e)


if __name__ == '__main__':
    from brain.brain import Client
    data = ['log 1', 'log 2']
    mailer = Mailer(hostname='192.168.100.100', port=1025)
    mailer.send(client=Client(hostname='127.0.0.1', port=22, username='user', password='pass', email='-@-.com'),
                data=data)
