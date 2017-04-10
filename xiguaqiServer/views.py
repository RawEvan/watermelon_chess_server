from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from forms import roomForm
import random
import json
import pdb
import time

try:
    import sae.kvdb
    kv = sae.kvdb.Client()
except Exception, e:
    print e

def setRoomID():
    waitingRooms = kv.get('waitingRooms')
    playingRooms = kv.get('playingRooms')
    if waitingRooms:
        roomID = random.choice(waitingRooms)
        waitingRooms.remove(roomID)
        if not playingRooms:
            playingRooms = []
        playingRooms.append(roomID)
    else:
        waitingRooms = []
        roomID = random.randint(1, 10000)
        while playingRooms and roomID in playingRooms:
            roomID = random.randint(1, 10000)
        waitingRooms.append(roomID)
    kv.set('waitingRooms', waitingRooms)
    kv.set('playingRooms', playingRooms)
    return str(roomID)


def setName():
    name = random.randint(1, 10000)
    nameList = kv.get('nameList')
    if not nameList:
        nameList = []
    while name in nameList:
        name = random.randint(1, 10000)
    nameList.append(name)
    kv.set('nameList', nameList)

    return str(name)


def initRoomInfo():
    roomInfo = {}
    roomInfo['roomID'] = None
    roomInfo['full'] = False
    roomInfo['player1'] = None
    roomInfo['player2'] = None
    roomInfo['playerNum'] = '0'
    roomInfo['player2Pre'] = False
    roomInfo['player1Pre'] = False
    roomInfo['preOK'] = False
    roomInfo['pointStatus'] = None
    roomInfo['turn'] = None
    roomInfo['status'] = 'init'
    return roomInfo


@csrf_exempt
def room(request):
    if request.method == 'POST':
        print '----------request.POST----------'
        print request.POST
        action = request.POST['action']
        roomID = str(request.POST['roomID'])
        if not roomID:
            roomID = setRoomID()
        name = request.POST['name']
        if not name:
            name = setName()
        roomInfoJson = kv.get(roomID)
        if action == 'enter':
            if not roomInfoJson:
                roomInfo = initRoomInfo()
                roomInfo['roomID'] = roomID
                roomInfo['player1'] = name
                roomInfo['playerNum'] = '1'
            else:
                roomInfo = json.loads(roomInfoJson)
                if roomInfo['playerNum'] == '0':
                    roomInfo['roomID'] = roomID
                    roomInfo['player1'] = name
                    roomInfo['playerNum'] = '1'
                elif roomInfo['playerNum'] == '1':
                    if roomInfo['player1'] != name:
                        roomInfo['player2'] = name
                        roomInfo['playerNum'] = '2'
                        roomInfo['full'] = True
                else:
                    pass
            print time.ctime() + 'enter:' + roomID + name

        elif action == 'pre':
            roomInfo = json.loads(roomInfoJson)
            if name == roomInfo['player1']:
                roomInfo['player1Pre'] = True
            elif name == roomInfo['player2']:
                roomInfo['player2Pre'] = True
            else:
                pass
            if roomInfo['player1Pre'] and roomInfo['player2Pre']:
                roomInfo['status'] = 'playing'
                roomInfo['turn'] = random.choice(
                    [roomInfo['player1'], roomInfo['player2']])
                roomInfo['preOK'] = True
            print time.ctime() + 'pre:' + roomInfo['roomID'] + name

        elif action == 'leave':
            roomInfo = json.loads(roomInfoJson)
            if name == roomInfo['player1']:
                roomInfo['player1'] = None
                roomInfo['turn'] = None
            elif name == roomInfo['player2']:
                roomInfo['player2'] = None
                roomInfo['turn'] = None
            else:
                pass
            print time.ctime() + 'leave:' + roomInfo['roomID'] + name
            if roomInfo['player1'] == None and roomInfo['player2'] == None:
                roomInfo = initRoomInfo()

        elif action == 'query':
            roomInfo = json.loads(roomInfoJson)
            if not roomInfo['roomID']:
                print time.ctime() + 'query:' + 'no room' + name
            else:
                print time.ctime() + 'query:' + roomInfo['roomID'] + name

        elif action == 'play':
            pointStatus = request.POST['pointStatus']
            roomInfo = json.loads(roomInfoJson)
            if name == roomInfo['turn']:
                roomInfo['pointStatus'] = pointStatus
                if name == roomInfo['player1']:
                    roomInfo['turn'] = roomInfo['player2']
                else:
                    roomInfo['turn'] = roomInfo['player1']
            print time.ctime() + 'play:' + roomInfo['roomID'] + name

        elif action == 'reset':
            print time.ctime() + 'reset:' + roomInfo['roomID'] + name
            waitingRooms = kv.get('waitingRooms')
            playingRooms = kv.get('playingRooms')
            try:
                waitingRooms.remove(roomID)
            except:
                pass
            try:
                playingRooms.remove(roomID)
            except:
                pass
            kv.set('playingRooms', playingRooms)
            kv.set('waitingRooms', waitingRooms)
            roomInfo = initRoomInfo()

        else:
            roomInfo = json.dumps('error:' + action)

        roomInfoJson = json.dumps(roomInfo)
        kv.set(roomID, roomInfoJson)
        roomInfoJson = kv.get(roomID)

    return HttpResponse(roomInfoJson)
