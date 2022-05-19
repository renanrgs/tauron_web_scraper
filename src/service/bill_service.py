"""
service module for bill operations
"""
from datetime import datetime

from data_model.bill import Bill
from session.session import TauronSession
from soup.html_parser import HtmlParser
from util.formatter import Util


class BillService:
    """
    Service class to perform operations over bills
    """
    def __init__(self, session=TauronSession()):
        self.dashboard_response, self.session = session.login()
        self.parser = HtmlParser(self.dashboard_response.content)
        self.http_adapter = session.http_adapter

    def _navigate(self, url):
        self.session.mount(url, self.http_adapter)
        return self.session.get(url)

    def get_total_debt(self):
        """
        Returns total debt
        :return: total debt of electricity bill
        """
        content = self.dashboard_response.content
        return self.parser.get_total_debt(content)

    def get_last_reading(self):
        """
        Get the last consumption meter value
        :return: last consumption value
        """
        return self.parser.get_last_reading(self.dashboard_response.content)

    def next_due_bill_datetime(self):
        """
        Due date of the next bill
        :return: datetime containing the next due date
        """
        content = self.dashboard_response.content
        date = self.parser.get_next_bill(content).strip()
        date = Util.remove_non_digits(date)
        date = datetime.strptime(date, '%d%m%Y')

        return date

    def is_urgent_bill(self):
        """
        Checks if a bill is urgent. In that case,
        if 5 days or less is left for due date
        :return: true or false
        """
        now = datetime.now()
        date = self.next_due_bill_datetime()
        days_left = (now - date).days
        return days_left > -5

    def due_bill_date_str(self, date_format='%d-%m-%Y'):
        """
        Returns the next bill due date
        :param date_format: date pattern
        :return: a string containing the next due date
        """
        return self.next_due_bill_datetime().strftime(date_format)

    def next_bill_value(self):
        """
        Returns the next bill value
        :return: next bill amount
        """
        content = self.dashboard_response.content
        float_value = self.parser.get_next_bill_value(content)\
            .replace(',', '.')\
            .replace('zł', '')\
            .strip()
        return float_value

    def get_next_bill(self) -> Bill:
        """
        Returns next bill
        :return: next bill
        """
        amount = self.next_bill_value()
        due_date = self.due_bill_date_str()
        return Bill(amount, due_date)
