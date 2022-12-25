import requests
import os
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path


class PriceCheck:
    def momo_price(self,url_list):
        for i, url in enumerate(url_list):
            hs = {
                "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36",
            }
            res = requests.get(url, headers=hs)
            soup = BeautifulSoup(res.text, "html.parser")
            
            
            old_price = 0
            price = soup.find("meta", property="product:price:amount")["content"]
            item = soup.find("meta", property="og:title")['content']

            ######################################################################################################
            #                   BLOCK 1. see README.md and change the params below                               #
            ######################################################################################################
            mailaddress = "youremail@gmail.com"
            password = "your password"
            fpath = "C:\\Users\\price_check"


            if os.path.exists('%s\\%s.txt'% (fpath, url.split("?")[1])):
                with open('%s\\%s.txt'% (fpath, url.split("?")[1]), 'r') as f:
                    old_price = f.read()
                with open('%s\\%s.txt'% (fpath, url.split("?")[1]), 'w') as f:
                    f.write(price)

                if price != old_price:
                    content = MIMEMultipart()  #建立MIMEMultipart物件
                    content["subject"] = "【價格變動!】 %s" % item  #郵件標題                  
                    content["from"] = mailaddress  #寄件者
                    content["to"] = mailaddress #收件者
                    #content.attach(MIMEText("%s 的價格由 %s 變動為 %s" %(item, old_price, price)))  #郵件內容

                    template = Template(Path("%s\\template.html"% fpath).read_text(encoding="utf-8"))
                    body = template.substitute({ "item": item, "old_price" : old_price, "price" : price, "url" : url})
                    content.attach(MIMEText(body, "html"))
                    
                    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
                        try:
                            smtp.ehlo()  # 驗證SMTP伺服器
                            smtp.starttls()  # 建立加密傳輸                           
                            smtp.login(mailaddress, password)  # password = gmail application password
                            smtp.send_message(content)  # 寄送郵件
                            #print("Complete!")
                        except Exception as e:
                            pass
                            #print("Error message: ", e)
                            
                else:
                	pass
                    #print('資料未更新，從資料庫讀取...')
            else:            
                with open('%s\\%s.txt'% (fpath, url.split("?")[1]), 'w') as f:
                    f.write(price)
                #print('Current Price Saved...') 
                
if __name__ == "__main__":
    check_price = PriceCheck()

            ######################################################################################################
            #                   BLOCK 2.     product url that you want to chase below                            #
            ######################################################################################################    
    url_list = ["https://www.momoshop.com.tw/goods/",
                "https://www.momoshop.com.tw/goods/"]

    check_price.momo_price(url_list)
