from dataclasses import asdict
from flask import Flask, jsonify

from service.tauron_scrape_service import TauronService

service = TauronService()

app = Flask(__name__)


@app.route('/api/v1/next-bill', methods=['GET'])
def get_next_bill():
    return jsonify(asdict(service.get_next_bill()))


app.run()

if __name__ == "__main__":
    get_next_bill()
