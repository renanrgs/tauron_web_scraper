from bs4 import BeautifulSoup

class HtmlParser:

    def __init__(self, content=None):
        self.parser = BeautifulSoup(content, 'html.parser') if content else BeautifulSoup('', 'html.parser')

    def get_total_debt(self, content):
        self.parser.markup = content
        return self.parser.find("span", attrs={"class": "amountInfo red"}).text
