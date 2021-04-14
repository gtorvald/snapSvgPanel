import json as js
import sys

TEXT_SIZE = 4  #размер текста
TEXT_COLOR = "#000000"  # цвет текста

MAIN_COLOR = "#d0d0d0"  # цвет вычислительной стойки
MAIN_RX = 3  # закругление вычислительной стойки
MAIN_STROKE_COLOR = "#ffffff"  # цвет рамки вычислительной стойки

BLOCK_RX = 0.7  # закругление углов блоков
BLOCK_WIDTH = 30  # ширина блока
BLOCK_HEIGHT = 3  # высота блока
BLOCK_COLOR = "#6a6a6a"  # цвет блока
BLOCK_STROKE_COLOR = "#ffffff"  # цвет рамки блока
BLOCK_X = 8  # начальные значение координат блоков
BLOCK_Y = BLOCK_X * 1.5  # начальные значение координат блоков

commutatorX = BLOCK_X  # начальные значение координат коммутаторов
commutatorY = BLOCK_Y  # начальные значение координат коммутаторов
COMMUTATOR_WIDTH = BLOCK_WIDTH  # ширина коммутатора
COMMUTATOR_HEIGHT = 1  # высота коммутатора
COMMUTATOR_COLORS = ["#3e73a2", "#6b3fa1"]  # цвета коммутаторов разных типов
COMMUTATOR_STROKE_COLOR = "#ffffff"  # цвет рамки коммутатора
COMMUTATOR_RX = 0.7  # закругление углов коммутаторов

PATH_WIDTH = 1  # расстояние между уровнями путей
PATH_STROKE_WIDTH = 0.5  # толщина путей

with open("config.json", "r") as readFile:
    config = js.load(readFile)
countBlocks = config['left']['countBlocks']
countBlocksInOnePul = config['left']['countBlocksInOnePul']
countCommutators = config['left']['countCommutators']
commutatorsDescription = config['left']['commutators']
linkTypes = config['left']['linkTypes']
linksIn = config['left']['links']['in']
countLinksIn = len(linksIn)
linksOut = config['left']['links']['out']
countLinksOut = len(linksOut)


class Rect:
    id = ""
    x = 0
    y = 0
    svg = "<rect style=\""
    commutatorType = 0

    def __init__(self, type, num, x, y, commutatorType):
        self.id = type + str(num)
        self.x = x
        self.y = y
        self.commutatorType = commutatorType

    def generateSvgMain(self, width, height):
        self.svg += "fill:" + MAIN_COLOR + ";"
        self.svg += "stroke:" + MAIN_STROKE_COLOR + ";"
        self.svg += "stroke-width:0.8\""
        self.svg += " id=\"" + str(self.id) + "\""
        self.svg += " width=\"" + str(width) + "\""
        self.svg += " height=\"" + str(height) + "\""
        self.svg += " x=\"" + str(self.x) + "\""
        self.svg += " y=\"" + str(self.y) + "\""
        self.svg += " rx=\"" + str(MAIN_RX) + "\"" + "/>"

    def generateSvgBlock(self):
        self.svg += "fill:" + BLOCK_COLOR + ";"
        self.svg += "stroke:" + BLOCK_STROKE_COLOR + ";"
        self.svg += "stroke-width:0.1\""
        self.svg += " id=\"" + str(self.id) + "\""
        self.svg += " width=\"" + str(BLOCK_WIDTH) + "\""
        self.svg += " height=\"" + str(BLOCK_HEIGHT) + "\""
        self.svg += " x=\"" + str(self.x) + "\""
        self.svg += " y=\"" + str(self.y) + "\""
        self.svg += " rx=\"" + str(BLOCK_RX) + "\"" + "/>"

    def generateSvgCommutator(self):
        self.svg += "fill:" + COMMUTATOR_COLORS[self.commutatorType] + ";"
        self.svg += "stroke:" + BLOCK_STROKE_COLOR + ";"
        self.svg += "stroke-width:0.1\""
        self.svg += " id=\"" + str(self.id) + "\""
        self.svg += " width=\"" + str(COMMUTATOR_WIDTH) + "\""
        self.svg += " height=\"" + str(COMMUTATOR_HEIGHT) + "\""
        self.svg += " x=\"" + str(self.x) + "\""
        self.svg += " y=\"" + str(self.y) + "\""
        self.svg += " rx=\"" + str(COMMUTATOR_RX) + "\"" + "/>"

blockX = BLOCK_X
blockY = BLOCK_Y

def getBlocks(shift):
    global blockY
    blocks = []
    for i in range(0, countBlocks):
        blocks.append(Rect("block", i + shift, blockX, blockY, 0))
        blockY += BLOCK_HEIGHT
        if (i + 1) % countBlocksInOnePul == 0:
            blockY += 2
    return blocks

blocks = getBlocks(0)

def getCommutators(shift):
    commutators = []
    for i in range(0, countCommutators):
        commutators.append(Rect("commutator", i + shift, commutatorX, commutatorY, 0))
    return commutators

commutators = getCommutators(0)

def takePlacesBlocksAndCommutators(shiftCom, shiftBlock):
    for desc in commutatorsDescription:
        for i in range(0, desc[1]):
            commutators[desc[2][i][0] - shiftCom].y = blocks[desc[0] - shiftBlock].y + 1 + i * COMMUTATOR_HEIGHT
            for j in range(0, len(linkTypes)):
                if desc[2][i][1] == linkTypes[j]:
                    commutators[desc[2][i][0] - shiftCom].commutatorType = j
                    break
        for i in range(desc[0] - shiftBlock, countBlocks):
            blocks[i - shiftBlock].y += desc[1] * COMMUTATOR_HEIGHT + 2

