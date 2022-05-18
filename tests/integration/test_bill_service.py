from service.bill_service import BillService

service = BillService()


def test_get_next_bill():
    bill = service.get_next_bill()
    assert bill.amount
    assert float(bill.amount)
    assert bill.due_date


def test_next_bill_value():
    amount = service.next_bill_value()
    assert amount


def test_get_last_reading():
    last_reading = service.get_last_reading()
    assert int(last_reading)
