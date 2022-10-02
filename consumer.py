import settings

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
    'invalid_positive_number': '0 초과 양수만 입력해주세요.',
    'invalid_drink_range': '유효하지 않는 음료수 번호입니다.',
    'invalid_sole_out' : '품절된 음료수입니다.',
    'invalid_money_range' : '잔액이 부족합니다.',
}

def transport_not_negative_number(input_value):
    if input_value.isnumeric() is not True:
        return 'invalid_int_type'
    elif int(input_value) < 0:
        return 'invalid_positive_number'
    return int(input_value)

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
    print('=========소비자 메뉴얼==========')
    print('0. 메뉴 보기')
    print('1. 음료수 목록 보기')
    print('2. 음료수 구입하기')
    print('3. 금액 투입하기')
    print('4. 투입 금액 반환받기')
    print('5. 소비자 모드 나가기(exit)')

#음료수 목록 확인
def process_drink_list():
    print('========음료수 목록=========')
    for index, drink in enumerate(settings.DRINK_STOCK):
        drink_sold_out = drink['cost']
        if drink['stock'] == 0:
            drink_sold_out = 'X'
        print(f'{index}. {drink["name"]}\t: {drink_sold_out}')
    print('============================')

#음료수 구매하기    
def process_change(cost):
    total_money = 0
    for money in settings.SALES:
        settings.SALES[money] += settings.TEMP_SALES[money]
        total_money += money * settings.TEMP_SALES[money]
        settings.TEMP_SALES[money] = 0
    change = total_money - cost
    settings.CHANGE -= change

def process_buy(drink):
    total_money = 0
    for money in settings.TEMP_SALES:
        total_money += money * settings.TEMP_SALES[money]
    if drink['cost'] > total_money:
        print(invalid_input_type['invalid_money_range'])
    else:
        print(f'{drink["index"]}번 {drink["name"]}을 구매하셨습니다. 잔돈 : {total_money - drink["cost"]}원')
        process_change(drink['cost'])
        
def transport_drink_name_input(input_value):
    if input_value.isnumeric() is True:
        if int(input_value) >= settings.DRINK_POCKET_SIZE and int(input_value) < 0:
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
    process_drink_list()
    drink = process_drink_select()
    process_buy(drink)

# 금액 투입하기
def process_money_input():
    total_money = show_input_money()
    money_input(total_money)
    show_input_money()
    
def show_input_money():
    print('========투입된 금액=========')
    total_money = 0
    for money in settings.TEMP_SALES:
        print(f'{money}\t: {settings.TEMP_SALES[money]}개')
        total_money += money * settings.TEMP_SALES[money]
    print(f'총\t  {total_money}원')
    print('============================')
    return total_money

def money_input(total_money):
    total_money = total_money
    for money in settings.TEMP_SALES:
        cnt = custom_input(f'투입하실 {money}원의 수량을 입력해주세요.(현재 총 금액 : {total_money})',
                           transport_positive_number)
        settings.TEMP_SALES[money] = cnt
        print(cnt)
        total_money += money * settings.TEMP_SALES[money]
        
# 투입한 금액 반환받기
def process_money_return():
    total_money = 0
    for money in settings.TEMP_SALES:
        total_money += money * settings.TEMP_SALES[money]
        settings.TEMP_SALES[money] = 0
    print(f'투입하신 {total_money}원이 반환되었습니다.')

def transport_manual_input(input_value):
    for process_name, valid_input in consumer_manual_mapping.items():
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

def process_consumer():
    process_name = manual_input('소비자 메뉴를 선택해주세요.')
    if process_name != 'process_exit':
        globals()[process_name]()