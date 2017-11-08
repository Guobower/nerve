# -*- coding: utf-8 -*-
import os

from cryptography.fernet import Fernet

from brain.brain import Client, Brain
from brain.brain import parse_clients

import unittest
from unittest import TestCase


class TestBrain(TestCase):
    def test_parse_clients(self):
        # Converts xml to namedtuple Client
        client_fixtures = [Client(hostname="192.168.100.101", port="22",
                                  username="vagrant", password="vagrant", email="client01@example.com")]
        clients = parse_clients(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_config.xml'))
        self.assertCountEqual(client_fixtures, clients)

    def test_ssh_connect(self):
        # TODO MAKE TEST FOR SSH AND SFTP CONNECTION
        pass

    def test_send_client_script(self):
        # TODO MAKE TEST FOR SENDING SCRIPT IN THE CLIENT
        pass

    def test_decrypt(self):
        cipher_key = Fernet.generate_key()
        brain = Brain(cipher_key=cipher_key)

        text = 'Apple'
        cipher = Fernet(cipher_key)
        encrypted = cipher.encrypt(text.encode()).decode()

        self.assertEqual(brain.decrypt(encrypted).decode(), text)


if __name__ == '__main__':
    unittest.main()
