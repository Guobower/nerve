# -*- coding: utf-8 -*-
import argparse
import os

from brain.brain import BASE_DIR, Brain
from brain.db import Database
from brain.mailer import Mailer
from brain.brain import parse_clients

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", help="Database Name", type=str, default='demo.db')
    parser.add_argument("--smtp-ip", help="SMTP IP Address", type=str, default='192.168.100.200')
    parser.add_argument("--smtp-port", help="SMTP Port", type=int, default=1025)
    parser.add_argument('--client-config', help='Client Configuration File', type=str, default='brain/config.xml')
    parser.add_argument('--cipher-key', help='Encryption Key', type=str)
    args = parser.parse_args()

    clients = parse_clients(args.client_config)

    db = Database(args.database)
    db.connect()
    db.create_table()

    mailer = Mailer(hostname=args.smtp_ip, port=args.smtp_port)

    brain = Brain(clients=clients, db=db, mailer=mailer, cipher_key=args.cipher_key)
    brain.run()
