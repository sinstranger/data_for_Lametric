import os

HOST = '0.0.0.0'

PORT = 8088


if os.environ.get('TEST_LAM'):
    FINOLOG_API_KEY = 'dkv6uaV7ON2fEThB18318e4d73b5a02e35a526cc0fa39defnzLed5sqZyV775ua'

    FINOLOG_BIZ_SETTINGS = [
        {'biz_id': 28618, 'icon': 18348, 'goal_start': 0, 'goal_end': 26000, 'unit': 'k', 'duration': 30},  # Beer
        {'biz_id': 28615, 'icon': 33859, 'goal_start': 0, 'goal_end': 3500, 'unit': 'k', 'duration': 30}]  # Develop

else:
    FINOLOG_API_KEY = os.environ.get('API_KEY')
    BIZ1 = int(os.environ.get('BIZ1'))
    BIZ2 = int(os.environ.get('BIZ1'))

    FINOLOG_BIZ_SETTINGS = [
        {'biz_id': BIZ1, 'icon': 18348, 'goal_start': 0, 'goal_end': 26000, 'unit': 'k', 'duration': 50},  # Beer
        {'biz_id': BIZ2, 'icon': 33859, 'goal_start': 0, 'goal_end': 3500, 'unit': 'k', 'duration': 50}]  # Develop
