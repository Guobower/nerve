# -*- coding: utf-8 -*-
import datetime
from sense.sense import Sense
from collections import namedtuple
from random import randint
from cryptography.fernet import Fernet

import unittest
from unittest import TestCase
from unittest.mock import patch

Memory = namedtuple('Memory', 'total available percent used free')


class TestSense(TestCase):
    def setUp(self):
        self.cipher_key = Fernet.generate_key()
        self.sense = Sense(host_ip='127.0.0.1', cipher_key=self.cipher_key, is_debug=True)

    # Assuming 4 CPUs
    @patch('sense.sense.psutil.cpu_percent',
           return_value=[-0.01, 0, 100, 100.01])
    def test_get_cpu_usage(self, _):
        # CPU USAGE IS ONLY VALID WHEN IT IS BETWEEN 0 - 100
        result = self.sense.get_cpu_usage()
        self.assertEqual(result, [False, True, True, False])

    @patch('sense.sense.psutil.virtual_memory',
           return_value=Memory(total=0, available=0, percent=100.01, used=0, free=0))
    def test_get_memory_usage_greater_than_100(self, _):
        # MEMORY USAGE IS ONLY VALID WHEN IT IS BETWEEN 0 - 100 (FAIL)
        result = self.sense.get_memory_usage()
        self.assertEqual(result, False)

    @patch('sense.sense.psutil.virtual_memory',
           return_value=Memory(total=0, available=0, percent=-0.01, used=0, free=0))
    def test_get_memory_usage_less_than_0(self, _):
        # MEMORY USAGE IS ONLY VALID WHEN IT IS BETWEEN 0 - 100 (FAIL)
        result = self.sense.get_memory_usage()
        self.assertEqual(result, False)

    @patch('sense.sense.psutil.virtual_memory',
           return_value=Memory(total=0, available=0, percent=randint(0, 100), used=0, free=0))
    def test_get_memory_usage_less_than_ok(self, _):
        # MEMORY USAGE IS ONLY VALID WHEN IT IS BETWEEN 0 - 100 (PASS)
        result = self.sense.get_memory_usage()
        self.assertEqual(result, True)

    @patch('sense.sense.psutil.boot_time')
    def test_get_uptime_ok(self, boot_time):
        # BOOT TIME MUST ALWAYS BE LESSER THAN CURRENT TIME (PASS)
        # DUE TO DATETIME IS IMMUTABLE WE WILL MOCK BOOT TIME TO BE LESS THAN DATETIME.NOW()
        # https://solidgeargroup.com/mocking-the-time
        now = datetime.datetime.now() - datetime.timedelta(hours=4)
        boot_time.return_value = now.timestamp()

        result = self.sense.get_uptime()
        self.assertEqual(result, True)

    @patch('sense.sense.psutil.boot_time')
    def test_get_uptime_fail(self, boot_time):
        # BOOT TIME MUST ALWAYS BE LESSER THAN CURRENT TIME (FAIL)
        now = datetime.datetime.now() + datetime.timedelta(hours=4)
        boot_time.return_value = now.timestamp()

        result = self.sense.get_uptime()
        self.assertEqual(result, False)

    def test_encrypt(self):
        # check if encryption properly works
        original_text = 'Apple'
        cipher = Fernet(self.cipher_key)
        encrypted = self.sense.encrypt(original_text)
        decrypted = cipher.decrypt(encrypted.encode())

        self.assertEqual(original_text, decrypted.decode())


if __name__ == '__main__':
    unittest.main()
