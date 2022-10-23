# -*- coding: euc-kr -*-

from admin import process_admin
from consumer import process_consumer

import os

admin_manual_mapping = {
    'process_consumer': ['1', '�Һ���'],
    'process_admin': ['2', '������'],
    'process_exit': ['3', '����'],
}

invalid_input_type = {
    'invalid_manual_command': '�������� �ʴ� ��ɾ��Դϴ�.',
    'invalid_int_type': '���ڸ� �Է����ּ���.',
    'invalid_positive_number': '0 �ʰ� ����� �Է����ּ���.',
}

def transport_positive_number(input_value):
    if input_value.isnumeric() is not True:
        return 'invalid_int_type'
    elif int(input_value) <= 0:
        return 'invalid_positive_number'
    return int(input_value)

# custom input
def custom_input(prompt, transport_func, **kwargs):
    input_value = (input(prompt + ' : ')).strip()
    if kwargs == {}:
        result_value = transport_func(input_value)
    else:
        result_value = transport_func(input_value, **kwargs)
    return result_value

# processes
# �޴� ����
def process_view_menu():
    print('====Main menu====')
    print("1. �Һ���")
    print("2. ������")
    print("3. ����")

def process_exit():
    exit()

def transport_manual_input(input_value):
    for process_name, valid_input in admin_manual_mapping.items():
        if input_value in valid_input:
            return process_name
    return 'invalid_manual_command'

def manual_input(prompt):
    process_view_menu()
    process_name = custom_input(prompt, transport_manual_input)

    if process_name == 'invalid_manual_command':
        print(invalid_input_type[process_name])
        process_name = manual_input(prompt)
    elif process_name == 'process_view_menu':
        process_name = manual_input(prompt)
    return process_name

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def __main__():
    while True:
        process_name = manual_input('���� �޴��� �������ּ���.')

        if process_name != 'process_exit':
            globals()[process_name]()
            clearConsole()


__main__()
