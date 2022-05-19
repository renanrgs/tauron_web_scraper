"""
test module for bill service
"""
from datetime import datetime

from service.bill_service import BillService

service = BillService()


def test_get_next_bill() -> None:
    """
    Test method get_next_bill
    :return: None
    """
    bill = service.get_next_bill()
    assert bill.amount
    assert float(bill.amount)
    assert bill.due_date


def test_next_bill_value() -> None:
    """
    Tests method that return next bill value
    :return: None
    """
    amount = service.next_bill_value()
    assert amount


def test_get_last_reading() -> None:
    """
    Tests get-last_reading method
    :return: None
    """
    last_reading = service.get_last_reading()
    assert int(last_reading)


def test_is_urgent_bill() -> None:
    """
    Test method is_urgent_bill
    :return: None
    """
    next_due_date = service.next_due_bill_datetime()
    left_days = (datetime.now() - next_due_date).days
    expected = left_days > -5
    assert service.is_urgent_bill() == expected
