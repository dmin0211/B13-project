import settings
import os

string_before_prompt = ''

consumer_manual_mapping = {
    'process_view_menu': ['0', '메뉴 보기'],
    'process_drink_list': ['1', '음료수 목록 보기'],
    'process_drink_buy': ['2', '음료수 구입하기'],
    'process_money_input': ['3', '금액 투입하기'],
    'process_money_return': ['4', '투입 금액 반환받기'],
    'process_exit': ['5', '소비자 모드 나가기', 'exit', '소비자 모드 나가기(exit)'],
}

invalid_input_type = {
    'invalid_manual_command': '존재하지 않는 명령어입니다.',
    'invalid_int_type': '숫자만 입력해주세요.',
    'invalid_drink': '존재하지 않는 음료수입니다.',
    'invalid_not_negative_number': '0이상의 정수만 입력해주세요.',
    'invalid_drink_range': '유효하지 않은 음료수 번호입니다.',
    'invalid_sold_out' : '품절된 음료수입니다.',
    'invalid_money_range' : '잔액이 부족합니다.',
}

def transport_not_negative_number(input_value):
    try:
        input_value = int(input_value)
        if input_value < 0:
            return 'invalid_not_negative_number'
        return input_value
    except:
        return 'invalid_int_type'

# custom input
def custom_input(prompt, transport_func, **kwargs):
    input_value = input(prompt + ' : ')
    if kwargs == {}:
        result_value = transport_func(input_value)
    else:
        result_value = transport_func(input_value, **kwargs)
    return result_value

# processes
# 메뉴 보기
def process_view_menu():
    tmp_string = ''
    tmp_string += '=========소비자 메뉴얼==========\n'
    tmp_string += '0. 메뉴 보기\n'
    tmp_string += '1. 음료수 목록 보기\n'
    tmp_string += '2. 음료수 구입하기\n'
    tmp_string += '3. 금액 투입하기\n'
    tmp_string += '4. 투입 금액 반환받기\n'
    tmp_string += '5. 소비자 모드 나가기(exit)'
    return tmp_string

#음료수 목록 확인
def process_drink_list():
    tmp_string = '========음료수 목록========='
    for index, drink in enumerate(settings.DRINK_STOCK):
        drink_sold_out = drink['cost']
        if drink['stock'] == 0:
            drink_sold_out = 'X'
        
        tmp_string += f'\n{index}. {drink["name"]}\t: {drink_sold_out}'
    tmp_string += '\n============================'

    return tmp_string

#음료수 구매하기    
def process_change(cost):
    total_money = 0
    for money in settings.SALES:
        settings.SALES[money] += settings.TEMP_SALES[money]
        total_money += money * settings.TEMP_SALES[money]
        settings.TEMP_SALES[money] = 0
        print(settings.TEMP_SALES[money])
    change = total_money - cost
    settings.CHANGE -= change
    return change

def process_buy(drink):
    total_money = 0
    for money in settings.TEMP_SALES:
        total_money += money * settings.TEMP_SALES[money]
    if drink['stock'] == 0:
        return invalid_input_type['invalid_sold_out']
    if drink['cost'] > total_money:
        return invalid_input_type['invalid_money_range']
    else:
        change = process_change(drink['cost'])
        return f'{drink["index"]}번 {drink["name"]}을 구매하셨습니다. 잔돈 : {change}원'
        
def transport_drink_name_input(input_value):
    if input_value.isnumeric() is True:
        if int(input_value) >= settings.DRINK_POCKET_SIZE or int(input_value) < 0:
            return 'invalid_drink_range'
        else:
            return {'index': int(input_value), **settings.DRINK_STOCK[int(input_value)]}
    else:
        if input_value not in settings.DRINK_KINDS:
            return 'invalid_drink'
        else:
            return_value = []
            for index, drink in enumerate(settings.DRINK_STOCK):
                if drink['name'] == input_value:
                    return_value.append({'index': index, **drink})
            return return_value[0] if len(return_value) == 1 else return_value

