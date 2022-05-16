from crypt import methods
from http.client import responses
from flask import Flask
from service.email_service import EmailService

from service.tauron_scrape_service import TauronService


app = Flask(__name__)


@app.route('/api/v1/send-bill-notification')
def send_bill_notification():
    bill_service = TauronService()
    email_service = EmailService()
    bill = bill_service.get_next_bill()
    email_service.send_bill_notification(bill)
    return '<b>Email sent to destination</b>'


app.run()

if __name__ == "__main__":
    send_bill_notification()
