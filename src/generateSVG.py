import json as js
import sys

with open("config1.json", "r") as readFile:
    config = js.load(readFile)

TEXT_SIZE = 4  #размер текста
TEXT_COLOR = "#000000"  # цвет текста

MAIN_COLOR = "#d0d0d0"  # цвет вычислительной стойки
MAIN_RX = 3  # закругление вычислительной стойки
MAIN_STROKE_COLOR = "#ffffff"  # цвет рамки вычислительной стойки

BLOCK_WIDTH = 40  # ширина блока
BLOCK_HEIGHT = 3  # высота блока
BLOCK_COLOR = "#6a6a6a"  # цвет блока
BLOCK_STROKE_COLOR = "#ffffff"  # цвет рамки блока
BLOCK_RX = 0.7  # закругление углов блоков
BLOCK_X = 8  # начальные значение координат блоков
BLOCK_Y = BLOCK_X * 1.5  # начальные значение координат блоков
blockX = BLOCK_X
blockY = BLOCK_Y

COMMUTATOR_WIDTH = BLOCK_WIDTH  # ширина коммутатора
COMMUTATOR_HEIGHT = 1  # высота коммутатора
COMMUTATOR_COLORS = ["#3e73a2", "#6b3fa1"]  # цвета коммутаторов разных типов
COMMUTATOR_STROKE_COLOR = "#ffffff"  # цвет рамки коммутатора
COMMUTATOR_RX = 0.7  # закругление углов коммутаторов
commutatorX = BLOCK_X  # начальные значение координат коммутаторов
commutatorY = BLOCK_Y  # начальные значение координат коммутаторов

BLADE_WIDTH = BLOCK_WIDTH  # ширина блейд-шасси
BLADE_HEIGHT = 20  # высота блейд-шасси
BLADE_COLOR = "#9e9e9e"  # цвет блейд-шасси
BLADE_STOKE_COLOR = "#ffffff"  # цвет рамки блейд-шасси
BLADE_RX = 0.7  # закругление углов блейд-шасси
bladeX = BLOCK_X  # начальные значения координа блейд-шасси
bladeY = BLOCK_Y  # начальные значения координа блейд-шасси

SERVER_COLOR = "#6a6a6a"  # цвет сервера в блейд-шасси
SERVER_STROKE_COLOR = "#ffffff"  # цвет рамки сервера в блейд-шасси
SERVER_RX = 0.7  # закругление углов сервера в блейд-шасси

PATH_WIDTH = 1  # расстояние между уровнями путей
PATH_STROKE_WIDTH = 0.5  # толщина путей


class Rect:
    id = ""
    x = 0
    y = 0
    svg = "<rect style=\""
    commutatorType = 0
    bladeCountServers = 0

    def __init__(self, id, x, y, commutatorType, bladeCountServers = 0):
        self.id = id
        self.x = x
        self.y = y
        self.commutatorType = commutatorType
        self.bladeCountServers = bladeCountServers

    def generateSvg(self, color, strokeColor, width, height, rx, strokeWidth):
        self.svg += "fill:" + color + ";"
        self.svg += "stroke:" + strokeColor + ";"
        self.svg += "stroke-width:" + str(strokeWidth) + "\""
        self.svg += " id=\"" + str(self.id) + "\""
        self.svg += " width=\"" + str(width) + "\""
        self.svg += " height=\"" + str(height) + "\""
        self.svg += " x=\"" + str(self.x) + "\""
        self.svg += " y=\"" + str(self.y) + "\""
        self.svg += " rx=\"" + str(rx) + "\"" + "/>"


def getBlocks(countBlocksInOnePul):
    global blockY
    blocks = []
    for i in range(0, countBlocks):
        blocks.append(Rect(blocksId[i], blockX, blockY, 0))
        blockY += BLOCK_HEIGHT
        if (i + 1) % countBlocksInOnePul == 0:
            blockY += 2
    return blocks


globalWidth = 0
globalHeight = 0
svgLeft = ""
svgRight = ""
name = ""
countParts = 0

