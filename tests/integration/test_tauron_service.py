from service.tauron_scrape_service import TauronService

service = TauronService()


def test_get_next_bill():
    bill = service.get_next_bill()
    assert bill.amount
    assert bill.due_date


def test_next_bill_value():
    amount = service.next_bill_value()
    assert amount
