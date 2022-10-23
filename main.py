# -*- coding: euc-kr -*-

from admin import process_admin
from consumer import process_consumer

import os

admin_manual_mapping = {
    'process_consumer': ['1', '소비자'],
    'process_admin': ['2', '관리자'],
    'process_exit': ['3', '종료'],
}

invalid_input_type = {
    'invalid_manual_command': '존재하지 않는 명령어입니다.',
    'invalid_int_type': '숫자만 입력해주세요.',
    'invalid_positive_number': '0 초과 양수만 입력해주세요.',
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
# 메뉴 보기
def process_view_menu():
    print('====Main menu====')
    print("1. 소비자")
    print("2. 관리자")
    print("3. 종료")

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
        process_name = manual_input('메인 메뉴를 선택해주세요.')

        if process_name != 'process_exit':
            globals()[process_name]()
            clearConsole()


__main__()
