import requests
import json
from time import strptime
from datetime import datetime

import settings


class BaseFinologBiz:

    FINOLOG_API_BIZ_URL = 'https://api.finolog.ru/v1/biz/'

    def __init__(self, **kwargs):
        for kwarg in kwargs.keys():
            self.__setattr__(kwarg, kwargs[kwarg])

    def __str__(self):
        return 'Finolog biz object with id {}'.format(self.biz_id)

    def __repr__(self):
        return self.__str__()

    def get_biz_accounts_API_url(self) -> str:
        """ Return link https://api.finolog.ru/v1/biz/{biz_id}/account """
        return '{}{}/account'.format(self.FINOLOG_API_BIZ_URL, self.biz_id)

    def get_biz_transactions_API_url(self) -> str:
        """ Return link https://api.finolog.ru/v1/biz/{biz_id}/tramsaction """
        return '{}{}/transaction'.format(self.FINOLOG_API_BIZ_URL, self.biz_id)

    def get_accounts_response(self):
        return requests.get(self.get_biz_accounts_API_url(), headers={'Api-Token': settings.FINOLOG_API_KEY})

    def get_transactions_response(self):
        return requests.get(self.get_biz_transactions_API_url(), headers={'Api-Token': settings.FINOLOG_API_KEY})


class FinologBiz(BaseFinologBiz):

    """
    Class represents finolog.ru business instance.
    Methods of class allow to build lametric frames form finolog API's requests.

    Frames for each business:
    1. Summary - sum from all accounts of biz;
    2. Income goal - goal frames with income's sum on current year;
    3. Income chart - chart frame with income by months.
    """
    MONTHS_NUMBERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

    def get_summary_frame(self):
        """ Example {"icon": "794", "text": "Hello!"} """
        text = '{} K'.format(self._get_account_summary())
        return dict(icon=self.icon, text=text, duration=self.duration)

    def get_income_goal_frame(self):
        """ Example  {"icon": "22835", "goalData": {"start": 0, "current": 6000, "end": 10000, "unit": "MI"}} """
        current = self._get_income_transactions_sum_in_current_year()
        result = {"icon": self.icon, "duration": self.duration, "goalData": {
            "start": self.goal_start, "current": current, "end": self.goal_end, "unit": self.unit}}
        return result

    def get_income_chart_frame(self):
        """ {"chartData": [1, 10, 15, 20, 6, 9, 11, 16, 22, 24]} """
        chartData = []
        values = self._get_income_transactions_sum_by_month_in_current_year()
        for month in self.MONTHS_NUMBERS:
            chartData.append(values[month])
        return {'chartData': chartData}

    def get_lametric_frames(self):
        return self.get_summary_frame(), self.get_income_goal_frame(), self.get_income_chart_frame(),

    def _get_account_summary(self) -> int:  # in thousands
        summary = 0
        for account in self.get_accounts_response().json():
            try:
                summary += account['summary'][0]['balance']
            except IndexError:
                pass
        return int(summary / 1000)

    def _get_income_transactions_sum_in_current_year(self) -> int:  # in thousands
        summ = 0
        for value in self._get_income_transactions_sum_by_month_in_current_year().values():
            summ += value
        return int(summ / 1000)

    def _get_income_transactions_sum_by_month_in_current_year(self) -> dict:
        transactions_by_month = {}
        for n in self.MONTHS_NUMBERS:
            transactions_by_month[n] = 0
        current_year = datetime.today().year

        for transaction in self.get_transactions_response().json():
            value, date = transaction['value'], datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
            if date.year == current_year and value > 0:
                transactions_by_month[date.month] += value
        return transactions_by_month


class FramesCatalog:

    biz_bunch = [FinologBiz(**kwargs) for kwargs in settings.FINOLOG_BIZ_SETTINGS]

    def get_frames_data(self):
        frames = [frame for sublist in [biz.get_lametric_frames() for biz in self.biz_bunch] for frame in sublist]
        return dict(frames=frames)

    def get_frames_json(self):
        frames_data = self.get_frames_data()
        json_data = json.dumps(frames_data)
        return json_data
