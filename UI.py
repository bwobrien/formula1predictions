'''
F1 Predictions App UI handler
'''

from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
from py import DB, F1API
import os



def getPoints(predictionsDb, api, uuid):
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
    pointsLast = float(calculatePoints(myRaceResult, raceResult, True))
    pointsLast += float(calculatePoints(myQualiResult, qualiResultCode, False))
    pointsTotal += float(pointsLast)
  return pointsLast, pointsTotal


def calculatePoints(myList, resultList, isRace):
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


def redirectUser(handler):
  userDb = DB.Users()
  user = users.get_current_user()
  if user is None:
    # Not signed in
    handler.redirect(users.create_login_url('/'))
    return

  userRow = userDb.getUserById(user.user_id())
  if userRow is None:
    # Signed-in, not registered
    handler.redirect('/register/view')
    return

  return user

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = redirectUser(self)
    if user is None:
      return
    api = F1API.API()
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
      pointsLast, pointsTotal = getPoints(predictionsDb, api, uuid)
    template_values = {
        'racenum': racenum,
        'drivers': api.getDriverList(),
        'logout_url': users.create_logout_url('/'),
        'user_name': userRow.display,
        'points_total': pointsTotal,
        'points_last_race': pointsLast
    }

    path = os.path.join(os.path.dirname(__file__), 'templates/base_makepredictions.html')
    self.response.out.write(template.render(path, template_values))


class Points(webapp2.RequestHandler):
  def get(self):
    user = redirectUser(self)
    if user is None:
      return
    userDb = DB.Users()
    predictionsDb = DB.Predictions()
    api = F1API.API()

    uuid = user.user_id()
    opponents = userDb.getOpponents(uuid)
    for each in opponents:
      each['last'], each['total'] = getPoints(predictionsDb, api, each['uuid'])

    template_values = {
      'opponents': opponents
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/base_points.html')
    self.response.out.write(template.render(path, template_values))


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
                                       ('/predictions', PredictionsHandler),
                                       ('/points', Points)
                                       ], debug=True)
