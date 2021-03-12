#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/12 8:25 上午
# @Author  : Du Jincan
# @Email   : jincan.du@gmail.com
# @File    : backup_network_dev.py
# @Software: PyCharm

from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException
from datetime import datetime
import time


def backup_network_dev(dev):
    try:
        net_connect = ConnectHandler(**dev)
        if dev['device_type']  == 'cisco_ios':
            net_connect.enable()
            output = net_connect.send_command("show run")
        elif dev['device_type'] == 'huawei':
            output = net_connect.send_command("dis cu")

        now = datetime.now()
        backup_file = "dev_" + dev['ip'] + "_" + str(now.year) + str(now.month) \
                      + str(now.day) + str(time.strftime("%H%M")) + ".cfg"
        backup = open(backup_file, "w")
        backup.write(output)
        backup.close()
        backup_msg = dev['ip'] + ' backup successful!'
        return backup_msg

    except NetMikoAuthenticationException as err_msg:
        return str(err_msg)

    except NetMikoTimeoutException as err_msg:
        return str(err_msg)

    except Exception as err_msg:
        return str(err_msg)
