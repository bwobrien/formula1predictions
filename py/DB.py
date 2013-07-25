"""F1 Predictions App Database interface
Defines the database tables and methods for accessing them.
"""

from google.appengine.ext import db

class Users(db.Model):
  uuid = db.StringProperty()
  email = db.StringProperty()
  display = db.StringProperty()

  def getUserById(self, uuid):
    usersResults = db.GqlQuery("SELECT * "
                               "FROM Users "
                               "Where uuid = '" + uuid + "'")
    for userRow in usersResults:
      '''Just return the first result, should only be one anyway'''
      return userRow

  def addUser(self, uuid, email, display):
    if not uuid:
      return

    userRow = Users()
    userRow.uuid = uuid
    userRow.email = email
    userRow.display = display
    userRow.put()
    
  def getOpponents(self, uuid):
    opponentsResults = db.GqlQuery("SELECT * "
                               "FROM Users")
    retList = []
    for each in opponentsResults:
      retDict = {}
      if uuid != each.uuid:
        retDict['name'] = each.display
        retDict['uuid'] = each.uuid
        retList.append(retDict)
    return retList

class Predictions(db.Model):
  uuid = db.StringProperty()
  raceNum = db.IntegerProperty()
  submitted = db.DateTimeProperty(auto_now_add=True)
  quali = db.StringListProperty()
  race = db.StringListProperty()
  
  def addPredictions(self, uuid, raceNum, quali, race):
    predictionsRow = Predictions()
    predictionsRow.uuid = uuid
    predictionsRow.quali = quali
    predictionsRow.race = race
    predictionsRow.raceNum = raceNum
    predictionsRow.put()
    
  def getNextRaceByUuid(self, uuid):
    predictionsResults = db.GqlQuery("SELECT * " +
                               "FROM Predictions " +
                               "Where uuid = '" + uuid + "'" +
                               "ORDER BY submitted DESC")

    for predictionsRow in predictionsResults:
      return predictionsRow.raceNum + 1
    
  def getPredictions(self, uuid, raceNum, isRace):
    queryResult = db.GqlQuery("SELECT * " +
                              "FROM Predictions " +
                              "WHERE uuid = '" + uuid + "'" +
                              "AND raceNum = " + str(raceNum))
    if isRace:
      return queryResult.get().race
    else:
      return queryResult.get().quali

class Results(db.Model):
  raceNum = db.IntegerProperty(required=True)
  quali = db.StringListProperty()
  race = db.StringListProperty()

#test
def main():
  db = Users()
  print db.getOpponents('185804764220139124118')
  

if __name__ == "__main__":
    main()
