# -*- coding: utf-8 -*-
import os
import datetime
import time
import psutil
import argparse
import sys

from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Sense(object):
    """
    Class Object for the client mainly for data gathering and encryption
    """
    def __init__(self, host_ip=None, duration=None, cipher_key='', is_debug=False):
        if not host_ip:
            raise ValueError('Host IP Address are required')
        self.host_ip = host_ip
        self.duration = duration
        self.cipher_key = cipher_key
        self.is_debug = is_debug
        self.dump = []

    def get_cpu_usage(self):
        cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
        result = []
        for i, cpu_percent in enumerate(cpu_percents):
            if 0.0 <= cpu_percent <= 100.0:
                self.display_value('DONE', f'CPU{i}', f'{cpu_percent}')
                result.append(True)
                continue
            self.display_value('FAILED', f'CPU{i}', f'{cpu_percent}')
            result.append(False)
        return result

    def get_memory_usage(self):
        mem = psutil.virtual_memory()
        mem_percent = mem.percent

        if 0.0 <= mem_percent <= 100.0:
            self.display_value('DONE', 'MEM', f'{mem_percent}')
            return True
        self.display_value('FAILED', 'MEM', f'{mem_percent}')
        return False

    def get_uptime(self):
        # https://www.programcreek.com/python/example/53873/psutil.boot_time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        uptime = now - boot_time
        uptime_sec = uptime.seconds + (uptime.days * 60 * 60 * 24)
#        days, hours, minutes = uptime.days, uptime.seconds // 3600, uptime.seconds // 60 % 60
        if now > boot_time:
            self.display_value('DONE', 'UPTIME', f'{uptime_sec}')
#            self.display_value('DONE', 'UPTIME', f'{days:02d}:{hours:02d}:{minutes:02d}')
            return True
        self.display_value('FAILED', 'UPTIME', f'{uptime}')
#        self.display_value('FAILED', 'UPTIME', f'{days:02d}:{hours:02d}:{minutes:02d}')
        return False

    def encrypt(self, text):
        # https://www.blog.pythonlibrary.org/2016/05/18/python-3-an-intro-to-encryption/
        cipher = Fernet(self.cipher_key)
        return cipher.encrypt(text.encode()).decode()

    def display_value(self, status, name, val):
        display = f"""{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f} {self.host_ip} {status:8} {name:8} {val:8}"""
        if self.is_debug:
            print(display)
        self.dump.append(display)

    def run(self):
        self.get_cpu_usage()
        self.get_memory_usage()
        self.get_uptime()
        encrypted = self.encrypt(', '.join(self.dump))
        sys.stdout.write(encrypted)
        time.sleep(0.1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-ip", help="Host IP Address", type=str)
    parser.add_argument('--duration', default=2, help='time in seconds before closing the script')
    parser.add_argument('--cipher-key', help='Encryption Key', type=str)
    args = parser.parse_args()

    if not args.host_ip:
        print('HOST IP Address is Required')
        sys.exit(0)

    sense = Sense(host_ip=args.host_ip, duration=args.duration, cipher_key=args.cipher_key)
    sense.run()
