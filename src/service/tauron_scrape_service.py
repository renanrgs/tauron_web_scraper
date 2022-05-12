from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from http_adapter.ssl3_http_adapter import Ssl3HttpAdapter
from config.env_enum import Environment
from soup.html_parser import HtmlParser
from util.formatter import Util
from datetime import datetime


class Session(ABC):

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_http_adapter(self):
        pass


class TauronService:
    def __init__(self, session: Session):
        self.dashboard_response, self.session = session.login()
        self.parser = HtmlParser(self.dashboard_response.content)
        self.http_adapter = session.get_http_adapter()

    def _navigate(self, url):
        self.session.mount(url, self.http_adapter)
        return self.session.get(url)

    def get_total_debt(self):
        content = self.dashboard_response.content
        return self.parser.get_total_debt(content)

    def get_last_reading(self):
        return self.parser.get_last_reading(self.dashboard_response.content)

    def _next_bill_date_time(self):
        content = self.dashboard_response.content
        date = self.parser.get_next_bill(content).strip()
        date = Util.remove_non_digits(date)
        date = datetime.strptime(date, '%d%m%Y')

        return date

    def is_urgent_bill(self):
        now = datetime.now()
        date = self._next_bill_date_time()
        days_left = (now - date).days
        return True if days_left > -5 else False

    def next_due_bill_date(self):
        return self._next_bill_date_time().strftime('%d-%m-%Y')

    def next_bill_value(self):
        content = self.dashboard_response.content
        return self.parser.get_next_bill_value(content).strip()


class TauronSession(Session):

    def __init__(self, adapter: HTTPAdapter = Ssl3HttpAdapter()):
        self.url = 'https://logowanie.tauron.pl/login'
        self.adapter = adapter
        self.session = requests.Session()
        self.session.mount(self.url, adapter=self.adapter)

    def login(self):
        user_data = {'username': Environment.TAURON_USER.value,
                     'password': Environment.TAURON_PASSWORD.value}
        response = self.session.post(
            self.url, cookies={'PHPSESSID': ''}, data=user_data, allow_redirects=False)
        response = self._manage_redirects(self.session, response)
        return response, self.session

    def get_http_adapter(self):
        return self.adapter

    def _manage_redirects(self, session, response):
        while response.next:
            session.mount(response.next.url, self.adapter)
            response = session.get(response.next.url, allow_redirects=False)
        return response


if __name__ == '__main__':
    service = TauronService(session=TauronSession())
    print(service.get_total_debt())
    print(service.get_last_reading())
    print(service.is_urgent_bill())
    print(service.next_due_bill_date())
    print(service.next_bill_value())