if config['type'] == 1:

    name = config['name']
    countParts = config['parts']
    countBlocks = config['left']['countBlocks']
    blocksId = config['left']["blocks"]
    countBlocksInOnePul = config['left']['countBlocksInOnePul']
    countCommutators = config['left']['countCommutators']
    commutatorsDescription = config['left']['commutators']
    linkTypes = config['left']['linkTypes']
    linksIn = config['left']['links']['in']
    countLinksIn = len(linksIn)
    linksOut = config['left']['links']['out']
    countLinksOut = len(linksOut)

    blocks = getBlocks(countBlocksInOnePul)

    def takePlacesBlocksAndCommutators(shiftBlock):
        commutators = []
        for desc in commutatorsDescription:
            if desc[0] >= countBlocks + shiftBlock:
                yBegin = blocks[countBlocks - 1].y + BLOCK_HEIGHT
            else:
                yBegin = blocks[desc[0] - shiftBlock].y
            for i in range(desc[1]):
                for j in range(len(linkTypes)):
                    if desc[2][i][1] == linkTypes[j]:
                        commutators.append(Rect(desc[2][i][0], commutatorX, yBegin + 1 + i * COMMUTATOR_HEIGHT, j))
                        break
            for i in range(desc[0] - shiftBlock, countBlocks):
                blocks[i - shiftBlock].y += desc[1] * COMMUTATOR_HEIGHT + 2
        return commutators

    commutators = takePlacesBlocksAndCommutators(0)


    class Path:
        id = ""
        type = ""
        typeLink = 0
        level = 0
        count = 0
        elements = []
        svg = ""

        def __init__(self, id, type, level, typeLink, count, elements):
            self.id = "link" + type + str(id)
            self.type = type
            self.typeLink = typeLink
            self.count = count
            self.level = level
            self.elements = elements

        def generateSvg(self):
            self.svg = "<g id=\"" + self.id + "\" style=\"fill:none;"
            self.svg += "stroke:" + COMMUTATOR_COLORS[self.typeLink] + ";"
            self.svg += "stroke-width:" + str(PATH_STROKE_WIDTH) + "\">"
            minY = 10000000
            maxY = 0
            globalX = 0
            for elem in self.elements:
                self.svg += "\n\t\t<path "

                def findId(mas, id):
                    for i in range(len(mas)):
                        if mas[i].id == id:
                            return i
                    return -1

                i = findId(blocks, elem)
                parts = blocks
                width = BLOCK_WIDTH
                height = BLOCK_HEIGHT
                if i == -1:
                    i = findId(commutators, elem)
                    parts = commutators
                    width = COMMUTATOR_WIDTH
                    height = COMMUTATOR_HEIGHT
                if self.type == "Right":
                    self.svg += "d=\"M " + str(parts[i].x + width) + " "
                else:
                    self.svg += "d=\"M " + str(parts[i].x) + " "
                minY = min(minY, parts[i].y + height / 2)
                maxY = max(maxY, parts[i].y + height / 2)
                self.svg += str(parts[i].y + height / 2) + " H "
                if self.type == "Right":
                    globalX = parts[i].x + width + self.level * PATH_WIDTH
                    self.svg += str(globalX)
                else:
                    globalX = parts[i].x - self.level * PATH_WIDTH
                    self.svg += str(globalX)
                self.svg += "\"/>"
            self.svg += "\n\t\t<path "
            if self.type == "Right":
                self.svg += "d=\"M " + str(globalX) + " " + str(minY) + " "
            else:
                self.svg += "d=\"M " + str(globalX) + " " + str(minY) + " "
            self.svg += "V " + str(maxY) + "\"/>"
            self.svg += "\n\t</g>"

    paths = []
    maxPathLevel = 0
    maxPathLevelIn = 0

    def getLinksIn(shift):
        global maxPathLevel
        global maxPathLevelIn
        for j in range(len(linksIn)):
            maxPathLevel = max(maxPathLevel, linksIn[j][0])
            maxPathLevelIn = max(maxPathLevelIn, linksIn[j][0])
            for i in range(len(linkTypes)):
                if linksIn[j][1] == linkTypes[i]:
                    paths.append(Path(j + shift, "Right", linksIn[j][0], i, linksIn[j][2], linksIn[j][3]))
                    break

    getLinksIn(0)

    maxPathLevelOut = 0

    def getLinksOut(shift):
        global maxPathLevel
        global maxPathLevelOut
        for j in range(0, len(linksOut)):
            maxPathLevel = max(maxPathLevel, linksOut[j][0])
            maxPathLevelOut = max(maxPathLevelOut, linksOut[j][0])
            for i in range(0, len(linkTypes)):
                if linksOut[j][1] == linkTypes[i]:
                    paths.append(Path(j + shift, "Left", linksOut[j][0], i, linksOut[j][2], linksOut[j][3]))
                    break

    getLinksOut(0)

    def getSvg():
        svg = ""
        for i in range(0, countBlocks):
            blocks[i].x += maxPathLevelOut * PATH_WIDTH
            blocks[i].generateSvg(BLOCK_COLOR, BLOCK_STROKE_COLOR, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_RX, 0.1)
            svg += "\t" + blocks[i].svg + "\n"
        for i in range(0, countCommutators):
            commutators[i].x += maxPathLevelOut * PATH_WIDTH
            commutators[i].generateSvg(COMMUTATOR_COLORS[commutators[i].commutatorType],
                COMMUTATOR_STROKE_COLOR, COMMUTATOR_WIDTH, COMMUTATOR_HEIGHT, COMMUTATOR_RX, 0.1)
            svg += "\t" + commutators[i].svg + "\n"
        for i in range(maxPathLevel, -1, -1):
            for j in range(0, len(paths)):
                if paths[j].level == i:
                    paths[j].generateSvg()
                    svg += "\t" + paths[j].svg + "\n"
        return svg[:-1]

    svgLeft = getSvg()

    svgRight = ""
    maxY = blocks[len(blocks) - 1].y
    shiftCom = countCommutators
    shiftBlock = countBlocks
    blockX = BLOCK_X * 1.5 + PATH_WIDTH * maxPathLevelOut + max(BLOCK_WIDTH, COMMUTATOR_WIDTH) + PATH_WIDTH * maxPathLevelIn
    globalWidth = 2 * BLOCK_X + PATH_WIDTH * maxPathLevelOut + countParts * max(BLOCK_WIDTH, COMMUTATOR_WIDTH) + PATH_WIDTH * maxPathLevelIn

    if countParts == 2:
        countBlocks = config['right']['countBlocks']
        blocksId = config['right']['blocks']
        countBlocksInOnePul = config['right']['countBlocksInOnePul']
        countCommutators = config['right']['countCommutators']
        commutatorsDescription = config['right']['commutators']
        linkTypes = config['right']['linkTypes']
        linksIn = config['right']['links']['out']
        linksOut = config['right']['links']['in']

        blockY = BLOCK_Y
        commutatorX += PATH_WIDTH * maxPathLevelOut + max(BLOCK_WIDTH, COMMUTATOR_WIDTH) + PATH_WIDTH * maxPathLevelIn + BLOCK_X * 0.5
        blocks = getBlocks(countBlocksInOnePul)
        commutators = takePlacesBlocksAndCommutators(shiftBlock)

        paths = []
        maxPathLevel = 0
        maxPathLevelIn = 0
        getLinksIn(countLinksIn)
        maxPathLevelOut = 0
        getLinksOut(countLinksOut)

        svgRight = getSvg()

        globalWidth += PATH_WIDTH * maxPathLevelOut + PATH_WIDTH * maxPathLevelIn + BLOCK_X * 0.5

    globalHeight = max(maxY, blocks[countBlocks - 1].y + BLOCK_HEIGHT, commutators[countCommutators - 1].y + COMMUTATOR_HEIGHT) + BLOCK_X


