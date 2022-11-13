import settings
import os

string_before_prompt = ''


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


admin_manual_mapping = {
    'process_view_menu': ['0', '메뉴 보기'],
    'process_drink_stock': ['1', '음료수 수량 확인'],
    'process_drink_replenishment': ['2', '음료수 채워 넣기'],
    'process_change_replenishment': ['3', '거스름돈 채워 넣기'],
    'process_sales_view': ['4', '매출 보기'],
    'process_sales_settlement': ['5', '매출 정산'],
    'process_exit': ['6', '관리자 모드 나가기', 'exit', '관리자 모드 나가기(exit)'],
}

invalid_input_type = {
    'invalid_manual_command': '존재하지 않는 명령어입니다.',
    'invalid_int_type': '숫자만 입력해주세요.',
    'invalid_drink': '존재하지 않는 음료수입니다.',
    'invalid_positive_number': '0 초과 양수만 입력해주세요.',
    'invalid_drink_max_stock': '채울 수 있는 음료의 최대치는 10개입니다.',
    'invalid_drink_replenishment': '음료수가 최대수량입니다.',
}


def transport_positive_number(input_value):
    if input_value[0] == '-' and input_value[1:].isnumeric() is True:
        return 'invalid_positive_number'
    elif input_value.isnumeric() is not True:
        return 'invalid_int_type'
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
    tmp_string = ''
    tmp_string += '=========관리자 메뉴얼==========\n'
    tmp_string += '0. 메뉴 보기\n'
    tmp_string += '1. 음료수 수량 확인\n'
    tmp_string += '2. 음료수 채워 넣기\n'
    tmp_string += '3. 거스름돈 채워 넣기\n'
    tmp_string += '4. 매출 보기\n'
    tmp_string += '5. 매출 정산\n'
    tmp_string += '6. 관리자 모드 나가기(exit)'
    return tmp_string


# 음료수 재고 확인
def process_drink_stock():
    tmp_string = '========음료수 재고========='
    for index, drink in enumerate(settings.DRINK_STOCK):
        tmp_string += f'\n{index}. {drink["name"]}\t: {drink["stock"]}'
    tmp_string += '\n============================'

    return tmp_string


# 음료수 채워 넣기
def transport_drink_name_input(input_value):
    if input_value.isnumeric() is True:
        if int(input_value) >= settings.DRINK_POCKET_SIZE or int(input_value) < 0:
            return 'invalid_drink'
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
    for drink in drinks:
        print(f'{drink["index"]}. {drink["name"]}\t: {drink["stock"]}')
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
        if drink['stock'] == settings.MAX_STOCK:
            print(invalid_input_type['invalid_drink_replenishment'])
            return process_drink_select()
        else:
            return drink
    elif type(drink) == list:
        is_max_stock = True
        for item in drink:
            is_max_stock = is_max_stock and item['stock'] == settings.MAX_STOCK
        if is_max_stock is True:
            print(invalid_input_type['invalid_drink_replenishment'])
            return process_drink_select()
        else:
            return process_duplicate_drink_select(drink)


def transport_drink_replenishment_amount_input(input_value, current_drink_stock):
    transport_positive_value = transport_positive_number(input_value)
    if type(transport_positive_value) == int and current_drink_stock + transport_positive_value > settings.MAX_STOCK:
        return 'invalid_drink_max_stock'
    return transport_positive_value


def process_replenishment_after_select_drink(drink):
    replenishment_amount = custom_input(
        f'[{drink["index"]}. {drink["name"]}] 보충할 수량을 입력해주세요.(현재 수량 : {drink["stock"]})',
        transport_drink_replenishment_amount_input,
        current_drink_stock=drink['stock']
    )
    if type(replenishment_amount) == str:
        print(invalid_input_type[replenishment_amount])
        process_replenishment_after_select_drink(drink)
    else:
        settings.DRINK_STOCK[drink['index']]['stock'] += replenishment_amount


def process_drink_replenishment():
    print(process_drink_stock())
    total_stock = 0
    for index, drink in enumerate(settings.DRINK_STOCK):
        total_stock += int(drink['stock'])
    if (total_stock >= settings.MAX_STOCK * settings.DRINK_POCKET_SIZE):
        return invalid_input_type['invalid_drink_replenishment']
    drink = process_drink_select()
    process_replenishment_after_select_drink(drink)


# 거스름돈 채워 넣기
def process_change_replenishment():
    money = list(settings.CHANGE.keys())
    money_index = 0
    current_change_string = '========거스름돈 수량========='
    for unit, count in settings.CHANGE.items():
        current_change_string += f'\n[{unit} 원권]\t: {str(count)}'
    current_change_string += '\n=============================='

    print(current_change_string)
    while money_index < len(money):
        replenishment_amount = custom_input(f'보충할 {money[money_index]} 원권 수량을 입력해주세요.',
                                            transport_positive_number)
        if type(replenishment_amount) == str:
            print(invalid_input_type[replenishment_amount])
        else:
            settings.CHANGE[money[money_index]] += replenishment_amount
            money_index += 1

    tmp_string = '========거스름돈 수량========='
    for unit, count in settings.CHANGE.items():
        tmp_string += f'\n[{unit} 원권]\t: {str(count)}'
    tmp_string += '\n=============================='
    return tmp_string


# 매출 보기
def process_sales_view():
    total_sales = 0
    tmp_string = '=========매출 보기=========='
    for unit, count in settings.SALES.items():
        total_sales += unit * count
        tmp_string += f'\n[{unit} 원권]\t: {str(count)}'
    tmp_string += f'\n전체 매출 : {str(total_sales)}'
    tmp_string += '\n============================'
    return tmp_string


# 매출 정산
def process_sales_settlement():
    total_sale = 0
    for unit, count in settings.SALES.items():
        settings.SALES[unit] = 0
        total_sale += unit * count
    tmp_string = f'매출 {total_sale}을 정산했습니다.'
    return tmp_string


def transport_manual_input(input_value):
    for process_name, valid_input in admin_manual_mapping.items():
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


def process_admin():
    global string_before_prompt
    menu_string = process_view_menu()
    string_before_prompt = menu_string
    process_name = manual_input('관리자 권한 메뉴를 선택해주세요.')
    while process_name != 'process_exit':
        string_before_prompt = ''
        set_before_prompt = globals()[process_name]()
        if set_before_prompt is not None:
            string_before_prompt = set_before_prompt
        else:
            string_before_prompt = menu_string
        clear_console()
        process_name = manual_input('관리자 권한 메뉴를 선택해주세요.')
