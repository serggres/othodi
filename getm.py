# -*- coding: UTF-8 -*-
import urllib
# import nltk, urllib
# from bs4 import BeautifulSoup # damit werden die HTML-texte entfernt
# импорт инструмента BeautifulSoup
import bs4
import sys # system
import os
import requests

def get_raw_text_from_url(url,start_marker = 'DATASTART',end_marker = 'DATAEND'):
    responce = requests.get(url) # получили много иформации
    # print(responce.headers['content-type']) # в том числе и информацию о кодировке, в которой скачана страница - можно посмотреть.
    soup = bs4.BeautifulSoup(responce.text, 'html.parser') # BeautifulSoup сам разбиратеся с кодировкой
    texts = soup.findAll(text=True) # возвращает весь текст со всех уровней html

    def visible(element): # выбрасываем все, что браузер бы не вывел на экран.
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False 
        return True

    f = open(os.devnull, 'w')
    temp = sys.stdout
    sys.stdout = f

    visible_texts = filter(visible, texts) # функция "filter()" по значению "visible" (True|False) включает или не включает текст ("texts") в возвращаемый список
    raw_text = u"" # инициализируем пустую строку, которая точно будет печататься в консоли
    for text in visible_texts:
        try:
            print(text)  # русский текст печатается, но что-то все равно не выводится в консоль. Вряд ли это что-то нам пригодится..
            raw_text = raw_text + '\n' + text # Если напечатать удалось, добавляем в итоговую строку
        except UnicodeError as e: # знаем, что будут проблемы с печатью "не той" кодировки.
            pass # игнорируем эти проблемы.
    sys.stdout = temp
    # cut_text = raw_text.split(start_marker)[1].split(end_marker)[0].strip()
    return(raw_text)

    # return(soup.get_text())

# def get_raw(url):
#   urlData = urllib.request.urlopen(url)
#   html = urlData.read().decode("utf-8")
#   string_of_func_settings = 'html.parser'
#   soup = bs4.BeautifulSoup(html, string_of_func_settings) # -> error
#   return(soup.get_text())


# def make_text(raw):
#   tokens = nltk.word_tokenize(raw)
#   print("tokens data:")
#   print(type(tokens))
#   print(tokens)
#   text = nltk.Text(tokens)
#   return(text) #prints <Text: >first words from the given text< ...>
    #print(text[:40]) prints given number of words from >text<

# def get_vocab(text):
#   tokens = nltk.word_tokenize(text)
#   dic = {}
#   for token in tokens:
#       dic[token] = dic.get(token, 0) + 1
#   return(len(dic.keys()))

# def lowercasing(text):
#   tokens = nltk.word_tokenize(text)
#   lower = [x.lower() for x in tokens]
#   print(' '.join(lower))

if __name__ == "__main__":
    url_1 = "https://www.dropbox.com/s/t9b9n2i03bz7ckk/cities.txt?dl=0"
    # url_1 = "http://google.ru"
    # url_1 = "http://www.cis.uni-muenchen.de/kurse/desi/sp/"
    raw_text = get_raw_text_from_url(url_1)
    out = open('cities_from_dropbox.txt', 'wb')
    out.write(raw_text)
    out.close()
    # print(raw_text)

    # sys.exit(0) # exit script