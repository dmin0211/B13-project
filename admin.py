mocking_drink = {
    '파워에이드': 13,
    '케토레이': 10,
}

mocking_chane = 10000

mocking_sales = {
    100: 5,
    500: 4,
    1000: 3,
    5000: 0,
}

admin_manual_mapping = {
    'process_view_menu': ['0', '메뉴 보기'],
    'process_drink_stock': ['1', '음료수 수량 확인'],
    'process_drink_replenishment': ['2', '음료수 채워 넣기'],
    'process_change_replenishment': ['3', '거스름돈 채워 넣기'],
    'process_sales_view': ['4', '매출 보기'],
    'process_sales_settlement': ['5', '매출 정산'],
    'process_exit': ['6', '관리자 모드 나가기', 'exit', '관리자 모드 나가기(exit)'],
}


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
    print("=========재고 확인==========")
    for drink, stock in mocking_drink.items():
        print('[' + drink + ']\t: ', stock)
    print("============================")


# 음료수 채워 넣기
def process_drink_replenishment():
    print('drink replenishment')


# 거스름돈 채워 넣기
def process_change_replenishment():
    print('change replenishment')


# 매출 보기
def process_sales_view():
    total_sales = 0
    print("=========매출 보기==========")
    for unit, count in mocking_sales.items():
        total_sales += unit * count
        print('[', unit, '원권]\t: ', count)
    print('전체 매출 : ', total_sales)
    print("============================")


# 매출 정산
def process_sales_settlement():
    print('sales settlement')


def check_invalid_manual(input_value):
    for process_name, valid_input in admin_manual_mapping.items():
        if input_value in valid_input:
            return process_name
    return False


def manual_input(prompt):
    process_view_menu()
    input_value = input(prompt + ' : ')
    process_name = check_invalid_manual(input_value)
    if process_name is False:
        print('Invalid Command. Please Try Again.')
        process_name = manual_input(prompt)
    elif process_name == 'process_view_menu':
        process_name = manual_input(prompt)
    return process_name


def process_admin():
    process_name = manual_input("관리자 권한 메뉴를 선택해주세요.")
    if process_name != 'process_exit':
        globals()[process_name]()
