config_dir = '../config/'

welcome_text = \
    '''
\tПривет! Я помогу тебе в составлении конфигурации для
\tнашей панели. Ответь на несколько вопросов, и я сгенерирую
\tшаблон конфигурации с подсказками, который ты сможешь
\tлегко заполнить и быстро начать пользоваться панелью.

\tПодсчет объектов идет всегда сверху вниз. Начальный индекс - 1.

\tЗакончить работу: ctrl + C
\tВерсия: 1.0
    '''
MAX_PARTS = 10
MAX_OBJECTS_IN_PART = 100
MAX_LINKS = 100

BLOCK_TYPE = 'block'
COMMUTATOR_TYPE = 'commutator'
BLADE_TYPE = 'blade'

COUNT_OF_NODES_IN_POOL = 8
NODES_IN_LOM2_POOL = {
    0: [1, 2, 5, 6],
    1: [3, 4, 7, 8],
    2: [9, 10, 13, 14],
    3: [11, 12, 15, 16],
    4: [17, 18, 21, 22],
    5: [19, 20, 23, 24],
    6: [25, 26, 29, 30],
    7: [27, 28, 31, 32]
}

def read_int(welcome_text, min, max):
    while True:
        result = int(input(welcome_text))
        if result < min or result > max:
            print('\t\tОшибка: ' + str(result) + ' некорректное значение')
            continue
        return result

def read_bool(welcome_text):
    while True:
        read_text = input(welcome_text).lower()
        if read_text in ['y', 'yes']:
            return True
        elif read_text in ['n', 'no']:
            return False
        print ('\t\tОшибка: не распознан ответ')

print(welcome_text)
config_file = config_dir + input('\tНазвание файла с конфигурацией: ' + config_dir)

count_objects = 0

is_lom2 = read_bool('\tЭто стойка Ломоносов-2? (y/n) ')
if is_lom2:
    rack_number = read_int('\tНомер стойки: ', 48, 56)
    count_parts = 2
else:
    count_parts = read_int('\tКоличество вертикальных частей у стойки: ', 1, MAX_PARTS)

parts = []
for i in range(1, count_parts + 1):
    count_in_part = read_int('\tКоличество объектов в ' + str(i) + ' вертикальной части: ',
                             1, MAX_OBJECTS_IN_PART)
    count_objects += count_in_part
    part = {'count': count_in_part, 'blades': set(), 'commutators': set()}
    while True:
        blade_count = read_int('\tКоличество блейд-шасси в ' + str(i) + ' вертикальной части: ',
                               0, count_in_part)
        for j in range(1, blade_count + 1):
            part['blades'].add(read_int('\tИндекс ' + str(j) + ' блейд-шасси: ',
                                           1, count_in_part + 1))
        if len(part['blades']) != blade_count:
            print('\t\tОшибка: некорректные индексы блейд-шасси.')
            continue
        break
    while True:
        commutator_count = read_int('\tКоличество коммутаторов в ' + str(i) + ' вертикальной части: ',
                               -1, count_in_part)
        for j in range(1, commutator_count + 1):
            part['commutators'].add(read_int('\tИндекс ' + str(j) + ' коммутатора: ',
                                           0, count_in_part + 1))
        if len(part['commutators']) != commutator_count:
            print('\t\tОшибка: некорректные индексы коммутаторов.')
            continue
        break
    parts.append(part)

count_links = read_int('\tКоличество связей в стойке: ', 0, MAX_LINKS)
links = []
for i in range(1, count_links + 1):
    count_in_link = read_int('\tКоличество объектов в ' + str(i) + ' связи: ',
                             1, count_objects)
    links.append(count_in_link)

def get_object_type(index, object):
    if index in object['blades']:
        return BLADE_TYPE
    if index in object['commutators']:
        return COMMUTATOR_TYPE
    return BLOCK_TYPE

def get_block_id(part_number, local_block_id):
    if part_number == 0:
        pool_number = COUNT_OF_NODES_IN_POOL - 1 - local_block_id // COUNT_OF_NODES_IN_POOL
        id_in_pool = COUNT_OF_NODES_IN_POOL - 1 - local_block_id % COUNT_OF_NODES_IN_POOL
    elif part_number == 1:
        pool_number = local_block_id // COUNT_OF_NODES_IN_POOL
        id_in_pool = local_block_id % COUNT_OF_NODES_IN_POOL
    else:
        raise ValueError('Lom2 rack has more then 2 parts')

    block_id = ''
    for host_index in NODES_IN_LOM2_POOL[id_in_pool]:
        if host_index < 10:
            str_host_index = '0' + str(host_index)
        else:
            str_host_index = str(host_index)
        block_id += 'n' + str(rack_number) + str(pool_number) + str_host_index + ';'
    return block_id


with open(config_file, 'w') as file:
    print('# массив, описывающий вертикальные части стойки', file=file)
    print('parts:', file=file)
    for i in range(count_parts):
        if i == 0:
            print('  # ширина вертикальной части', file=file)
        print('  - width: 1', file=file)
        if i == 0:
            print('  # массив, описывающий объекты внутри вертикальной части', file=file)
        print('    objects:', file=file)
        local_block_id = 0
        for j in range(1, parts[i]['count'] + 1):
            if j == 1:
                print('        # тип объекта', file=file)
            object_type = get_object_type(j, parts[i])
            print('      - type: ' + object_type, file=file)
            if j == 1:
                print('        # размер объекта', file=file)
            print('        size: 1', file=file)
            if j == 1:
                print('        # уникальный идентификатор объекта', file=file)
            if object_type == BLOCK_TYPE:
                if is_lom2:
                    print('        id: ' + str(get_block_id(i, local_block_id)), file=file)
                    local_block_id += 1
                else:
                    print('        id: <...>', file=file)
            elif object_type == BLADE_TYPE:
                print('        id: <...>', file=file)
                print('        # конфигурация блейд-шасси', file=file)
                print('        settings: ', file=file)
                print('          count_sections: <...>', file=file)
                print('          servers:', file=file)
                print('              # массив серверов блейд-шасси', file=file)
            elif object_type == COMMUTATOR_TYPE:
                print('        id: <...>', file=file)
                print ('       # тип коммутатора', file=file)
                print('        commutator_type: <...>', file=file)

    if count_links == 0:
        print('links: []', file=file)
    else:
        print('links:', file=file)
        for i in range(count_links):
            if i == 0:
                print('    # тип связи', file=file)
            print('  - type: <...>', file=file)
            if i == 0:
                print('    # массив, описывающий объекты внутри связи', file=file)
            print('    objects: ', file=file)
            for j in range(links[i]):
                if j == 0:
                    print('        # идентификатор объекта, находящегося внутри связи', file=file)
                print('      - id: <...>', file=file)

print()
print('\tШаблон конфигурации готов: ' + str(config_file))
print()


