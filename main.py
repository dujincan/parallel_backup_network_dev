#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/10 2:56 下午
# @Author  : Du Jincan
# @Email   : jincan.du@gmail.com
# @File    : main.py
# @Software: PyCharm

import multiprocessing as mp
import xlrd

from mail_to_admin import mail_to_admin
from backup_network_dev import backup_network_dev

excelfile = "xxxxxx.xlsx"

if __name__ == '__main__':

    processes = []
    backup_msg = []

    workbook = xlrd.open_workbook(excelfile)
    sheet = workbook.sheet_by_index(0)

    for device in range(1, sheet.nrows):
        ip = sheet.row(device)[1].value
        port = sheet.row(device)[2].value
        username = sheet.row(device)[3].value
        password = sheet.row(device)[4].value
        secret = sheet.row(device)[5].value
        device_type = sheet.row(device)[6].value

        node = {
            "device_type": device_type,
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
            "secret": secret,
        }
        processes.append(mp.Process(target=backup_network_dev, args=[node]))
        msg = backup_network_dev(node)
        backup_msg.append(msg)

    for p in processes:
        p.start()
        # print(p.pid)

    for p in processes:
        p.join()

    mail_context = '\n'.join(backup_msg)

    mail_conf = {'my_sender': 'xxxxxx',
                 'my_pass': 'xxxxxx',
                 'recipients': ["xxxxxx", "xxxxxx"],
                 'mail_context': mail_context,
                 'mail_subject': 'xxxxxx',
                 'mail_server': "xxxxxx",
                 'port': 465,
                 }

    mail_to_admin(**mail_conf)
