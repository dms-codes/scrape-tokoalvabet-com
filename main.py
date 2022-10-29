import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs

FILENAME = 'tokoalvabet.csv'
START_ROW_NUM = 1
COLUMNS = ['Judul',
            'Harga',
            'Penulis',
            'Genre',
            'Stock',
            'Berat',
            'Cetakan',
            'Bulan',
            'Tahun',
            'Lebar', 
            'Panjang',
            'Tebal',
            'Format',
            'ISBN',
            'Sinopsis',
            'Tentang_penulis',
            'Foto Produk1',
            'Foto Produk2',
]
ALVABET_DISCOUNT = 0.35
SS1 = "https://www.tokopedia.com/search?condition=1&fcity=174%2C175%2C176%2C177%2C178%2C179&navsource=&ob=3&pmin="
SS2 = "&rf=true&shop_tier=1%233%232&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&q="
HEADERS = {
    'authority': 'www.dickssportinggoods.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}
def runScrapeQt():
    from PyQt6 import uic
    from PyQt6.QtWidgets import QMainWindow,QApplication,QPlainTextEdit,QTextEdit,QPushButton,QLabel,QFileDialog
    from PyQt6.QtGui import QPixmap,QImage
    import os
    import sys
    import csv
    import requests as r 
    from bs4 import BeautifulSoup as bs 
    from datetime import datetime
    import pandas as pd

    class UI(QMainWindow):
        def __init__(self):
            super(UI,self).__init__() 
            uic.loadUi('scrape-tokoalvabet-com.ui',self)

            self.getchild()
            self.start = datetime.now()
            self.timestartLbl.setText('Time start : '+self.start.strftime("%d/%m/%Y, %H:%M:%S"))
            self.show()

        def getchild(self):
            self.homeURLPTE = self.findChild(QPlainTextEdit,'homeURLPTE')
            self.columnsPTE = self.findChild(QPlainTextEdit,'columnsPTE')
            self.filenamePTE = self.findChild(QPlainTextEdit,'filenamePTE')
            self.logTE = self.findChild(QTextEdit,'logTE')
            #self.logTE.setPlainText('res 59 Detik79200.0Richard Wiseman Pengembangan Diri49')
            
            self.scrapeBtn = self.findChild(QPushButton,'scrapeBtn')
            self.scrapeBtn.clicked.connect(self.onClick)
            
            self.timestartLbl = self.findChild(QLabel,'timestartLbl')
            self.timefinishLbl = self.findChild(QLabel,'timefinishLbl')
            self.numrowsLbl = self.findChild(QLabel,'numrowsLbl')
        
        def scrape(self,homeurl,columns,filename):
            self.rowsnum = 0
            html = r.get(homeurl).content
            soup = bs(html,'html.parser')
            category_links = soup.find_all('li', class_='category my-menu')
            with open(filename, 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                col_names = columns
                writer.writerow(col_names)
                titles = [""]
                for category in category_links:
                    category_text = category.text.strip()
                    category_url = category.find('a')['href']
                    c_urls = []
                    c_urls.append(category_url)
                    #print(category_text, category_url)
                    category_html = r.get(category_url).content
                    category_page_soup = bs(category_html,'html.parser')
                    pagination_pages = category_page_soup.find_all('a', class_='js-search-link')
                    try:
                        last_page = int(pagination_pages[-2]['href'].split('page=')[-1])
                        for i in range(2,last_page+1):
                            c_urls.append(category_url+"?page="+str(i))
                    except:pass
                    for c_url in c_urls:
                        page_html = r.get(c_url).content
                        page_soup = bs(page_html,'html.parser')
                        products = page_soup.find_all('a',class_='thumbnail product-thumbnail')
                        num_products = len(products)
                        for i,product in enumerate(products):
                            product_url = product['href']
                            product_html = r.get(product_url).content
                            product_soup = bs(product_html,'html.parser')
                            div = product_soup.find('div',class_='product-discount')
                            print(product_url)
                            if div:
                                span = div.find('span')
                                price = float(span.text.replace("Rp","").replace(",00",""))*1000
                            else:
                                price = float(product_soup.find('div',class_='current-price').text.split("\n")[1].replace("Rp","").replace(",00",""))*1000

                            if price == 0:
                                continue
                            product_info_soup = product_soup.find_all('div',class_='product-information')

                            for info in product_info_soup:
                                QApplication.processEvents()

                                for p in info.find_all('p'):
                                    if p.text.startswith('Judul'):
                                        #print(p.text)
                                        judul = p.text.split(':')[1].strip()

                                        #print('Judul: ',judul)
                                    elif p.text.startswith('Penulis'):
                                        if ':' in p.text:
                                            penulis = p.text.split(":")[1].strip()
                                        else:
                                            penulis = p.text.split("Penulis")[1].strip()
                                    elif p.text.startswith('Penerjemah'):
                                        penerjemah = p.text.split(":")[1].strip()
                                    elif p.text.startswith('Genre'):
                                        genre = p.text.split(':')[1]
                                    elif p.text.startswith('Cetakan'):
                                        cetakan = p.text.split(':')[1]
                                        #print('cetakan',cetakan)
                                        if len(cetakan.split(';'))==2:
                                            if ',' not in cetakan.split(';')[1]:
                                                cetakan_ke = cetakan.split(';')[1].split(' ')[0]
                                                bulan = cetakan.split(';')[1].split(' ')[1]
                                                tahun = cetakan.split(';')[1].split(' ')[2]
                                            else:    
                                                cetakan_ke = cetakan.split(';')[1].split(',')[0]
                                                bulan = cetakan.split(';')[1].split(',')[1].split(' ')[1]
                                                #print(cetakan_ke,bulan)
                                                tahun = int(cetakan.split(';')[1].split(',')[1].split(' ')[2])
                                        elif len(cetakan.split(','))==1:
                                            cetakan = ""
                                        elif len(cetakan.split(','))==3:
                                            cetakan_ke = cetakan.split(',')[0]
                                            bulan = cetakan.split(',')[1]
                                            tahun = int(cetakan.split(',')[2])                              
                                        else:    
                                            cetakan_ke = cetakan.split(',')[0]
                                            bulan_tahun = cetakan.split(',')[1].strip().replace(';','').replace('\\','').split(' ')
                                        #print(cetakan_ke)
                                        #print(bulan_tahun)
                                        if len(bulan_tahun)==5:
                                            cetakan_ke = bulan_tahun[2]
                                            bulan = bulan_tahun[3]
                                            tahun = int(bulan_tahun[4])                               
                                        elif len(bulan_tahun)==3:
                                            cetakan_ke = bulan_tahun[2]
                                            bulan = bulan_tahun[0]
                                            tahun = int(bulan_tahun[1])
                                        elif len(bulan_tahun)==2:
                                            bulan = bulan_tahun[0]
                                            tahun = int(bulan_tahun[1])
                                        else:
                                            bulan = ""
                                            tahun = int(bulan_tahun[0])
                                    elif p.text.startswith('Ukuran'):  
                                        if "(" in p.text:
                                            format = p.text.split("(")[1].strip().replace(')','')   
                                            pp = p.text.split("(")[0].strip()
                                        else:
                                            pp = p.text           
                                        ukuran = pp.split(':')[1].replace(' ','').replace("cm","").replace('Cm','').replace("x"," ").replace('X',' ').replace(',','.')
                                        lebar = float(ukuran.split(" ")[0].strip())
                                        panjang = float(ukuran.split(" ")[1].strip())
                                    elif p.text.startswith('Format'):  
                                        format = p.text.split(" ")[1]
                                    elif p.text.startswith('Tebal'):
                                        p_l = p.text.split(':')[1].strip()
                                        if '+' in p_l:
                                            p_l = p_l.split('+')[1].strip()
                                        #print(p.text,p_l)
                                        #if p_l.split(" ")[0] == '':
                                        #    tebal = 'NA'
                                        #    berat = 'NA'
                                        #else: 
                                        tebal = int(p_l.split(" ")[0]) 
                                        berat = int(tebal) + 100
                                    elif p.text.startswith('ISBN'):
                                        isbn = p.text.split(':')[1]
                                    else:
                                        format = ''
                            
                            if judul not in titles:
                                titles.append(judul)            
                                stock_soup = product_soup.find('div',class_='product-quantities')
                                try:
                                    stock = int(stock_soup.find('span').text.split(' ')[0])
                                except:
                                    stock = 0
                                    continue
                                thumbnails = product_soup.find_all('li',class_='thumb-container')
                                img_urls = []
                                for thumbnail in thumbnails:
                                    img_urls.append(thumbnail.find('a')['data-zoom-image'])
                                
                                if len(img_urls) == 1:
                                    img_urls.append("")
                #                print(judul,price,penulis,genre,cetakan,bulan,tahun,lebar, panjang,tebal,berat,isbn,stock,sep="\n")
                #                print(img_urls)
                                sinopsis_tentang_penulis = product_soup.find('div',class_ ='product-d').text[9:].strip()
                                if len(sinopsis_tentang_penulis.split('PENULIS'))==2:
                                    sinopsis, tentang_penulis = sinopsis_tentang_penulis.split('PENULIS')
                                    sinopsis = sinopsis.strip()
                                    tentang_penulis = tentang_penulis.strip()
                                elif len(sinopsis_tentang_penulis.split('PENULIS'))==1:
                                    sinopsis = sinopsis_tentang_penulis.split('PENULIS')[0]
                                    sinopsis = sinopsis.strip()
                                    tentang_penulis = ""
                                list_res = [judul, price, penulis, genre, stock,berat, cetakan,bulan,tahun,lebar, panjang,tebal,format,isbn,sinopsis,tentang_penulis,
                                        img_urls[0],img_urls[1]]
                                res = ''
                                for l in list_res:
                                    res += str(l).strip()+'\n'
                                #print('res',res)
                                self.logTE.setText(str(res))
                                QApplication.processEvents()
                                #import time
                                #time.sleep(5)
                                writer.writerow([judul, price, penulis, genre, stock,berat, cetakan,bulan,tahun,lebar, panjang,tebal,format,isbn,sinopsis,tentang_penulis,
                                        img_urls[0],img_urls[1]])
                                self.rowsnum += 1
                                #print(f'{i+1}/{num_products} {genre} - {judul}')
            self.end = datetime.now()
            self.timefinishLbl.setText('Time finish : '+self.end.strftime("%d/%m/%Y, %H:%M:%S"))
            self.numrowsLbl.setText('Number of rows : '+str(self.rowsnum)) 
            print("The time of execution of above program is :",
                (self.end-self.start), "s")    
        
        def onClick(self):
            homeurl = self.homeURLPTE.toPlainText()
            columns = self.columnsPTE.toPlainText()
            filename = self.filenamePTE.toPlainText()
            self.scrape(homeurl,COLUMNS,filename)
            
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()



def get_dataframe(filename=FILENAME,columns=COLUMNS, start_row_num = START_ROW_NUM):
    orig_df = pd.read_csv(f'{filename}')
    df = orig_df[start_row_num-1:]
    df.columns = columns
    return df

def read_data_csv():
    col_names = COLUMNS
    df = get_dataframe(filename=FILENAME, columns=col_names,start_row_num=1)
    return df

def runPriceComparatorQt():
    from PyQt6 import uic
    from PyQt6.QtWidgets import QMainWindow,QApplication,QLineEdit,QTextEdit,QPushButton,QLabel,QFileDialog
    from PyQt6.QtGui import QPixmap,QImage
    import os
    import sys

    class UI(QMainWindow):
        def __init__(self):
            super(UI,self).__init__()
            
            uic.loadUi('price-comparator-alvabet.ui',self)
            
            self.getChildren()
            self.index = 0
            self.price_comparator_qt()
            self.updateData()

            #self.startBtn.clicked.connect(self.onStart)    
            self.show()
        
        def getChildren(self):
            self.cb = QApplication.clipboard()
            self.cb.clear()
            self.totalRowsLbl = self.findChild(QLabel,'totalRowsLbl')
            self.nomorLE = self.findChild(QLineEdit,'nomorLE')
            self.nomorLE.returnPressed.connect(self.onPressed)
            
            self.titleTE = self.findChild(QTextEdit,'titleTE')
            
            self.normalPriceLE = self.findChild(QLineEdit,'normalPriceLE')
            self.discountLE = self.findChild(QLineEdit,'discLE')
            self.bepLE = self.findChild(QLineEdit,'bepLE')
            self.stockLE = self.findChild(QLineEdit,'stockLE')
            self.descTE = self.findChild(QTextEdit,'descTE')
            self.searchURLTE = self.findChild(QTextEdit,'searchURLTE')
            self.searchResultsLE = self.findChild(QLineEdit,'searchResultsLE')
            self.searchDetailsTE = self.findChild(QTextEdit,'searchDetailsTE')
            self.beratLE = self.findChild(QLineEdit,'beratLE')
            self.backBtn = self.findChild(QPushButton,'backBtn')
            self.backBtn.clicked.connect(self.onBack) 
            
            self.nextBtn = self.findChild(QPushButton,'nextBtn')
            self.nextBtn.clicked.connect(self.onNext) 
            
            #self.startBtn = self.findChild(QPushButton,'startBtn') 

            self.imgLabel = self.findChild(QLabel,'imgLabel')

            self.saveImageBtn = self.findChild(QPushButton,'saveImageBtn') 
            self.saveImageBtn.clicked.connect(self.onSaveImage) 
            
            self.copyLibrariURLBtn = self.findChild(QPushButton,'copyLibrariURLBtn')
            self.copyLibrariURLBtn.clicked.connect(self.onCopyURL) 
            
            self.tweetBtn = self.findChild(QPushButton,'tweetBtn')
            self.tweetBtn.clicked.connect(self.onTweet)
            
            self.copyTitleBtn = self.findChild(QPushButton,'copyTitleBtn')
            self.copyTitleBtn.clicked.connect(self.onCopyTitleBtnClicked)
                       
            self.copyDescBtn = self.findChild(QPushButton,'copyDescBtn')           
            self.copyDescBtn.clicked.connect(self.onCopyDescBtnClicked)


        def onCopyTitleBtnClicked(self):
            text = f'{self.titleTE.toPlainText()}'
            try:
                self.cb.setText(text)
            except:
                pass

        def onCopyDescBtnClicked(self):
            text = f'{self.descTE.toPlainText()}'
            try:
                self.cb.setText(text)
            except:
                pass
            
        def onTweet(self):
            hashtags = ''
            self.data['Penulis'][self.index] = self.data['Penulis'][self.index].strip().replace('.','')
            for t in self.titleTE.toPlainText().split(' '):
                hashtags += '#'+t.replace(':','')+' '
            if '&' in self.data['Penulis'][self.index]:
                penuliss = self.data['Penulis'][self.index].split('&')
                for penulis in penuliss:
                    hashtags +='#'+''.join(penulis.replace('.','').split(' '))+' '
            else:
                hashtags +='#'+''.join(self.data['Penulis'][self.index].split(' '))
            tweet = f'{self.titleTE.toPlainText()} {hashtags} {self.copyLibrariURLBtn.text()}'
            try:
                self.cb.setText(tweet)
            except:
                pass

        def onCopyURL(self):
            try:
                self.cb.setText(self.li_url)
            except:
                pass
            
        def onSaveImage(self):
            default_fname = self.data['Foto Produk1'][self.index].split('/')[-1]
            fname,_ = QFileDialog.getSaveFileName(self, 'Save File',default_fname)
            import requests
            try:
                with open(fname, 'wb') as f:
                    f.write(requests.get(self.data['Foto Produk1'][self.index]).content)
            except:
                pass 
            
        def onPressed(self):
            self.index = int(self.nomorLE.text())-1
            self.updateData()

        def onStart(self):
            self.price_comparator_qt()
            if self.nomorLE.text()=='':
                self.index = 0
            else: 
                self.index = int(self.nomorLE.text())-1
            self.updateData()
                    
        def onNext(self):
            if self.index == len(self.data):
                self.index = self.index
            else:
                self.index += 1
            self.updateData()

        def onBack(self):
            if self.index == 0:
                self.index = self.index
            else:
                self.index -= 1
            self.updateData()
            
        def updateData(self):
            self.image = QImage()
            try:
                self.image.loadFromData(requests.get(self.data['Foto Produk1'][self.index]).content)
            except:
                pass
            self.imgLabel.setPixmap(QPixmap(self.image))
            self.imgLabel.show()
            
            self.totalRowsLbl.setText(f'Total Number of Data : {str(int(len(self.data)))}')
            self.nomorLE.setText(str(self.index+1))
            self.titleTE.setText(str(self.data['Judul'][self.index]).strip())
            self.normalPriceLE.setText(str(self.data['Harga'][self.index]))
            self.discountLE.setText(str(ALVABET_DISCOUNT*100)+'%')
            price = float(self.data['Harga'][self.index])
            breakevenprice = price*(1-(ALVABET_DISCOUNT))*1.03
            self.bepLE.setText(f'Rp.{breakevenprice:,.0f}')
            self.stockLE.setText(str(self.data['Stock'][self.index]).strip())
            self.beratLE.setText(str(self.data['Berat'][self.index]).strip())
            self.descTE.setText(str(self.data['Sinopsis'][self.index]).strip())
            
            self.data['Judul'][self.index] = self.data['Judul'][self.index].strip()
            self.data['Judul'][self.index] = self.data['Judul'][self.index].replace(':',' ')
            self.data['Judul'][self.index] = self.data['Judul'][self.index].replace('?',' ')
            if len(self.data['Judul'][self.index])>70:
                self.data['Judul'][self.index] = self.data['Judul'][self.index][:70]
            search_query = SS1+str(breakevenprice)+SS2+'"'+self.data['Judul'][self.index].strip()+'"'
            self.searchURLTE.setText(search_query)
            
            html = requests.get(search_query,headers=HEADERS).content
            soup = bs(html, 'html.parser')
            products_soup = soup.find_all('div', class_='css-974ipl')  #css-12sieg3
            search_details_data = []
            shop_name_list = []
            res = ""
            librari_url = ''
            for product_soup in products_soup:
                
                try:
                    #product information 
                    product_url = product_soup.find('a')['href']
                    #shop location and name
                    shop_info_soup = product_soup.find('div', class_ = 'css-1rn0irl' )
                    shop_name = shop_info_soup.find('span',class_ = 'prd_link-shop-name css-1kdc32b flip').text
                    if shop_name not in shop_name_list:
                        shop_name_list.append(shop_name)
                    else: continue
                    shop_location = shop_info_soup.find('span',class_ ='prd_link-shop-loc css-1kdc32b flip').text

                    price = product_soup.find('div',class_="prd_link-product-price css-1ksb19c").text.replace("Rp","").replace(".","")
                    terjual = ""
                    try:
                        terjual = product_soup.find('span', class_="prd_label-integrity css-1duhs3e").text
                    except:pass
                    
                    if shop_name == "Librari":
                        librari_url = product_url

                    search_details_data.append([shop_name,float(price),terjual])
                except:
                    pass
            self.searchDetailsTE.setText('')
            if search_details_data: 
                try:
                    self.pricingQt(search_details_data,breakevenprice,self.data['Judul'][self.index],librari_url)
                except:
                    self.searchDetailsTE.setText('')    
                    self.copyLibrariURLBtn.setText('No URL to copy.')
            self.searchResultsLE.setText(str(len(search_details_data)))
            #self.searchDetailsTE.setText(self.data['Sinopsis'][self.index])
        
        def pricingQt(self,data,breakevenprice,title,url):
            self.li_url = url.split('?')[0]
            self.copyLibrariURLBtn.setText(self.li_url)
            url = url.split("?")[0]
            #ress = f'Search results: {len(data)}.\n'
            ress = ''
            res = []
            #put data to result if price>breakevenprice
            librari_index = 100
            for d in data:
                shop_name,price,terjual = d
                if terjual == "":
                    n = 0
                else: n = terjual.split(" ")[1]
                profit_if_price_follow = price - 50 - breakevenprice 
                if shop_name == 'Librari':
                    res.append(d)
                else:
                    if profit_if_price_follow and n :
                        res.append(d)     
            if len(res)>0:           
                for i,r in enumerate(res):
                    ress += f'{r[0]}\t{r[1]:,.2f}\t{r[2]}\n'
                    if r[0] == 'Librari':
                        librari_index = i
                        li_profit = r[1] - 50 - breakevenprice 
                        
                #print(librari_index)
                if librari_index == 0:
                    #print(res[librari_index])
                    li_price = res[librari_index][1]
                    ress +=f'Our price is already the best @{li_price:,.2f}\n'
                    #if profit_if_price_follow>0:
                    if li_profit>0:
                        ress +=f'Profit: {li_profit:,.2f}\n'
                    else:
                        ress +=f'Loss: {li_profit:,.2f}\n'
                    
                    if len(res)>1:
                        next_price = res[librari_index+1][1] 
                        if next_price - li_price > 50:
                            ress +=f"Price can be increased to {next_price -50:,.2f}\n"
            else: print("No results.")
            print(ress)
            self.searchDetailsTE.setText(ress) 
        
        
        def price_comparator_qt(self):
            df = read_data_csv()
            if self.nomorLE.text()=='':
                startsfrom = 1
                self.nomorLE.setText(str(startsfrom))
            else: startsfrom = int(self.nomorLE.text())
            
            self.data = df[startsfrom-1:]
            
            
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()    
    
if __name__=='__main__':
    #runScrapeQt()
    runPriceComparatorQt()