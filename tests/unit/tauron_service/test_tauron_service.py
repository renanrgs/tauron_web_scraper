
from datetime import datetime
from data_model.bill import Bill
from service.tauron_scrape_service import TauronService


def test_is_urgent_bill():
    bill = Bill(150.0, '23-05-2022')
    is_urgent = TauronService.is_urgent_bill_str(bill)
    assert is_urgent
