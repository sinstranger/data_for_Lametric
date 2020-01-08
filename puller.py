import requests
import json

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

    def get_account_API_url(self) -> str:
        return '{}{}/account'.format(self.FINOLOG_API_BIZ_URL, self.biz_id)

    def get_account_response(self):
        return requests.get(self.get_account_API_url(), headers={'Api-Token': settings.FINOLOG_API_KEY})

    def get_account_summary(self):
        summary = 0
        for account in self.get_account_response().json():
            try:
                summary += account['summary'][0]['balance']
            except IndexError:
                pass
        return int(summary / 1000)

    def get_lametric_frame(self):
        return dict(icon=self.icon, goalData=self._get_goal_data_for_lametric_frame(), duration=self.duration)

    def _get_goal_data_for_lametric_frame(self):
        return dict(start=self.goal_start, current=self.get_account_summary(), end=self.goal_end, unit=self.unit)


class FramesCatalog:

    biz_bunch = [BaseFinologBiz(**kwargs) for kwargs in settings.FINOLOG_BIZ_SETTINGS]

    def get_frames_data(self):
        frames = [biz.get_lametric_frame() for biz in self.biz_bunch]
        return dict(frames=frames)

    def get_frames_json(self):
        frames_data = self.get_frames_data()
        json_data = json.dumps(frames_data)
        return json_data
