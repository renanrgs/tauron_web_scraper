import requests
from util.singleton import singleton
from requests.adapters import HTTPAdapter
from http_adapter.ssl3_http_adapter import Ssl3HttpAdapter
from config.env_enum import Environment
from soup.html_parser import HtmlParser
from util.formatter import remove_non_digits
from datetime import datetime


@singleton
class TauronService:
    def __init__(self):
        self.dashboard_response, self.session = Session().login()
        self.parser = HtmlParser(self.dashboard_response.content)

    def _navigate(self, url):
        self.session.mount(url, Ssl3HttpAdapter())
        return self.session.get(url)

    def get_total_debt(self):
        content = self.dashboard_response.content
        return self.parser.get_total_debt(content)

    def get_last_reading(self):
        return self.parser.get_last_reading(self.dashboard_response.content)

    def _next_bill_date_time(self):
        content = self.dashboard_response.content
        date = self.parser.get_next_bill(content).strip()
        date = remove_non_digits(date)
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


@singleton
class Session:

    def __init__(self, adapter: HTTPAdapter = Ssl3HttpAdapter()):
        self.url = 'https://logowanie.tauron.pl/login'
        self.adapter = adapter
        self.session = requests.Session()
        self.session.mount(self.url, adapter=self.adapter)

    def login(self):
        user_data = {'username': Environment.TAURON_USER.value, 'password': Environment.TAURON_PASSWORD.value}
        response = self.session.post(self.url, cookies={'PHPSESSID': ''}, data=user_data, allow_redirects=False)
        response = self._manage_redirects(self.session, response)
        return response, self.session

    def _manage_redirects(self, session, response):
        while response.next:
            session.mount(response.next.url, self.adapter)
            response = session.get(response.next.url, allow_redirects=False)
        return response


if __name__ == '__main__':
    service = TauronService()
    print(service.get_total_debt())
    print(service.get_last_reading())
    print(service.is_urgent_bill())
    print(service.next_due_bill_date())
    print(service.next_bill_value())
