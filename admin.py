import settings

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
    'invalid_drink_range': '유효하지 않는 음료수 번호입니다.',
    'invalid_drink_max_stock': '채울 수 있는 음료의 최대치는 10개입니다.',
}


def transport_positive_number(input_value):
    if input_value.isnumeric() is not True:
        return 'invalid_int_type'
    elif int(input_value) <= 0:
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
    print('=========관리자 메뉴얼==========')
    print('0. 메뉴 보기')
    print('1. 음료수 수량 확인')
    print('2. 음료수 채워 넣기')
    print('3. 거스름돈 채워 넣기')
    print('4. 매출 보기')
    print('5. 매출 정산')
    print('6. 관리자 모드 나가기(exit)')


# 음료수 재고 확인
def process_drink_stock():
    print('========음료수 재고=========')
    for index, drink in enumerate(settings.DRINK_STOCK):
        print(f'{index}. {drink["name"]}\t: {drink["stock"]}')
    print('============================')


# 음료수 채워 넣기
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
        return drink
    elif type(drink) == list:
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
    process_drink_stock()
    drink = process_drink_select()
    process_replenishment_after_select_drink(drink)


# 거스름돈 채워 넣기
def process_change_replenishment():
    replenishment_amount = custom_input(f'보충할 거스름돈량을 입력해주세요.(현재 거스름돈 : {settings.CHANGE})',
                                        transport_positive_number)
    settings.CHANGE += replenishment_amount


# 매출 보기
def process_sales_view():
    total_sales = 0
    print('=========매출 보기==========')
    for unit, count in settings.SALES.items():
        total_sales += unit * count
        print('[', unit, '원권]\t: ', count)
    print('전체 매출 : ', total_sales)
    print('============================')


# 매출 정산
def process_sales_settlement():
    total_sale = 0
    for unit, count in settings.SALES.items():
        settings.SALES[unit] = 0
        total_sale += unit * count
    print(f'매출 {total_sale}을 정산했습니다.')


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


def process_admin():
    process_name = manual_input('관리자 권한 메뉴를 선택해주세요.')
    if process_name != 'process_exit':
        globals()[process_name]()