takePlacesBlocksAndCommutators(0, 0)


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

    def generateSvg(self, shiftCom, shiftBlock):
        self.svg = "<g id=\"" + self.id + "\" style=\"fill:none;"
        self.svg += "stroke:" + COMMUTATOR_COLORS[self.typeLink] + ";"
        self.svg += "stroke-width:" + str(PATH_STROKE_WIDTH) + "\">"
        minY = 10000000
        maxY = 0
        globalX = 0
        for elem in self.elements:
            self.svg += "\n\t\t<path "
            if elem.find("block") != -1:
                i = int(elem[5:])
                parts = blocks
                shift = shiftBlock
                width = BLOCK_WIDTH
                height = BLOCK_HEIGHT
            else:
                i = int(elem[3:])
                parts = commutators
                shift = shiftCom
                width = COMMUTATOR_WIDTH
                height = COMMUTATOR_HEIGHT
            if self.type == "Right":
                self.svg += "d=\"M " + str(parts[i - shift].x + width) + " "
            else:
                self.svg += "d=\"M " + str(parts[i - shift].x) + " "
            minY = min(minY, parts[i - shift].y + height / 2)
            maxY = max(maxY, parts[i - shift].y + height / 2)
            self.svg += str(parts[i - shift].y + height / 2) + " H "
            if self.type == "Right":
                globalX = parts[i - shift].x + width + self.level * PATH_WIDTH
                self.svg += str(globalX)
            else:
                globalX = parts[i - shift].x - self.level * PATH_WIDTH
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
    for j in range(0, len(linksIn)):
        maxPathLevel = max(maxPathLevel, linksIn[j][0])
        maxPathLevelIn = max(maxPathLevelIn, linksIn[j][0])
        for i in range(0, len(linkTypes)):
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

def getSvg(shiftCom, shiftBlock):
    svg = ""
    for i in range(0, countBlocks):
        blocks[i].x += maxPathLevelOut * PATH_WIDTH
        blocks[i].generateSvgBlock()
        svg += "\t" + blocks[i].svg + "\n"
    for i in range(0, countCommutators):
        commutators[i].x += maxPathLevelOut * PATH_WIDTH
        commutators[i].generateSvgCommutator()
        svg += "\t" + commutators[i].svg + "\n"
    for i in range(maxPathLevel, -1, -1):
        for j in range(0, len(paths)):
            if paths[j].level == i:
                paths[j].generateSvg(shiftCom, shiftBlock)
                svg += "\t" + paths[j].svg + "\n"
    return svg

svgLeft = getSvg(0, 0)

maxY = blocks[len(blocks) - 1].y
shiftCom = countCommutators
shiftBlock = countBlocks
name = config['name']
countBlocks = config['right']['countBlocks']
countBlocksInOnePul = config['right']['countBlocksInOnePul']
countCommutators = config['right']['countCommutators']
commutatorsDescription = config['right']['commutators']
linkTypes = config['right']['linkTypes']
linksIn = config['right']['links']['out']
linksOut = config['right']['links']['in']

blockX = BLOCK_X * 1.5 + PATH_WIDTH * maxPathLevelOut + max(BLOCK_WIDTH, COMMUTATOR_WIDTH) + PATH_WIDTH * maxPathLevelIn
globalWidth = 2 * BLOCK_X + PATH_WIDTH * maxPathLevelOut + 2 * max(BLOCK_WIDTH, COMMUTATOR_WIDTH) + PATH_WIDTH * maxPathLevelIn
blockY = BLOCK_Y
commutatorX += PATH_WIDTH * maxPathLevelOut + max(BLOCK_WIDTH, COMMUTATOR_WIDTH) + PATH_WIDTH * maxPathLevelIn + BLOCK_X * 0.5
blocks = getBlocks(shiftBlock)
commutators = getCommutators(shiftCom)
takePlacesBlocksAndCommutators(shiftCom, shiftBlock)

paths = []
maxPathLevel = 0
maxPathLevelIn = 0
getLinksIn(countLinksIn)
maxPathLevelOut = 0
getLinksOut(countLinksOut)

svgRight = getSvg(shiftCom, shiftBlock)

globalWidth += PATH_WIDTH * maxPathLevelOut + PATH_WIDTH * maxPathLevelIn + BLOCK_X * 0.5
globalHeight = max(maxY, blocks[len(blocks) - 1].y) + BLOCK_HEIGHT + BLOCK_X
main = Rect("main", "", BLOCK_X * 0.5, BLOCK_X * 0.5, 0)
main.generateSvgMain(globalWidth - BLOCK_X, globalHeight - BLOCK_X)
print("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" + str(globalWidth) + "mm\" height=\"" + str(globalHeight) + "mm\" viewBox=\"0 0 " + str(globalWidth) + " " + str(globalHeight) + "\">")
print("\t" + main.svg)
print("\t<text style=\"font-size:" + str(TEXT_SIZE) + ";fill:" + TEXT_COLOR + "\" x=\"" + str((globalWidth - TEXT_SIZE * 0.5 * len(name)) * 0.5) + "\" y=\"" + str(BLOCK_X + TEXT_SIZE * 0.5) + "\" id=\"name\">" + name + "</text>")
print(svgLeft + svgRight + "</svg>")
