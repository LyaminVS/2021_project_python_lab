# Dolgopio

**чтобы запустить игру, нужно запустить файл main.py**


пиксельный симулятор-стратегия управления студентом

предыстория: в 2048 году на Долгопрудный обрушился шквал гнева студентов ФРКТ, кампус МФТИ разрушен, не осталось ни одной живой души. остался только засидевшийся в боталке фопф, перед которым теперь стоит задача с помощью ландафшица и ресурсов своего мозга восстановить кампус.

цель: восстановить НК, КПМ, КСП, БИО и ЛК после нашествия ртшников

над проектом работали:

Лямин Василий - main.py, background.py

Тюрников Алексей - menu.py, start_screen.py, main.py

Моргай Ангелина - map_logic.py

Ханина Виктория - objects.py, constants.py, pics/

модули:

main.py - связывающий модуль игры, сохранение данных в файлы, распаковка данных из файлов

background.py - модуль, отвечающий за отрисовку фона и сеток строительства

menu.py - модуль, описывающий класс инвентарей

start_screen.py - модуль со стартовыми меню и кнопками

map_logic.py - модуль, отвечающий за логику игры: реализация и ограничение движения, коллизия, ивентчекеры

objects.py - модуль с описанием класса объектов

constants.py - модуль, хранящий цветовые константы

испольуемые библиотеки: pygame, os, shutil