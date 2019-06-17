import csv


class ScraperPipeline(object):
    def __init__(self):
        self.file = open('data.csv', 'w', newline='', encoding='utf8')
        self.writer = csv.writer(self.file)

    def __del__(self):
        self.file.close()

    def process_item(self, item, _):
        self.writer.writerow([item['account'], item['keyword'], item['text']])
        return item
