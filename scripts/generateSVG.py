# добавить проверку уникальность link_id

import yaml
from yaml.loader import SafeLoader

with open('../config/config.yaml') as f:
    main_config = yaml.load(f, Loader=SafeLoader)

with open('../config/lom2_48_config.yaml') as f:
    config = yaml.load(f, Loader=SafeLoader)

MAIN_COLOR = main_config['main']['color']  # цвет вычислительной стойки
MAIN_RX = 3 # закругление вычислительной стойки
MAIN_STROKE_COLOR = main_config['main']['stroke_color']  # цвет рамки вычислительной стойки
MAIN_STROKE_WIDTH = 0.3 # ширина рамки

PART_WIDTH = main_config['part']['width'] # дефолтная ширина вертикальной части
PART_DIFFERENCE = main_config['part']['difference'] # расстояние между

BLOCK_HEIGHT = main_config['block']['height'] # высота вычислительного блока
BLOCK_COLOR = main_config['block']['color']  # цвет блока
BLOCK_STROKE_COLOR = main_config['block']['stroke_color']  # цвет рамки блока
BLOCK_RX = 0.7  # закругление углов блоков

COMMUTATOR_HEIGHT = main_config['commutator']['height']  # высота коммутатора
COMMUTATOR_COLORS = main_config['commutator']['colors']  # цвета коммутаторов разных типов
COMMUTATOR_STROKE_COLOR = main_config['commutator']['stroke_color']  # цвет рамки коммутатора
COMMUTATOR_RX = 0.7  # закругление углов коммутаторов

BLADE_WIDTH = PART_WIDTH  # ширина блейд-шасси
BLADE_HEIGHT = main_config['blade']['height']  # высота блейд-шасси
BLADE_COLOR = main_config['blade']['color']  # цвет блейд-шасси
BLADE_STOKE_COLOR = main_config['blade']['stroke_color']  # цвет рамки блейд-шасси
BLADE_RX = 0.7  # закругление углов блейд-шасси

SERVER_COLOR = main_config['blade']['servers']['color']  # цвет сервера в блейд-шасси
SERVER_STROKE_COLOR = main_config['blade']['servers']['stroke_color']  # цвет рамки сервера в блейд-шасси
SERVER_RX = 0.7  # закругление углов сервера в блейд-шасси

STROKE_WIDTH = 0.4
BEGIN_X = 8  # начальные значение координат
BEGIN_Y = BEGIN_X * 1.5  # начальные значение координат

PATH_WIDTH = 2  # расстояние между уровнями путей
PATH_STROKE_WIDTH = 1  # толщина путей

TEXT_SIZE = 10 # размер текста
TEXT_COLOR = '#000000' # цвет текста

IS_SCALE = main_config['part']['is_scale']

class Rect:
    svg = '\t<rect style=\"'

    def __init__(self, id, x, y, color, strokeColor, width, height, rx,
                 strokeWidth, partIndex):
        self.id = id
        self.type = 'usually block'
        self.x = x
        self.y = y
        self.color = color
        self.strokeWidth = strokeWidth
        self.strokeColor = strokeColor
        self.width = width
        self.height = height
        self.rx = rx
        self.partIndex = partIndex

    def get_svg(self):
        self.svg += "fill:" + self.color + ";"
        self.svg += "stroke:" + self.strokeColor + ";"
        self.svg += "stroke-width:" + str(self.strokeWidth) + "\""
        self.svg += " id=\"" + str(self.id) + "\""
        self.svg += " width=\"" + str(self.width) + "\""
        self.svg += " height=\"" + str(self.height) + "\""
        self.svg += " x=\"" + str(self.x) + "\""
        self.svg += " y=\"" + str(self.y) + "\""
        self.svg += " rx=\"" + str(self.rx) + "\"" + "/>"
        return self.svg

