from flask import Flask, render_template, request, jsonify, json
from datetime import datetime

import os
import sqlite3
import dbmethods as d

leagueGT = 'fantasyDb_GT.db'
leagueJL = 'fantasyDb_JL.db'
currLeague = None

app = Flask(__name__)

databaseMethods = None

#HOME PAGE ROUTE
@app.route('/')
def m():
    changeDatabase(leagueGT)
    return render_template('base.html', league1=leagueGT,league2=leagueJL,league1Name="Georgia Tech League", league2Name="Justice League")

#CHANGE LEAGUE HANDLER
@app.route('/changeleague', methods = ['POST'])
def changeleague():
    newLeague=request.form['leagueChosen']
    gather = request.form['gather']
    changeDatabase(newLeague)

    if gather == 'ALL' :
        status = 'SHOW'
    else : 
        status = 'HIDE'

    #LEAGUE TABLE C
    temp = databaseMethods.team
    leagueC = [
        ["string", "int", "int", "int"],
        ["Team", "Apps", "Championships", "Wins", "Losses"]
    ]
    for team in databaseMethods.getAllTeams() :
        databaseMethods.team = team
        tempR = databaseMethods.teamPlayoffRecord()
        leagueC.append([team, databaseMethods.playoffAppeareances(), databaseMethods.championships(), tempR[0], tempR[1] 
        ])
    databaseMethods.team = temp
    #bracket create and logic 
    if(gather != 'ALL') :
        bracketTeams, bracketResults = databaseMethods.finalBracket(gather)
    else : 
        bracketTeams = []
        bracketResults = []

    return jsonify({'leagueTeams' : databaseMethods.getAllTeams(), 'leagueA' : getLeagueA(gather), 'leagueC' : leagueC, 'status' : status, 'bracketTeams' : bracketTeams, 'bracketResults' : bracketResults})

#CHANGE TEAM HANDLER
@app.route('/changeteam', methods = ['POST'])
def changeteam():
    newTeam = request.form['teamChosen']
    gather = request.form['gather']
    databaseMethods.team = newTeam
    #TEAM TABLE D
    q = databaseMethods.sortList(getLeagueA(gather))

    teamD = [
        ["string", "int", "int", "int", "int", "int"],
        ["Team", "Wins", "Losses", "AVG Points Scored", "AVG Points Allowed", "Points Margin"]
    ]
    teamD.append(databaseMethods.sortList(getLeagueA(gather)))
    teamD[2].insert(0, databaseMethods.team)

    #TEAM TABLE E
    teamE = [
        ["string","string", "string", "string", "string", "string", "string"],
        ["Position", "QB", "RB", "WR", "TE", "DE/S", "K"],
        ["Player"],
        ["PPG"]        
        ]
    temp = databaseMethods.highestScoringPerPosition(gather)
    
    for i in temp :
        teamE[2].append(i[0])
        teamE[3].append(i[1])
    if gather != "ALL" :
        teamE.append(["Points"])
        for i in temp :
            teamE[4].append(i[2])

    return jsonify({'newTeam' : newTeam, 'teamD' : teamD, 'teamE' : teamE})

#method for changing teams, called at home page start and changeleague()  
def changeDatabase(newLeague):
    global currLeague
    currLeague=newLeague
    db = sqlite3.connect(currLeague)
    cursor = db.cursor()
    global databaseMethods 
    databaseMethods =  d.FetchStats(cursor)
    
#method used in changeteam() 
def getLeagueA(gather):

    leagueA = [
        ["string", "int", "int", "int", "int", "int"],
        ["Team", "Wins", "Losses", "AVG Points Scored", "AVG Points Allowed", "Points Margin"]
    ]

    temp = databaseMethods.team
    if gather == "ALL" :
        for team in databaseMethods.getAllTeams() :
            databaseMethods.team = team
            tempR = databaseMethods.teamOverallRecord()
            leagueA.append([team, tempR[0], tempR[1],
                databaseMethods.teamAveragePointsScored(), databaseMethods.teamAveragePointsAllowed(),
                round((databaseMethods.teamAveragePointsScored() - databaseMethods.teamAveragePointsAllowed()), 2)
            ])
    else : 
        for team in databaseMethods.getAllTeams() :
            databaseMethods.team = team
            tempR = databaseMethods.teamRecordYear(gather)
            leagueA.append([team, tempR[0], tempR[1],
                databaseMethods.teamAveragePointsScoredYear(gather), databaseMethods.teamAveragePointsAllowedYear(gather),
                round(databaseMethods.teamAveragePointsScoredYear(gather) - databaseMethods.teamAveragePointsAllowedYear(gather), 2)
            ])
    databaseMethods.team = temp
    return leagueA

'''    
if __name__ == '__main__':
    app.run(debug=True, threaded=False)    
'''
def start():
    app.run(host=('0.0.0.0'), use_reloader=False, debug=False, threaded=False, port=5001)