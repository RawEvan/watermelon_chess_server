#!/usr/bin/python  
#coding=utf-8  
  
import urllib  
import urllib2  
import json
import pdb
  
roomID = None
player1 = None 
player2 = None

def post(url, parameters):  
    data = urllib.urlencode(parameters)  
    req = urllib2.Request(url, data)
    req.add_header('Content-Type', "application/x-www-form-urlencoded")
    #response = urllib2.urlopen(url)  
    response = urllib2.urlopen(req)  
    jsonData = response.read()  
    data = json.loads(jsonData) 
    return data
  
def action(roomID, action, name, pointStatus = None):
    parameters = {'roomID': roomID, 'action': action, 'name': name, 'pointStatus': pointStatus}
    return parameters

def main():  
    #url = "http://xiguaqi.applinzi.com/room/"
    url = 'http://localhost:8080/room/'

    parameters = {'roomID': '', 'action': 'enter', 'name': ''} 
    pdb.set_trace()
    data = post(url, parameters)
    player1 = data['player1'] 
    print data
    data = post(url, parameters)
    player2, roomID = data['player2'], data['roomID']
    print player2, roomID

    parameters = action(roomID, 'pre', player1)
    print post(url, parameters)  
    parameters = action(roomID, 'pre', player2)
    print post(url, parameters)  

    parameters = action(roomID, 'query', player1)
    print post(url, parameters)  
    parameters = action(roomID, 'query', player2)
    print post(url, parameters)  

    parameters = action(roomID, 'play', player1, 'status1')
    print post(url, parameters)  
    parameters = action(roomID, 'play', player2, 'status2')
    print post(url, parameters)  

    parameters = action(roomID, 'leave', player1)
    print post(url, parameters)  
    parameters = action(roomID, 'leave', player2)
    print post(url, parameters)  
  
if __name__ == '__main__':  
    main()  