class Blade:
    svg = ''

    def __init__(self, bladeObject, x, y, coefficient, partIndex):
        self.bladeObject = bladeObject
        self.type = bladeObject['type']
        self.id = bladeObject['id']
        self.x = x
        self.y = y
        self.coefficient = coefficient
        self.partIndex = partIndex
        self.height = BLADE_HEIGHT * self.bladeObject['size']  * self.coefficient
        self.serverHeight = self.height - 2
        self.servers_info = []
        for server in bladeObject['settings']['servers']:
            self.servers_info.append({'id': server['id']})

    def build_server_info_for_links(self):
        self.servers_info = []
        currentX = self.x + 1
        countSections = self.bladeObject['settings']['count_sections']
        serverDefaultWidth = (PART_WIDTH - 1 * (countSections + 1)) / countSections
        for server in self.bladeObject['settings']['servers']:
            if not server['id']:
                currentX += serverDefaultWidth + 1
                continue
            serverX = {}
            serverX['id'] = server['id']
            currentWidth = server['size'] * (serverDefaultWidth + 1) - 1
            serverX['x'] = currentX + currentWidth / 2
            serverX['level'] = 1
            self.servers_info.append(serverX)
            currentX += currentWidth + 1

    def get_svg(self):
        countSections = self.bladeObject['settings']['count_sections']
        servers = self.bladeObject['settings']['servers']

        self.width = PART_WIDTH
        self.svg += Rect(self.id, self.x, self.y, BLADE_COLOR, BLADE_STOKE_COLOR, PART_WIDTH,
                          self.height, BLADE_RX, STROKE_WIDTH, self.partIndex).get_svg()

        serverDefaultWidth = (PART_WIDTH - 1 * (countSections + 1)) / countSections
        currentSections = 0
        currentX = self.x + 1
        elements = []

        for server in servers:

            if not server['id']:
                currentSections += 1
                currentX += serverDefaultWidth + 1
                continue

            currentSections += server['size']
            if currentSections > countSections:
                raise ValueError('Incorrect count of sections or servers configuration on blade')
            currentWidth = server['size'] * (serverDefaultWidth + 1) - 1
            elements.append(Rect(server['id'], currentX, self.y + 1, SERVER_COLOR, SERVER_STROKE_COLOR,
                              currentWidth, self.serverHeight, SERVER_RX, STROKE_WIDTH, i))
            currentX += currentWidth + 1

        for element in elements:
            self.svg += '\n' + element.get_svg()

        return self.svg

if IS_SCALE == True:
    len_parts = []
    len_max = 0
    for i in range(0, len(config['parts'])):
        len_parts.append(0)
        for object in config['parts'][i]['objects']:
            if object['type'] == 'block':
                len_parts[i] += BLOCK_HEIGHT * object['size']
            elif object['type'] == 'commutator':
                len_parts[i] += COMMUTATOR_HEIGHT * object['size']
            elif object['type'] == 'blade':
                len_parts[i] += BLADE_HEIGHT * object['size']
            else:
                raise ValueError(f'Incorrect type of object with id={object["id"]}')
            len_parts[i] += 1
        len_parts[i] -= 1
        len_max = max(len_max, len_parts[i])

    for i in range(0, len(config['parts'])):
        if len_parts[i] != len_max:
            config['parts'][i]['coefficient'] = \
                (len_max - len(config['parts'][i]['objects'])) / (len_parts[i] - len(config['parts'][i]['objects']))
        else:
            config['parts'][i]['coefficient'] = 1
else:
    for part in config['parts']:
        part['coefficient'] = 1

ids = set()
blocks = []
currentX = BEGIN_X
mainHeight = 0

for i in range(len(config['parts'])):
    part = config['parts'][i]

    currentY = BEGIN_Y
    for object in part['objects']:

        if object['id'] in ids:
            raise ValueError(f'Non unique id of object with id={object["id"]}')

        if object['type'] == 'block':
            color = BLOCK_COLOR
            strokeColor = BLOCK_STROKE_COLOR
            height = BLOCK_HEIGHT * object['size'] * part['coefficient']
            rx = BLOCK_RX

        elif object['type'] == 'commutator':
            if not object['commutator_type'] in COMMUTATOR_COLORS:
                raise ValueError(f'Incorrect type of commutator width id={object["id"]}')
            color = COMMUTATOR_COLORS[object['commutator_type']]
            strokeColor = COMMUTATOR_STROKE_COLOR
            height = COMMUTATOR_HEIGHT * object['size']  * part['coefficient']
            rx = COMMUTATOR_RX

        elif object['type'] == 'blade':
            blocks.append(Blade(object, currentX, currentY, part['coefficient'], i))
            currentY += BLADE_HEIGHT + 1
            continue

        else:
            raise ValueError(f'Incorrect type of object with id={object["id"]}')
        blocks.append(Rect(object['id'], currentX, currentY, color, strokeColor,
                           PART_WIDTH, height, rx, STROKE_WIDTH, partIndex=i))
        ids.add(object['id'])
        currentY += height + 1

    mainHeight = max(mainHeight, currentY)
    currentX += PART_WIDTH + PART_DIFFERENCE

