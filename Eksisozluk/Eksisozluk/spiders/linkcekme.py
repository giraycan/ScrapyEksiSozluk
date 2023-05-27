import scrapy

class EksiSozlukSpider(scrapy.Spider):
    name = 'linkcekme'
    start_urls = ['https://eksisozluk1923.com/']

    def parse(self, response):
        # Linkleri bir listeye aktar
        links = []

        entries = response.css('ul.topic-list li')
        for entry in entries:
            link = response.urljoin(entry.css('a::attr(href)').get())
            if link!='https://eksisozluk1923.com/':
                links.append(link)

        # Linkleri bir metin dosyasına yazdır
        with open('links.txt', 'w') as file:
            for link in links:
                file.write(link + '\n')

        yield {
            'links': links
        }
