#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import mechanize
import urllib
import time
#import zipfile
#import shutil
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import unidecode
# apt-get install python-mysql.connector

def getList(): 
    with open('stock_list.txt','r') as txt:
    #with open('stock_list_test.txt','r') as txt:
        stock_list = []
        stock_list = txt.read().split('\n')
    return stock_list

def writeData(data = "", file_name = "", switch = 0): 
    with open(file_name,'a') as txt:
        buf_1 = data
        txt.write(buf_1)
        if switch == 1:
            txt.write(",")
        else: 
            txt.close()
    return txt.close()

def EoD(date):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    stock_list = getList();

    for ticker in stock_list:
        url = "http://s.cafef.vn/Lich-su-giao-dich-" + ticker + "-1.chn#data"
        browser.open(url)
        soup = BeautifulSoup(browser.response().read(), "html.parser")
        check_table = soup.find('div', attrs={'id':'ctl00_ContentPlaceHolder1_ctl03_divHO'})
        if check_table == None:
            check_table = soup.find('div', attrs={'id':'ctl00_ContentPlaceHolder1_ctl03_notHO'})
        tr = check_table.find('table').findAll('tr')
        for row in tr:
            if row.has_attr('id'):
                writeData(ticker,"EoD.txt",1)
                td = row.findAll('td')
                for cell in td:
                    cell = cell.text
                    cell = unidecode.unidecode(cell).replace(',', '').strip()
                    writeData(cell, "EoD.txt", 1)
                writeData("\n", "EoD.txt")
        print tickerticker + "... EoD Done!"

def IntraDay(date):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    stock_list = getList()
    output_file_name = "IntrDay_" + date + ".csv"

    for ticker in stock_list:
        url = "http://s.cafef.vn/Lich-su-giao-dich-" + ticker + "-6.chn"
        browser.open(url)
        soup = BeautifulSoup(browser.response().read(), "html.parser")
        check_table = soup.find('div', attrs={'id':'price-list'})
        if check_table != None:
            table = check_table.find('table', attrs={'id':'tblData'})
            if table != None:
                tr = table.findAll('tr')       
                for row in tr:
                    writeData(ticker, output_file_name, 1)
                    td = row.findAll('td')
                    for cell in td:
                        cell = cell.text
                        cell = unidecode.unidecode(cell).replace(',', '').strip()
                        cell = cell.split(' ')
                        writeData(cell[0], output_file_name, 1)
                    writeData("\n", output_file_name)
                print ticker + "... IntrDay Done!"
            else:
                print ticker + "... **table not exist**"

def main():
    date = time.strftime("%Y%m%d")
    #EoD(date)
    print "Date defined..."
    print "Downloading data..."
    IntraDay(date)

    
main()