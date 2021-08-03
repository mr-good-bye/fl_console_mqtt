import flux_led as f_l
import pickle

commands = {}
data = {}
first_launch = True

#data:
#{id: {ip, working, name, model, working}}
#scanner.scanned:
#[{ipaddr, id, model}]

def discover():
    scanner = f_l.BulbScanner()
    scanner.scan(timeout = 6)
    for i in scanner.found_bulbs:
        bulb = f_l.WifiLedBulb(i['ipaddr'])
        bulb.turnOff()
    if first_launch:
        for i in data:
            data[i]['working'] = False
        first_launch = False
    for i in scanner.found_bulbs:
        id = i['id']
        if id in data:
            data[id]['ip'] = i['ipaddr']
            data[id]['working'] = True
            data[id]['model'] = i['model']
            print(data[id]['name'] + " подключено")
        else:
            bulb = f_l.WifiLedBulb(i['ipaddr'])
            bulb.turnOn()
            bulb.setRgb(255, 0, 0)
            name = input('Введите имя для ленты горящей красным: ')
            bulb.turnOff()
            data[id] = {}
            data[id]['ip'] = i['ipaddr']
            data[id]['name'] = name
            data[id]['model'] = i['model']
            data[id]['working'] = True
    for i in data:
        if not data[i]['working']:
            print(data[i]['name'] + "Не подключена. Если должна быть, повторите поиск")
    save()      
commands['обнаружить'] = discover

def help():
    for i in commands:
        print(i)
commands['помощь'] = help

def load():
    global data
    try:
        f_data = open('LEDS.pickle', 'rb')
        data = pickle.load(f_data)
        f_data.close()
        print('Загружено')
    except:
        print("Нет файла")
        return
    if len(data) == 0: return
    show()
commands['загрузить'] = load

def rename():
    print("==========Список==========")
    for i in data:
        print(i +': ' + data[i]['name'])
    print("==========================")
    i_n = input('Введите id или имя для переименования: ')
    if i_n in data:
        data[i_n]['name'] = input('Введите новое имя: ')
    else:
        for i in data:
            if data[i]['name'] == i_n:
                data[i]['name'] = input('Введите новое имя: ')
commands['переименовать'] = rename

def show():
    print("==========Список==========")
    for i in data:
        print(i +": " + data[i]['name'])
    print("==========================")
commands['отобразить'] = show

commands['выход'] = print

def save():
    f_data = open('LEDS.pickle', 'wb')
    pickle.dump(data, f_data)
    f_data.close()
    print('Сохранено!')
commands['сохранить'] = save

def delete():
    print("==========Список==========")
    for i in data:
        print(i +": " + data[i]['name'])
    print("==========================")
    i_n = input('Введите id или имя для удаления: ')
    if i_n in data:
        if input('Точно? д/н') == 'д':
            data.pop(i_n)
        else:
            return
    else:
        for i in data:
            if data[i]['name'] == i_n:
                if input('Точно? д/н') == 'д':
                    data.pop(i)
                else:
                    return
commands['удалить'] = delete

def setled():
    print("==========Список==========")
    for i in data:
        print(i +': ' + data[i]['name'])
    print("==========================")
    i_n = input('Введите id или имя для установки: ')
    led = ''
    if i_n in data:
        led = i_n
    else:
        for i in data:
            if data[i]['name'] == i_n:
                led = i
    if led == '':
        print('Неверные данные')
        return
    bulb = f_l.WifiLedBulb(data[led]['ip'])
    print("0-255")
    r = int(input("Красный:"))
    g = int(input("Зелёный:"))
    b = int(input("Синий:"))
    bulb.setRgb(r, g, b)
commands['установить'] = setled

def set_all():
    print("0-255")
    r = int(input("Красный:"))
    g = int(input("Зелёный:"))
    b = int(input("Синий:"))
    for i in data:
        bulb = f_l.WifiLedBulb(data[i]['ip'])
        bulb.setRgb(r,g,b)
commands['установить все'] = set_all

def all():
    o = input("вкл/выкл: ")
    if o == 'выкл':
        for i in data:
            bulb = f_l.WifiLedBulb(data[i]['ip'])
            bulb.turnOff()
    elif o == 'вкл':
        for i in data:
            bulb = f_l.WifiLedBulb(data[i]['ip'])
            bulb.turnOn()
    else:
        print("Неверные данные")
commands['переключить все'] = all

load()
inp = ''
print('помощь для списка команд')
while inp != 'выход':
    inp = input('~Pantheon > ')
    if inp in commands:
        commands[inp]()
    else:
        print('Команда не найдена')
save()