def transport_duplicate_drink_select_input(input_value, drinks):
    if input_value.isnumeric() is False:
        return 'invalid_int_type'
    else:
        for drink in drinks:
            if drink['index'] == int(input_value):
                return drink
        return 'invalid_drink'

def process_duplicate_drink_select(drinks):
    for index, drink in enumerate(settings.DRINK_STOCK):
        drink_sold_out = drink['cost']
        if drink['stock'] == 0:
            drink_sold_out = 'X'
        print(f'{index}. {drink["name"]}\t: {drink_sold_out}')
    select_drink = custom_input('동일한 음료수가 들어있는 칸이 존재합니다. 칸 번호를 입력해주세요.',
                                transport_duplicate_drink_select_input,
                                drinks=drinks)
    if type(select_drink) == str:
        print(invalid_input_type[select_drink])
        return process_duplicate_drink_select(drinks)
    else:
        return select_drink

def process_drink_select():
    drink = custom_input('음료수를 선택해주세요.(번호 or 이름)', transport_drink_name_input)
    if type(drink) == str:
        print(invalid_input_type[drink])
        return process_drink_select()
    elif type(drink) == dict:
        return drink
    elif type(drink) == list:
        return process_duplicate_drink_select(drink)

def process_drink_buy():
    print(process_drink_list())
    drink = process_drink_select()
    return process_buy(drink)

# 금액 투입하기
def process_money_input():
    print(show_input_money())
    money_input()
    return show_input_money()
    
def show_input_money():
    tmp_string = '========투입된 금액=========\n'
    total_money = 0
    for money in settings.TEMP_SALES:
        tmp_string += f'{money}\t: {settings.TEMP_SALES[money]}개\n'
        total_money += money * settings.TEMP_SALES[money]
    tmp_string += f'총\t: {total_money}원\n'
    tmp_string += '============================\n'
    return tmp_string

def money_input():
    total_money = 0
    for money in settings.TEMP_SALES:
        total_money += money * settings.TEMP_SALES[money]
    num = 0
    lst = list(settings.TEMP_SALES.keys())
    money = lst[num]
    while money:
        cnt = custom_input(f'투입하실 {money}원의 수량을 입력해주세요.(현재 총 금액 : {total_money})',
                           transport_not_negative_number)
        if type(cnt) is int:
            settings.TEMP_SALES[money] += cnt
            total_money += money * cnt
            if money == lst[-1]:
                break
            num += 1
            money = lst[num]
        else:
            print(invalid_input_type[cnt])
        
# 투입한 금액 반환받기
def process_money_return():
    total_money = 0
    for money in settings.TEMP_SALES:
        total_money += money * settings.TEMP_SALES[money]
        settings.TEMP_SALES[money] = 0
    tmp_string = f'투입하신 {total_money}원이 반환되었습니다.'
    return tmp_string

def transport_manual_input(input_value):
    for process_name, valid_input in consumer_manual_mapping.items():
        if input_value in valid_input:
            return process_name
    return 'invalid_manual_command'

def manual_input(prompt):
    print(string_before_prompt)
    process_name = custom_input(prompt, transport_manual_input)

    if process_name == 'invalid_manual_command':
        print(invalid_input_type[process_name])
        process_name = manual_input(prompt)
    return process_name

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def process_consumer():
    global string_before_prompt
    menu_string = process_view_menu()
    string_before_prompt = menu_string
    process_name = manual_input('소비자 메뉴를 선택해주세요.')
    while process_name != 'process_exit':
        string_before_prompt = ''
        set_before_prompt = globals()[process_name]()
        if set_before_prompt is not None:
            string_before_prompt = set_before_prompt
        else:
            string_before_prompt = menu_string
        clearConsole()
        process_name = manual_input('소비자 메뉴를 선택해주세요.')
