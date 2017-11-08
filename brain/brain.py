# -*- coding: utf-8 -*-
import os
import paramiko
import xml.etree.ElementTree as ET

from collections import namedtuple
from cryptography.fernet import Fernet

from brain.db import Database
from brain.mailer import Mailer

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SENSE_DIR = os.path.join(os.path.split(BASE_DIR)[0], 'sense')

Client = namedtuple('Client', 'hostname port username password email')


class Brain(object):
    ssh_client = None
    stfp_client = None

    def __init__(self, clients=None, db=None, mailer=None,
                 cipher_key=None, remote_tmpdir='/tmp/nerve_client'):
        self.clients = clients
        self.remote_tmpdir = remote_tmpdir
        self.cipher_key = cipher_key or Fernet.generate_key()
        self.sense_script = 'sense.py'

        self.db = db
        self.mailer = mailer

    def ssh_connect(self, hostname, port, username, password):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
            self.stfp_client = self.ssh_client.open_sftp()
            print(f'ssh and sftp connection to {hostname}:{port} established')

        except paramiko.SSHException:
            print(f'ssh and sftp connection to {hostname}:{port} failed')

    def send_sense_script(self):
        try:
            self.stfp_client.chdir(self.remote_tmpdir)
            # CLEAR ALL FILES
            self.ssh_client.exec_command("rm .")
        except IOError:
            self.stfp_client.mkdir(self.remote_tmpdir)
            self.stfp_client.chdir(self.remote_tmpdir)

        src = os.path.join(SENSE_DIR, self.sense_script)
        dst = self.remote_tmpdir + f'/{self.sense_script}'
        self.stfp_client.put(src, dst)
        print('client script sent')

    def ssh_close(self):
        self.ssh_client.close()
        print('connection closed')
        print("============================================")

    def decrypt(self, encrypted_text):
        cipher = Fernet(self.cipher_key)
        print('message decrypted')
        return cipher.decrypt(encrypted_text.encode())

    def store_logs(self, log):
        logs = log.decode().split(',')
        for r in logs:
            # REMOVES BLANKS
            # index value
            # 0     timestamp_date
            # 1     timestamp_time
            # 2     status
            # 3     component
            # 4     value
            row = [i for i in r.split(' ') if i != '']

            data = {
                'timestamp': ' '.join([row[0], row[1]]),
                'hostname': row[2],
                'status': row[3],
                'component': row[4],
                'value': row[5],
            }
            self.db.insert_logs(data)
        self.db.commit()
        print('logs stored')

    def send_logs(self):
        for client in self.clients:
            print(f'sending email to {client.email}')
            logs = self.db.get_logs(client.hostname)
            data = []
            for line in logs:
                line_string = ' '.join([j for j in [str(i) for i in line[1:-1]]])
                data.append(line_string)

            self.mailer.send(client=client, data='\n'.join(data))

            logs_ids = [i[0] for i in logs]
            self.db.update_sent_logs(logs_ids)
        self.db.commit()

    def run(self):
        print("============================================")
        print("NERVE APPLICATION version 1")
        print("BY Marc Philippe de Villeres")
        print("============================================")
        for client in self.clients:
            self.ssh_connect(hostname=client.hostname, port=int(client.port),
                             username=client.username, password=client.password)
            self.send_sense_script()
            cmd = f"python3.6 {self.remote_tmpdir}/{self.sense_script} --host-ip {client.hostname} " \
                  f"--cipher-key '{self.cipher_key.decode()}'"
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd, get_pty=True)
            if stdout.channel.recv_exit_status() == 0:
                lines = stdout.readlines()
                if len(lines) == 1:
                    encrypted_text = lines[0]
                    decrypted_text = self.decrypt(encrypted_text)
                    self.store_logs(decrypted_text)
                else:
                    # TODO HANDLE ERROR HERE
                    pass
            else:
                # TODO HANDLE ERROR HERE
                pass
            self.ssh_close()
        self.send_logs()
        # TODO CONSIDER DELETING CLIENT SCRIPT FILE


def parse_clients(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    clients = []
    for i in root.findall('./client'):
        clients.append(Client(**i.attrib))
    return clients


if __name__ == '__main__':
    clients = parse_clients(os.path.join(BASE_DIR, 'config.xml'))

    db = Database('demo.db')
    db.connect()
    db.create_table()

    mailer = Mailer(hostname='192.168.100.200', port=1025)

    brain = Brain(clients=clients, db=db, mailer=mailer)
    brain.run()