def find_block(id):
    for block in blocks:
        if block.id == id:
            return block
    return None

def find_server(id):
    for block in blocks:
        if block.type == 'blade':
            for server in block.servers_info:
                if server['id'] == id:
                    return {'blade': block, 'server': server}
    return None

def get_partIndex_from_block_id(id):
    block = find_block(id)
    if block:
        return block.partIndex
    server_object = find_server(id)
    if server_object:
        return server_object['blade'].partIndex
    raise ValueError(f'No block or server with id={object["id"]}')

for link in config['links']:
    multi_parts = set()
    for object in link['objects']:
        partIndex = get_partIndex_from_block_id(object['id'])
        if partIndex == -1:
            raise ValueError(f'No part index for object with id={object["id"]}')
        multi_parts.add(partIndex)
    link['is_multi_parts'] = len(multi_parts) > 1

def add_level_to_parts(config_parts):
    parts = config_parts
    for part in parts:
        for object in part['objects']:
            object['left_level'] = 0
            object['right_level'] = 0
    return parts

def find_server_in_blade(blade, server_id):
    for server in blade['settings']['servers']:
        if server['id'] == server_id:
            return True
    return False

def update_link_level(parts, objects, is_multi_parts):
    if is_multi_parts:
        for object in objects:
            index_part = get_partIndex_from_block_id(object['id'])
            was_block = False
            for block in parts[index_part]['objects']:
                if block['id'] == object['id'] or (block['type'] == 'blade' and find_server_in_blade(block, object['id'])):
                    was_block = True
                if was_block:
                    block[f'{object["side"]}_level'] += 1
    else:
        index_part = get_partIndex_from_block_id(objects[0]['id'])
        max_block_index = 0
        min_block_index = 10000000
        for i in range(len(parts[index_part]['objects'])):
            block = parts[index_part]['objects'][i]
            for object in objects:
                if object['id'] == block['id'] or (block['type'] == 'blade' and find_server_in_blade(block, object['id'])):
                    max_block_index = max(max_block_index, i)
                    min_block_index = min(min_block_index, i)
        new_level = 0
        for i in range(min_block_index, max_block_index + 1):
            new_level = max(new_level, parts[index_part]['objects'][i][f'{objects[0]["side"]}_level'] + 1)
        for i in range(min_block_index, max_block_index + 1):
            parts[index_part]['objects'][i][f'{objects[0]["side"]}_level'] = new_level
    return parts


parts = add_level_to_parts(config['parts'])
for link in config['links']:
    parts = update_link_level(parts, link['objects'], link['is_multi_parts'])

for block in blocks:
    if block.partIndex != -1:
        block.x += max(object['left_level'] for object in parts[block.partIndex]['objects']) * PATH_WIDTH
        prev_parts_diff = 0
        for i in range(block.partIndex):
            prev_parts_diff += \
                (max(object['left_level'] for object in parts[i]['objects']) + \
                 max(object['right_level'] for object in parts[i]['objects']))
        block.x += prev_parts_diff * PATH_WIDTH


