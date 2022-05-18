
from datetime import datetime
from data_model.bill import Bill
from service.bill_service import BillService


def test_is_urgent_bill():
    bill = Bill(150.0, '23-05-2022')
    is_urgent = BillService.is_urgent(bill)
    assert is_urgent
