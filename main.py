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
                                writer.writerow(list_res)
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
            self.scrape(homeurl,columns,filename)
            
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
    
if __name__=='__main__':
    runScrapeQt()