class Link:
    svg = ''

    def __init__(self, id, strokeColor, strokeWidth):
        self.id = id
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.paths_blocks = []
        self.paths_servers = []
        self.paths_parts = []
        self.paths_multi = []
        self.end_parts = set()

    def add_path_block(self, block, side, link_level):
        path = {}
        if side == 'left':
            path['begin_x'] = block.x
            path['begin_y'] = block.y + 0.5 * block.height
            path['end'] = path['begin_x'] - link_level[block.partIndex] * PATH_WIDTH
        elif side == 'right':
            path['begin_x'] = block.x + block.width
            path['begin_y'] = block.y + 0.5 * block.height
            path['end'] = path['begin_x'] + link_level[block.partIndex] * PATH_WIDTH
        self.paths_blocks.append(path)

    def add_path_server(self, blade, server, side, link_level, all_links):
        server_path = {}
        server_path['begin_x'] = server['x']
        server_path['begin_y'] = blade.y + blade.height - server['level'] - 1
        server_path['end'] = blade.y + blade.height - server['level']
        server_path['blade_id'] = blade.id
        self.paths_servers.append(server_path)

        for link in all_links:
            for path_server in link.paths_servers:
                if path_server['blade_id'] == blade.id:
                    path_server['begin_y'] = server_path['begin_y']

        path = {}
        path['begin_x'] = server['x']
        path['begin_y'] = server_path['end']
        if side == 'left':
            path['end'] = path['begin_x'] - (server['x'] - blade.x) - link_level[blade.partIndex] * PATH_WIDTH
        elif side == 'right':
            path['end'] = path['begin_x'] + (blade.x + PART_WIDTH - server['x']) + link_level[blade.partIndex] * PATH_WIDTH
        self.paths_blocks.append(path)


    def add_path_parts(self, coord, end):
        min_y = 1000000000
        for path in self.paths_blocks:
            if path['end'] == coord:
                min_y = min(min_y, path['begin_y'])
        path = {}
        path['begin_y'] = min_y
        path['begin_x'] = coord
        path['end'] = end
        self.paths_parts.append(path)
        self.end_parts.add(end)

    def add_path_one_part(self):
        min_y = 1000000000
        max_y = 0
        for path in self.paths_blocks:
            min_y = min(min_y, path['begin_y'])
            max_y = max(max_y, path['begin_y'])
        path = {}
        path['begin_y'] = min_y
        path['begin_x'] = self.paths_blocks[0]['end']
        path['end'] = max_y
        self.paths_parts.append(path)

    def add_path_another_part(self, coord_multi_links):
        maximums_y = {}
        max_x = 0
        min_x = 1000000000
        for path in self.paths_blocks:
            max_x = max(max_x, path['end'])
            min_x = min(min_x, path['end'])
            if path['end'] not in maximums_y:
                maximums_y[path['end']] = path['begin_y']
            else:
                maximums_y[path['end']] = max(path['begin_y'], maximums_y[path['end']])
        for maximum in maximums_y.items():
            path = {}
            path['begin_x'] = maximum[0]
            path['begin_y'] = maximum[1]
            path['end'] = coord_multi_links
            self.paths_parts.append(path)
        path = {}
        path['begin_y'] = coord_multi_links
        path['begin_x'] = min_x
        path['end'] = max_x
        self.paths_multi.append(path)

    def get_svg(self):
        self.svg += f'\t<g id="{self.id}" style="fill:none;stroke:{self.strokeColor};stroke-width:{self.strokeWidth}">'
        for path in self.paths_blocks:
            self.svg += f'\n\t\t<path d="M {path["begin_x"]} {path["begin_y"]} H {path["end"]}"/>'
        for path in self.paths_servers:
            self.svg += f'\n\t\t<path d="M {path["begin_x"]} {path["begin_y"] - 0.15} V {path["end"] + 0.15}"/>'
        for path in self.paths_parts:
            self.svg += f'\n\t\t<path d="M {path["begin_x"]} {path["begin_y"] - 0.15} V {path["end"] + 0.15}"/>'
        for path in self.paths_multi:
            self.svg += f'\n\t\t<path d="M {path["begin_x"]} {path["begin_y"]} H {path["end"]}"/>'
        self.svg += '\n\t</g>'
        return self.svg

def update_coord(objects):
    result = {}
    for object in objects:
        block = find_block(object['id'])
        if block.partIndex not in result:
            result[block.partIndex] = [object['side']]
        elif object['side'] not in result[block.partIndex]:
            result[block.partIndex].append(object['side'])
    return result

coord_links = [{'left': 0, 'right': 0} for i in range(len(config['parts']))]
max_y = 0
for block in blocks:
    coord_links[block.partIndex]['left'] = block.x - 1
    coord_links[block.partIndex]['right'] = block.x + PART_WIDTH + 1
    max_y = max(max_y, block.y + block.height)
coord_multi_links = max_y + 1


