# -*- coding: euc-kr -*-

from admin import process_admin
from consumer import process_consumer

import os


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def __main__():
    while True:
        print("====Main menu====")
        print("1. �Һ���")
        print("2. ������")
        print("3. ����")

        try:
            a = int(input("menu: "))
        except ValueError:
            clearConsole()
            print("[Value Error]")

        if a == 1:
            clearConsole()
            process_consumer()
            #clearConsole()
        elif a == 2:
            clearConsole()
            process_admin()
            #clearConsole()
        elif a == 3:
            exit()
        else:
            clearConsole()
            print("[Invalid Number]")



__main__()
