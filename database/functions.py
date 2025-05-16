# Открытие файла
def open_file(name='settings'):  # открытие txt файла
    with open(f'data/{name}.txt', encoding='utf-8') as file:
        TRANSLATION, CONF = map(int, file.read().split('\n'))

    return TRANSLATION, CONF



# Запись изминений
def write(translation, conf, name='settings'):
    with open(f'data/{name}.txt', encoding='utf-8', mode='w') as file:
        data = f'{translation}\n{conf}'
        file.write(data)