def get_link_level(parts, objects, is_multi_parts):
    levels = [1 for i in range(len(parts))]
    if is_multi_parts:
        for object in objects:
            index_part = get_partIndex_from_block_id(object['id'])
            was_block = False
            for block in parts[index_part]['objects']:
                if block['id'] == object['id'] or (block['type'] == 'blade' and find_server_in_blade(block, object['id'])):
                    was_block = True
                if was_block:
                    levels[index_part] = max(levels[index_part], block[f'{object["side"]}_level'] + 1)
    else:
        index_part = get_partIndex_from_block_id(objects[0]['id'])
        max_block_index = 0
        min_block_index = 10000000
        for i in range(len(parts[index_part]['objects'])):
            block = parts[index_part]['objects'][i]
            for object in objects:
                if object['id'] == block['id'] or (block['type'] == 'blade' and find_server_in_blade(block, object['id'])):
                    max_block_index = max(max_block_index, i)
                    min_block_index = min(min_block_index, i)
        for i in range(min_block_index, max_block_index + 1):
            levels[index_part] = max(levels[index_part], parts[index_part]['objects'][i][f'{objects[0]["side"]}_level'] + 1)
    return levels


def update_link_level_server(blade, server, side):
    max_level = 0
    for i in range(len(blade.servers_info)):
        max_level = max(max_level, blade.servers_info[i]['level'])
    for i in range(len(blade.servers_info)):
        if  blade.servers_info[i]['id'] == server['id']:
            if (side == 'left'):
                for j in range(i + 1):
                    blade.servers_info[j]['level'] += 1
            elif (side == 'right'):
                for j in range(i, len(blade.servers_info)):
                    blade.servers_info[j]['level'] += 1
            else:
                raise ValueError(f'Incorrect side for server with id={server["id"]} in links')
    new_max_level = 0
    for i in range(len(blade.servers_info)):
        new_max_level = max(new_max_level, blade.servers_info[i]['level'])
    if max_level != new_max_level:
        blade.serverHeight -= 1
        if blade.serverHeight < 0.25 * blade.height:
            raise ValueError('Too small server height. Please increase blade height.')

for block in blocks:
    if block.type == 'blade':
        block.build_server_info_for_links()

parts = add_level_to_parts(config['parts'])
links = []
for link in config['links']:
    cur_link = Link(link['id'], COMMUTATOR_COLORS[link['type']], PATH_STROKE_WIDTH)
    link_level = get_link_level(parts, link['objects'], link['is_multi_parts'])
    for object in link['objects']:
        block = find_block(object['id'])
        if block:
            cur_link.add_path_block(block, object['side'], link_level)
            continue
        server_object = find_server(object['id'])
        if server_object:
            cur_link.add_path_server(server_object['blade'], server_object['server'], object['side'], link_level, links)
            update_link_level_server(server_object['blade'], server_object['server'], object['side'])
    if link['is_multi_parts']:
        cur_link.add_path_another_part(coord_multi_links)
        coord_multi_links += PATH_WIDTH
    else:
        cur_link.add_path_one_part()
    links.append(cur_link)
    parts = update_link_level(parts, link['objects'], link['is_multi_parts'])

diff = 0
for part in parts:
    diff += max(object['left_level'] for object in part['objects']) + \
               max(object['right_level'] for object in part['objects'])
mainWidth = currentX - 10 + BEGIN_X - 2 + 0.5 + PATH_WIDTH * diff
# учесть кол-во самых левых связей
mainHeight += BEGIN_Y - 1

print('<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100%\" height=\"100%\" viewBox=\"0 0 ' +
      str(mainWidth + 2) + ' ' + str(mainHeight + 2) + '\">')
main = Rect("main", 1, 1, MAIN_COLOR, MAIN_STROKE_COLOR,
            mainWidth, mainHeight, MAIN_RX, MAIN_STROKE_WIDTH, -1)

print(main.get_svg())

print("\t<text style=\"font-size:" + str(TEXT_SIZE) + ";fill:" + TEXT_COLOR + "\" x=\"" +
      str(mainWidth / 2) + "\" y=\"" + str(BEGIN_Y * 0.9) +
      "\" id=\"name\" text-anchor=\"middle\">SC name</text>")

for part in blocks:
    print(part.get_svg())

for link in links:
    print(link.get_svg())

print("</svg>")