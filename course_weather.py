import requests
from bs4 import BeautifulSoup


def get_temperature(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()

    res = f'\n\nГород {city} \nТемпература воздуха будет в районе ' + str(int(weather_data['main']['temp'])) + '°C,\n' + \
          'Ощущается как ' + str(int(weather_data['main']['feels_like'])) + '°C,\n' +\
          'Минимальная температура за день: ' + str(int(weather_data['main']['temp_min'])) + ' °C, \n' +\
          'Максимальная днем: ' + str(int(weather_data['main']['temp_max'])) + '°C,\n' +\
          'Скорость ветра: ' + str(weather_data['wind']['speed']) + ' м/с.'

    return res


def get_kurs(currency, url_currency):
    # Ссылка на нужную страницу

    full_page = requests.get(f'https://www.banki.ru/products/currency/cash/{url_currency}/stavropol~skiy_kray/essentuki/')

    # Разбираем через BeautifulSoup
    soup = BeautifulSoup(full_page.content, 'html.parser')

    # Получаем нужное для нас значение и возвращаем его
    convert = soup.findAll("div", {'class': "Text__sc-j452t5-0 bCCQWi"})

    return '\n\n' + currency + convert[0].text[0:-1:] + 'руб'


def do():
    text_temperature = 'Прогноз погоды' + get_temperature('Москва') + get_temperature('Санкт-Петербург') + get_temperature('Владивосток') + get_temperature('Краснодар')

    text_course = 'Курсы валют'
    text_course += get_kurs('Доллар: ', 'usd')
    text_course += get_kurs('Евро: ', 'eur')
    text_course += get_kurs('Юань: ', 'cny')

    return [text_temperature, text_course]
