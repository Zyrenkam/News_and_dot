import requests
from bs4 import BeautifulSoup


def create_answer():
    result = {}

    main_links = {'https://ria.ru/economy/': ['list-item__title color-font-hover-only', 'div'],
                  'https://ria.ru/politics/': ['list-item__title color-font-hover-only', 'div'],
                  'https://rsport.ria.ru/': ['cell-list__item-link color-font-hover-only', 'div'],
                  'https://ria.ru/science/': ['list-item__title color-font-hover-only', 'h1'],
                  'https://ria.ru/religion/': ['list-item__title color-font-hover-only', 'div']}

    for curr in main_links.keys():
        print(f"PARSING FROM {curr}")
        url = curr
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        news = soup.find_all('a', class_=main_links[curr][0], limit=1)

        list_of_links = []

        for tag in news:
            list_of_links.append(tag.get('href'))

        for link in list_of_links:
            url = link
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                title = '' + soup.find(main_links[curr][1], class_='article__title').text
                content = soup.find_all('div', class_='article__text')[0:2]
                foto = soup.find('div', class_='media').find('img').get('src')
                # print('LINK', link)
                # print('TITLE', title)
                for i in range(0, len(content)):
                    content[i] = content[i].text[29::]

                # print('CONTENT', content)

                result[title] = ' '.join(content) + '|' + foto
                # print('=================')
            except:
                pass

    return result
