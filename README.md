# cramfs
Library for read Compressed romfs images


# Библиотека для чтения образов Cramfs (Compressed romfs). Является частью проекта моего PokerCook - программы для работы с образами электронных книг PoketBook

## Возможности:
* в качестве источника можно использовать диск, файл, файлоподобный объект или байты
* можно явно указывать оффсет
* просмотр списка объектов
* переход в нужную папку и возврат в корневой каталог
* чтение файлов и символьных ссылок
* получение информации об объекте (имя, тип, размер, uid, права на исполнение, chmod)

Пример работы с библиотекой:
```python
# импорт библиотеки
from cramfs import cramFS

filename = "example.img" # указываем необходимый образ/диск/байты или объект BytesIO
offset = 512 # указываем смещение, по которому в файле находится образ cramfs (по-умолчанию offset = 0)

# работа с библиотекой
test = cramFS(filename, offset)

# получаем список объектов в корневой папке
files = test.ls()
for file in files:
    print(file)

test.cd('lib') # переходим в папку lib

print(test.pwd()) # убеждаемся, что мы находимся в папке lib
print(test.read('libcharset.so.1.0.0')) # читаем файл libcharset.so.1.0.0 из папки lib

print(test.cd('alsa-lib')) # переходим в папку alsa-lib внутри папки lib

# получаем список объектов в папке alsa-lib
files = test.ls()
for file in files:
    print(file)

test.cd('/') # возвращаемся в корневую папку

print(test.read('bin/restore.sh').decode()) # выводим скрипт restore.sh из папки bin
```
