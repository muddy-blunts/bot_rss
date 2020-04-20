#!/usr/local/bin/python
# coding: UTF-8

import feedparser
import datetime
import telebot
import configparser
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from time import sleep


# Считываем настройки
config = configparser.ConfigParser()
config.read('settings.ini')
FEED = config.get('RSS', 'feed')
DATETIME = config.get('RSS', 'DATETIME')
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CHANNEL = config.get('Telegram', 'CHANNEL')
delay = 60

#Получаем RSS ленту
rss = feedparser.parse(FEED)
# Инициализируем телеграмм бота
bot = telebot.TeleBot(BOT_TOKEN)

for post in reversed(rss.entries):
    data = post.published
    time = datetime.datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %z')
    time_old = config.get('RSS', 'DATETIME')
    time_old = datetime.datetime.strptime(time_old, '%Y-%m-%d  %H:%M:%S%z')

    print(time)
    print(time_old)
    # Пропускаем уже опубликованные посты
    if time <= time_old:
        continue
    else:
        # Записываем время и дату нового поста в файл
        config.set('RSS', 'DATETIME', str(time))
        with open('settings.ini', "w") as config_file:
            config.write(config_file)

    print('---------------------------------')
    print(time)
    


    # Получаем заголовок поста
    text = post.title
    print(text)

    # Получаем ссылку на пост
    link = post.links[0].href
    print(link)

    # Получаем картинку
    img = post.summary_detail.value # картинка в этом RSS обернута тэгами, получаем сами тэги
    soup = BeautifulSoup(img, "html.parser") # инициализируем библиотеку для работы с HTML
    img_get = soup.findAll('img')[0] # получаем тэг img
    img_get = img_get['src'] # получаем значение src тэга img
    print(img_get)

    # Скачиваем картинку
    urllib.request.urlretrieve(img_get, 'img.jpg')

    # Отправляем картинку и текстовое описание в Telegram
    bot.send_message(CHANNEL, '<a href="' + link + '">' + text + '</a>', parse_mode='HTML')
    
    if __name__ == 'main':
        while True:
            sleep(30)
bot.polling()
