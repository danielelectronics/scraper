import requests
from lxml import html
from time import sleep

# ifttt url key
ifttt_key = ''

class product:
    def __init__(self, url):
        self.url = url
        self.name = ''
        self.availability = ''
        self.statusChanged = False
        self.__getAvailability()

    def __getAvailability(self):
        try:
            page = requests.get(self.url)
        except:
            print('Could not get webpage.')
            return

        tree = html.document_fromstring(page.text)
        productAvailability = []

        for element in tree.iter():
            if self.name == '':
                if element.get('class') == 'title':
                    self.name = element.text_content()

            if element.get('class') == 'availability':
                for child in element:
                    if child.text_content() != '':
                        productAvailability.append(child.text_content())

            self.availability = "".join(productAvailability)

    def update(self):
        previousAvailibity = self.availability
        self.__getAvailability()
        if self.availability != previousAvailibity:
            self.statusChanged = True
        else:
            self.statusChanged = False

        return self.statusChanged

def notify(name, availability):
    try:
        requests.post('https://maker.ifttt.com/trigger/statusChanged/with/key/{}'.format(ifttt_key), json = { 'value1' : name, 'value2' : availability })
    except:
        print("Request failed.")

def main():
    # Create list of products
    products = []
    with open('url_list.txt') as file:
        for line in file:
            products.append(product(line.rstrip()))
            sleep(1)

    while True:
        for item in products:
            sleep(60*30)
            if item.update():
                print('Status changed. {0}, {1}, {2}'.format(item.name, item.availability, item.url))
                notify(item.name, item.availability)

if __name__ == '__main__':
    # execute only if run as a script
    main()
