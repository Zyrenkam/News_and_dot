
d = {'а': ['а', 'a', '@'],
  'б': ['б', '6', 'b'],
  'в': ['в', 'b', 'v'],
  'г': ['г', 'r', 'g'],
  'д': ['д', 'd'],
  'е': ['е', 'e'],
  'ё': ['ё', 'e'],
  'ж': ['ж', 'zh', '*'],
  'з': ['з', '3', 'z'],
  'и': ['и', 'u', 'i'],
  'й': ['й', 'u', 'i'],
  'к': ['к', 'k', 'i{', '|{'],
  'л': ['л', 'l', 'ji'],
  'м': ['м', 'm'],
  'н': ['н', 'h', 'n'],
  'о': ['о', 'o', '0', '○', '@'],
  'п': ['п', 'n', 'p'],
  'р': ['р', 'r', 'p', '₽'],
  'с': ['с', 'c', 's'],
  'т': ['т', 'm', 't'],
  'у': ['у', 'y', 'u'],
  'ф': ['ф', 'f'],
  'х': ['х', 'x', 'h', '}{'],
  'ц': ['ц', 'c', 'u,'],
  'ч': ['ч', 'ch'],
  'ш': ['ш', 'sh'],
  'щ': ['щ', 'sch'],
  'ь': ['ь', 'b'],
  'ы': ['ы', 'bi'],
  'ъ': ['ъ'],
  'э': ['э', 'e'],
  'ю': ['ю', 'io'],
  'я': ['я', 'ya']}

symbols = ['.', ',', '<', '>', '"', '!', '$', '%', '^', '*', '(', ')',
           "'", '[', ']', '{', '}', '/', '|', '-', '_', '+', '=', '#']


def check_msg(phrase):
    phrase = phrase.lower().replace(' ', '')
    print('CHECKING...')

    for el in symbols:
        phrase = phrase.replace(el, '')

    with open('banned_words.txt', 'r', encoding='utf-8') as file:
        words = file.readlines()
        for i in range(0, len(words)):
            words[i] = words[i].replace('\n', '')

    for key, value in d.items():
        for letter in value:
            for phr in phrase:
                if letter == phr:
                    phrase = phrase.replace(phr, key)

    last, res = '', ''
    for letter in phrase:
        if letter != last:
            res += letter
            last = letter

    phrase = res

    for word in words:
        for part in range(len(phrase)):
            fragment = phrase[part: part + len(word)]
            # Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
            if distance(fragment, word) <= len(word) * 0.25:
                print("Найдено '", word, "' Похоже на", fragment)
                return 0
    return 1


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]
