CHANGE = 10 ** 6
MAX_STOCK = 10
DRINK_POCKET_SIZE = 10
DRINK_KINDS = ['파워에이드', '게토레이', '포카리스웨트', '하늘보리', '솔의눈', '환타', '코카콜라', '칠성사이다', '펩시콜라']
DRINK_STOCK = [
    {'name': DRINK_KINDS[0], 'stock': 0, 'cost': 800},
    {'name': DRINK_KINDS[1], 'stock': 2, 'cost': 900},
    {'name': DRINK_KINDS[2], 'stock': 4, 'cost': 300},
    {'name': DRINK_KINDS[3], 'stock': 6, 'cost': 2100},
    {'name': DRINK_KINDS[4], 'stock': 7, 'cost': 500},
    {'name': DRINK_KINDS[5], 'stock': 8, 'cost': 1200},
    {'name': DRINK_KINDS[6], 'stock': 8, 'cost': 900},
    {'name': DRINK_KINDS[7], 'stock': 8, 'cost': 600},
    {'name': DRINK_KINDS[8], 'stock': 8, 'cost': 1800},
    {'name': DRINK_KINDS[8], 'stock': 10, 'cost': 1800},
]
SALES = {
    100: 5,
    500: 4,
    1000: 3,
    5000: 0,
}
TEMP_SALES = {
    100: 3,
    500: 0,
    1000: 0,
    5000: 0,
}
