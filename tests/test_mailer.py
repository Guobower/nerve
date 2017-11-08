# -*- coding: utf-8 -*-
from brain.brain import Client
from brain.mailer import Mailer

import unittest
from unittest import TestCase
from unittest.mock import patch


class TestMailer(TestCase):
    @patch("smtplib.SMTP")
    def test_send_ok(self, mock_smtp):
        data = ''.join(['log 1', 'log 2'])
        client = Client(hostname='127.0.0.1', port=22, username='user', password='pass', email='-@-.com')

        mailer = Mailer(hostname='192.168.100.100', port=1025)

        mailer.send(client, data)
        msg = mailer.get_msg(client, data)

        mock_smtp.return_value.sendmail.assert_called_once_with(
            'brain@nerve.com', [client.email], msg.as_string())

    @patch("smtplib.SMTP")
    def test_send_fail(self, mock_smtp):
        # TODO MAKE A FAILING TEST
        pass


if __name__ == '__main__':
    unittest.main()
