#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json as simplejson

"""Interface between app and F1 API (ergast.com/mrd/)
"""

class API():
  def getDriverList(self):
    DEFAULT_LIST = [
      {'code': 'VET', 'first': 'Sebastian', 'last': 'Vettel'},
      {'code': 'WEB', 'first': 'Mark', 'last': 'Webber'},
      {'code': 'ALO', 'first': 'Fernando', 'last': 'Alonso'},
      {'code': 'MAS', 'first': 'Felipe', 'last': 'Massa'},
      {'code': 'BUT', 'first': 'Jenson', 'last': 'Button'},
      {'code': 'PER', 'first': 'Sergio', 'last': 'Perez'},
      {'code': 'RAI', 'first': 'Kimi', 'last': 'Räikkönen'},
      {'code': 'GRO', 'first': 'Romain', 'last': 'Grosjean'},
      {'code': 'ROS', 'first': 'Nico', 'last': 'Rosberg'},
      {'code': 'HAM', 'first': 'Lewis', 'last': 'Hamilton'},
      {'code': 'HUL', 'first': 'Nico', 'last': 'Hulkenberg'},
      {'code': 'GUT', 'first': 'Esteban', 'last': 'Gutierrez'}, # code?
      {'code': 'DIR', 'first': 'Paul', 'last': 'di Resta'},
      {'code': 'SUT', 'first': 'Adrian', 'last': 'Sutil'}, # code?
      {'code': 'MAL', 'first': 'Pastor', 'last': 'Maldonado'},
      {'code': 'BOT', 'first': 'Valtteri', 'last': 'Bottas'}, # code?
      {'code': 'VER', 'first': 'Jean-Eric', 'last': 'Vergne'},
      {'code': 'RIC', 'first': 'Daniel', 'last': 'Ricciardo'},
      {'code': 'PIC', 'first': 'Charles', 'last': 'Pic'},
      {'code': 'VDG', 'first': 'Giedo', 'last': 'van der Garde'}, # code?
      {'code': 'BIA', 'first': 'Jules', 'last': 'Bianchi'}, # code?
      {'code': 'CHI', 'first': 'Max', 'last': 'Chilton'}, # code?
    ]
    return DEFAULT_LIST

  def getResult(self, race_num, isRace, year=2013):
    baseUrl = 'http://ergast.com/api/f1' #2013/1/results'
    if isRace:
      url = baseUrl + '/' + str(year) + '/' + str(race_num) + '/results.json'
      qualiOrRace = 'Results'
      codeOrId = 'code'
    #Qualifying
    else:
      url = baseUrl + '/' + str(year) + '/' + str(race_num) + '/qualifying.json'
      qualiOrRace = 'QualifyingResults'
      codeOrId = 'driverId'
    try:
      result = urllib2.urlopen(url)
    except urllib2.URLError, e:
      self.handleError(e)
    resultDict = simplejson.load(result)
    print "URL: " + url
    if resultDict['MRData']['total'] == '0':
      return []
    numDriver = len(resultDict['MRData']['RaceTable']['Races'][0][qualiOrRace])
    retList = []
    for i in range(numDriver):
      retList.append(resultDict['MRData']['RaceTable']['Races'][0][qualiOrRace][i]['Driver'][codeOrId])
    return retList
      
  def handleError(self, error):
#    do something
    return
  
  def getDriverCodeFromId(self, driverIdList):
    url = 'http://ergast.com/api/f1/2013/drivers.json'
    try:
      result = urllib2.urlopen(url)
    except urllib2.URLError, e:
      self.handleError(e)
      
    resultDict = simplejson.load(result)
    driverList = resultDict['MRData']['DriverTable']['Drivers']
    codeDict = {}
    for each in driverList:
      if each['driverId'] in driverIdList:
        codeDict[each['driverId']] = each['code']
    
    retList = []
    for each in driverIdList:
      retList.append(codeDict[each])
    return retList

#Test
def main():
  api = API()
  print api.getDriverCodeFromId(['button', 'hamilton', 'alonso'])
  

if __name__ == "__main__":
    main()
#    