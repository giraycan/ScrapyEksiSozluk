import scrapy


class EksiSozlukSpider(scrapy.Spider):
    name = 'eksisozluk'
    
    
    def start_requests(self):
        base_url = [
                ""
            ]
        #ekşi sözlükdeki gündem linklerini listeden çek sonra tek tek yorumları almak için parse ye gönder
        with open('links.txt', 'r') as file:
            base_url = file.read().splitlines()

        for link in base_url:
            print(link)
            for i in range(1, 100):
                
                url = link.replace("a=popular","p=") + str(i)
                
                yield scrapy.Request(url=url, callback=self.parse)
                
                
                
            
    
        

    def parse(self, response):
        x=1
        i=1
        yorumlar=[]
        kullanicilar=[]
        alt_yorumlar=[]
        #yorumlar-alt yorumlar ve kullanıcı isimlerin alındığı döngü
        while x!=None:
            
            entries = response.xpath(f"/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li[{str(i)}]/div[1]/text()").get()
            j=2
            text="s"
            all_text=""
            while text!=None:
                text=response.xpath(f"/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li[{str(i)}]/div[1]/text()[{str(j)}]").get()
                j=j+1
                if text!=None:
                    all_text="{} {}".format(all_text, str(text))

            
            kullanici_adi=response.xpath(f"/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li[{str(i)}]/footer/div[2]/div/div[1]/div[1]/div/a/text()").get()
            yorumlar.append(entries)
            kullanicilar.append(kullanici_adi)
            alt_yorumlar.append(all_text)
            x=entries
            i=i+1

        #gereksiz boşluk ve harflerin kadlırılması
        birlesik_liste=[]
        for a in range(len(yorumlar)-1):
            yorumlar[a]=(yorumlar[a]).strip("\n").replace("\r\n","")
            alt_yorumlar[a]=(alt_yorumlar[a]).strip("\n").strip()
            kullanicilar[a]=(kullanicilar[a]).strip("\n").strip()
        #None değerlerin atlatılması ve yorumla alt yorumların birleştirilmesi
        for yorum, alt_yorum in zip(yorumlar, alt_yorumlar):
            if yorum is None or alt_yorum is None:
                continue  # None değerleri atla

            birlesik_liste.append(yorum + " " + alt_yorum)
        #küfürlerin txt dosyasından çekilerek bir listeye aktarılması    
        kelime_listesi = []

        with open('karaliste.txt', 'r', encoding="utf-8") as dosya:
            for satir in dosya:
                kelime = satir.strip()  # Satır sonundaki boşlukları kaldırır
                kelime_listesi.append(kelime)

        
        #yorumlarda küfür listesindeki kelimelerden biri eşleşirse kullanıcıyı ve yorumunu bir listeye aktarsın
        eslesen_yorumlar = []
        eslesen_kullanicilar=[]
        for yorum,kullanici in zip(birlesik_liste,kullanicilar):
            if yorum is None or not isinstance(yorum, str):
                continue  # None veya str olmayan değerleri atla

            cümleler = yorum.split(' ')  # Yorumdaki cümleleri ayır
            eşleşme_bulundu = False
            for cümle in cümleler:
                for kelime in kelime_listesi:
                    if kelime == cümle:
                        eslesen_yorumlar.append(yorum)
                        eslesen_kullanicilar.append(kullanici)
                        eşleşme_bulundu = True
                        break  # Eşleşme bulunduğunda iç döngüden çık
                if eşleşme_bulundu:
                    break  # Dış döngüden çık
        
        #sonuç olarak kullanıcı ve yorumunu bir txt dosyasına çıkarsın
        with open("sonuc.txt", "a", encoding="utf-8") as dosya:
            for kullanici, yorum in zip(eslesen_kullanicilar, eslesen_yorumlar):
                satir = f"Kullanıcı: {kullanici}\tYorum: {yorum}\n"
                dosya.write("-" * 30 + "\n")
                dosya.write(satir)
                dosya.write("-" * 30 + "\n\n")
               


       
        

        
        
            
            

        
       