if config['type'] == 2:

    name = config['name']
    countParts = 1
    countBlocks = config['countBlocks']
    blocksId = config['blocks']
    countBlades = config['countBlades']
    bladesDescription = config['blades']
    linkTypes = config['linkTypes']
    linksIn = config['links']['in']
    countLinksIn = len(linksIn)
    linksOut = config['links']['out']
    countLinksOut = len(linksOut)

    blocks = getBlocks(countBlocks)
    bladeY = blocks[countBlocks - 1].y + BLOCK_HEIGHT + 2

    def getBlades():
        global bladeY
        blades = []
        for i in range(countBlades):
            blades.append(Rect("blade" + str(i), bladeX, bladeY, 0, bladesDescription[i][0]))
            bladeY += BLADE_HEIGHT + 2
        return blades

    blades = getBlades()

    def takePlacesBlocksAndBlades():
        j = 0
        for desc in bladesDescription:
            if desc[1] >= countBlocks:
                yBegin = blocks[countBlocks - 1].y + BLOCK_HEIGHT
            else:
                yBegin = blocks[desc[1]].y
            blades[j].y = yBegin + 2
            for i in range(desc[1], countBlocks):
                blocks[i].y += BLADE_HEIGHT + 4
            j += 1

    takePlacesBlocksAndBlades()

    def getSvg():
        svg = ""
        for i in range(countBlocks):
            blocks[i].generateSvg(BLOCK_COLOR, BLOCK_STROKE_COLOR, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_RX, 0.1)
            svg += "\t" + blocks[i].svg + "\n"
        for i in range(countBlades):
            blades[i].generateSvg(BLADE_COLOR, BLADE_STOKE_COLOR, BLADE_WIDTH, BLADE_HEIGHT, BLADE_RX, 0.1)
            svg += "\t" + blades[i].svg + "\n"
            serverWidth = (BLADE_WIDTH - 4 - (bladesDescription[i][0] - 1)) / bladesDescription[i][0]
            currentX = blades[i].x + 2
            for j in range(len(bladesDescription[i][2])):
                if (len(bladesDescription[0][2][j]) > 0):
                    server = Rect(bladesDescription[i][2][j][0], currentX, blades[i].y + 1, 0)
                    currentWidth = serverWidth * bladesDescription[i][2][j][1] + (bladesDescription[i][2][j][1] - 1) * 1
                    server.generateSvg(SERVER_COLOR, SERVER_STROKE_COLOR, currentWidth, BLADE_HEIGHT - 2, SERVER_RX, 0.1)
                    svg += "\t" + server.svg + "\n"
                    currentX += currentWidth + 1
                else:
                    currentX += serverWidth + 1
        return svg[:-1]

    svgLeft = getSvg()

    globalWidth = 2 * BLOCK_X + BLOCK_WIDTH
    globalHeight = max(blocks[countBlocks - 1].y + BLOCK_HEIGHT, blades[countBlades - 1].y + BLADE_HEIGHT) + BLOCK_X

print("export const SVGPanelCode = `")
main = Rect("main", BLOCK_X * 0.5, BLOCK_X * 0.5, 0)
main.generateSvg(MAIN_COLOR, MAIN_STROKE_COLOR, globalWidth - BLOCK_X, globalHeight - BLOCK_X, MAIN_RX, 0.8)
# print("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" + str(globalWidth) + "mm\" height=\"" +
#       str(globalHeight) + "mm\" viewBox=\"0 0 " + str(globalWidth) + " " + str(globalHeight) + "\">")
print("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100%\" height=\"100%\" viewBox=\"0 0 " +
      str(globalWidth) + " " + str(globalHeight) + "\">")
print("\t" + main.svg)
print("\t<text style=\"font-size:" + str(TEXT_SIZE) + ";fill:" + TEXT_COLOR + "\" x=\"" +
      str((globalWidth - TEXT_SIZE * 0.5 * len(name)) * 0.5) + "\" y=\"" + str(BLOCK_X + TEXT_SIZE * 0.5) +
      "\" id=\"name\">" + name + "</text>")
print(svgLeft)
if countParts == 2:
    print(svgRight)
print("</svg>`")