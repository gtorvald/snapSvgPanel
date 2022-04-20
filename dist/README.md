# SnapSVG плагин

SnapSVG плагин для Grafana.

## Установка плагина локально

1. Перейдите в директорию, указанную в вашей конфигурации Grafana в разделе [paths] : plugins.
2. Склонируйте репозиторий в эту директорию.
```
git clone https://github.com/gtorvald/snapSvgPanel.git
```
3. Установите зависимости и запустите плагин.
```
npm install
grunt
```
4. Перезапустите grafana.
Для MacOS:
```
brew services restart grafana
```
