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
    'invalid_manual_command': '존재하지 않는 명령어입니다. 다시 입력해주세요.',
    'invalid_drink': '존재하지 않는 음료수입니다. 다시 입력해주세요.',
    'invalid_drink_max_stock': '채울 수 있는 음료의 최대치는 10개입니다.',
    'invalid_drink_replenishment_type': '음료수 보충은 숫자만 입력 가능합니다.',
}


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
    print("=========관리자 메뉴얼==========")
    print("0. 메뉴 보기")
    print("1. 음료수 수량 확인")
    print("2. 음료수 채워 넣기")
    print("3. 거스름돈 채워 넣기")
    print("4. 매출 보기")
    print("5. 매출 정산")
    print("6. 관리자 모드 나가기(exit)")


# 음료수 재고 확인
def process_drink_stock():
    print("========음료수 재고=========")
    for drink, stock in settings.DRINK_STOCK.items():
        print('[' + drink + ']\t: ', stock)
    print("============================")


# 음료수 채워 넣기
def transport_drink_name_input(input_value):
    if input_value in settings.DRINK_STOCK.keys():
        return input_value
    return 'invalid_drink'


def transport_drink_replenishment_input(input_value, current_drink_stock):
    if input_value.isnumeric() is not True:
        return 'invalid_drink_replenishment_type'
    if current_drink_stock + input_value > settings.MAX_STOCK:
        return 'invalid_drink_max_stock'
    return input_value


def process_drink_replenishment():
    process_drink_stock()
    drink_name = custom_input("음료수 이름을 입력해주세요.", transport_drink_name_input)
    if drink_name == 'invalid_drink':
        print(invalid_input_type[drink_name])
        process_drink_replenishment()
    else:
        replenishment = custom_input(f'[{drink_name}] 보충할 수량을 입력해주세요.(현재 수량 : {settings.DRINK_STOCK[drink_name]})',
                                     transport_drink_replenishment_input,
                                     current_drink_stock=settings.DRINK_STOCK[drink_name])
        if replenishment == 'invalid_drink_replenishment_type' or replenishment == 'invalid_drink_max_stock':
            print(invalid_input_type[replenishment])
        # else:
    # settings.DRINK_STOCK[drink_name] += replenishment


# 거스름돈 채워 넣기
def process_change_replenishment():
    print('change replenishment')


# 매출 보기
def process_sales_view():
    total_sales = 0
    print("=========매출 보기==========")
    for unit, count in settings.SALES.items():
        total_sales += unit * count
        print('[', unit, '원권]\t: ', count)
    print('전체 매출 : ', total_sales)
    print("============================")


# 매출 정산
def process_sales_settlement():
    print('sales settlement')


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
    process_name = manual_input("관리자 권한 메뉴를 선택해주세요.")
    if process_name != 'process_exit':
        globals()[process_name]()


process_admin()
