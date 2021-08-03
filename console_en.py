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
            print(data[id]['name'] + " connected")
        else:
            bulb = f_l.WifiLedBulb(i['ipaddr'])
            bulb.turnOn()
            bulb.setRgb(255, 0, 0)
            name = input('Input name for a red led: ')
            bulb.turnOff()
            data[id] = {}
            data[id]['ip'] = i['ipaddr']
            data[id]['name'] = name
            data[id]['model'] = i['model']
            data[id]['working'] = True
    for i in data:
        if not data[i]['working']:
            print(data[i]['name'] + "not connected. Try discover again")
    save()      
commands['discover'] = discover

def help():
    for i in commands:
        print(i)
commands['help'] = help

def load():
    global data
    try:
        f_data = open('LEDS.pickle', 'rb')
        data = pickle.load(f_data)
        f_data.close()
        print('Loaded')
    except:
        print("No file")
        return
    if len(data) == 0: return
    show()
commands['load'] = load

def rename():
    print("===========LIST===========")
    for i in data:
        print(i +': ' + data[i]['name'])
    print("==========================")
    i_n = input('Input id or name to rename: ')
    if i_n in data:
        data[i_n]['name'] = input('Input new name: ')
    else:
        for i in data:
            if data[i]['name'] == i_n:
                data[i]['name'] = input('Input new name: ')
commands['rename'] = rename

def show():
    print("==========LIST==========")
    for i in data:
        print(i +": " + data[i]['name'])
    print("==========================")
commands['show'] = show

commands['exit'] = print

def save():
    f_data = open('LEDS.pickle', 'wb')
    pickle.dump(data, f_data)
    f_data.close()
    print('Saved!')
commands['save'] = save

def delete():
    print("===========LIST===========")
    for i in data:
        print(i +": " + data[i]['name'])
    print("==========================")
    i_n = input('Input id or name to delete: ')
    if i_n in data:
        if input('Are you sure? y/n') == 'y':
            data.pop(i_n)
        else:
            return
    else:
        for i in data:
            if data[i]['name'] == i_n:
                if input('Are you sure? y/n') == 'y':
                    data.pop(i)
                else:
                    return
commands['delete'] = delete

def setled():
    print("===========LIST===========")
    for i in data:
        print(i +': ' + data[i]['name'])
    print("==========================")
    i_n = input('Input id or name to set: ')
    led = ''
    if i_n in data:
        led = i_n
    else:
        for i in data:
            if data[i]['name'] == i_n:
                led = i
    if led == '':
        print('Incorrent data')
        return
    bulb = f_l.WifiLedBulb(data[led]['ip'])
    print("0-255")
    r = int(input("Red:"))
    g = int(input("Green:"))
    b = int(input("Blue:"))
    bulb.setRgb(r, g, b)
commands['set'] = setled

def set_all():
    print("0-255")
    r = int(input("Red:"))
    g = int(input("Green:"))
    b = int(input("Blue:"))
    for i in data:
        bulb = f_l.WifiLedBulb(data[i]['ip'])
        bulb.setRgb(r,g,b)
commands['set all'] = set_all

def all():
    o = input("on/off: ")
    if o == 'off':
        for i in data:
            bulb = f_l.WifiLedBulb(data[i]['ip'])
            bulb.turnOff()
    elif o == 'on':
        for i in data:
            bulb = f_l.WifiLedBulb(data[i]['ip'])
            bulb.turnOn()
    else:
        print("Incorrect input")
commands['turn all'] = all


load()
inp = ''
print('help to get commands list')
while inp != 'exit':
    inp = input('~Pantheon > ')
    if inp in commands:
        commands[inp]()
    else:
        print('command not found')
save()
