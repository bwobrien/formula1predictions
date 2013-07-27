'''
F1 Predictions App UI handler
'''

from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
from py import DB, F1API
import os


class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    api = F1API.API()
    if user:
      userDb = DB.Users()
      uuid = user.user_id()
      userRow = userDb.getUserById(uuid)
      predictionsDb = DB.Predictions()
      racenum = predictionsDb.getNextRaceByUuid(uuid)
      if racenum is None:
        racenum = 1
      pointsLast = 0
      pointsTotal = 0
      if racenum > 1:
        pointsLast, pointsTotal = self.getPoints(predictionsDb, api, uuid)
      #25,18,15 and half points for quali, 2 pt for 
      if userRow:
        #registered
        opponents = userDb.getOpponents(uuid)
        for each in opponents:
          each['last'], each['total'] = self.getPoints(predictionsDb, api, each['uuid'])
        template_values = {
            'racenum': racenum,
            'drivers': api.getDriverList(),
            'logout_url': users.create_logout_url('/'),
            'user_name': userRow.display,
            'points_total': pointsTotal,
            'points_last_race': pointsLast,
            'opponents': opponents
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/overall_makepredictions.html')
        self.response.out.write(template.render(path, template_values))
      else:
        self.redirect('/register/view')

    else:
      self.redirect(users.create_login_url('/'))

  def getPoints(self, predictionsDb, api, uuid):
    racenum = predictionsDb.getNextRaceByUuid(uuid)
    pointsTotal = 0
    pointsLast = 0
    if racenum == None:
      return 0, 0
    for i in range(1, racenum):
      raceResult = api.getResult(i, True)
      qualiResult = api.getResult(i, False)
      qualiResultCode = api.getDriverCodeFromId(qualiResult)
      myRaceResult = predictionsDb.getPredictions(uuid, i, True)
      myQualiResult = predictionsDb.getPredictions(uuid, i, False)
      pointsLast = float(self.calculatePoints(myRaceResult, raceResult, True))
      pointsLast += float(self.calculatePoints(myQualiResult, qualiResultCode, False))
      pointsTotal += float(pointsLast)
    return pointsLast, pointsTotal

  def calculatePoints(self, myList, resultList, isRace):
    if resultList == []:
      return 0
    top3 = resultList[:3]
    #quali point (to be double if it's race)
    points = [12.5, 9, 7.5]
    wrongOrderPoints = 1
    if isRace:
      points = [i * 2 for i in points]
      wrongOrderPoints = 2

    myTotal = 0.0
    for i in range(len(myList)):
      if myList[i] == top3[i]:
        myTotal += points[i]
      elif myList[i] in top3:
        myTotal += wrongOrderPoints
    return myTotal




class PredictionsHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    predictionsDb = DB.Predictions()
    q1 = self.request.get('q1')
    q2 = self.request.get('q2')
    q3 = self.request.get('q3')
    r1 = self.request.get('r1')
    r2 = self.request.get('r2')
    r3 = self.request.get('r3')
    quali = [q1, q2, q3]
    race = [r1, r2, r3]
    uuid = user.user_id()
    raceNum = predictionsDb.getNextRaceByUuid(uuid)
    if raceNum is None:
      raceNum = 1
    predictionsDb.addPredictions(uuid, raceNum, quali, race)
    template_values = {
                       'racenum': raceNum,
                       'quali': quali,
                       'race': race
                       }
    path = os.path.join(os.path.dirname(__file__), 'templates/predictions_recorded.html')
    self.response.out.write(template.render(path, template_values))
        

class RegisterView(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(user.create_login_url(self.request.uri))
    else:
      self.response.out.write('''
                <form action="/register/submit" method="post">
                  <div><span>Display Name:</span><input type="text" name="displayName" /></div>
                  <div><input type="submit" value="Register" /></div>
                </form>''')

class RegisterSubmit(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(user.create_login_url(self.request.uri))
    else:
      displayName = self.request.get('displayName')
      userDb = DB.Users()
      userDb.addUser(user.user_id(), user.email(), displayName)
      self.redirect('/')

application = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                       ('/register/view', RegisterView),
                                       ('/register/submit', RegisterSubmit),
                                       ('/predictions', PredictionsHandler)
                                       ], debug=True)
