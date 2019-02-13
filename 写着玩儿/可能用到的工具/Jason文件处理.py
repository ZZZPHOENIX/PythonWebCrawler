import json
import datetime

periods = {
    '1': '8:00~9:40',
    '2': '10:00~11:40',
    '3': '14:00~15:40',
    '4': '16:00~17:40',
    '5': '19:00~20:40',
}

buildings = {
    'A': '500137',
    'B': '500138',
    'C': '500139',
    'D': '500140',
    '升华前楼': '500153',
    '科教南楼': '500154',
    '科教北楼': '500155',
}

'''
with open('空教室/B座-2018-11-14.json') as f:
    content = f.read()

a = json.loads(content)
leisure_room = {}
for i in a['obj']['roomlist']:
    for period in i['record']:
        if 1 <= period['room_period'] <= 5 and period['room_state'] == '0':
            if i['room_name'] not in leisure_room:
                leisure_room[i['room_name']] = []
            leisure_room[i['room_name']].append(periods[str(period['room_period'])])

for item in leisure_room:
    print(item, end='\t')
    for period in leisure_room[item]:
        print(period, end='\t')
    print('')
'''
periods = {
            '1': '8:00~9:40',
            '2': '10:00~11:40',
            '3': '14:00~15:40',
            '4': '16:00~17:40',
            '5': '19:00~20:40',
        }

leisure_room = {
    '1': [],
    '2': [],
    '3': [],
    '4': [],
    '5': [],
}

with open('空教室/B座-2018-11-14.json') as f:
    source = f.read()
a = json.loads(source)

for i in a['obj']['roomlist']:
    for period in i['record']:
        if 1 <= period['room_period'] <= 5 and period['room_state'] == '0':
            leisure_room[str(period['room_period'])].append(i['room_name'])

for item in leisure_room:
    print(periods[item], end='\t')
    for period in leisure_room[item]:
        print(period, end='\t')
    print('')
#print(leisure_room)