import sqlite3, sys, math
from espn_api.football import League
import os

def main(argv): #JL or GT

    #Credentials
    _espn_s2 = ''
    _swid = ''

    #League IDs
    JusticeLeague = ''
    GTLeague = ''
    LEAGUENAME=  ''
    REALTIME = int(argv[2]) #current week
    currentLeague = ''

    
    #define which league is being used
    if argv[1] == '1':
            currentLeague = GTLeague
            LEAGUENAME = 'GT'
    else :
           currentLeague = JusticeLeague
           LEAGUENAME = 'JL'
    
    print(REALTIME, currentLeague, "league = ", LEAGUENAME, "current week = ", argv[2])

    #creates database
    def createDatabase():
        db = sqlite3.connect('fantasyDb_' + LEAGUENAME + '.db')
        cursor = db.cursor()
        try:
            cursor.execute('''CREATE TABLE Games
                            (Season integer, Week integer, Home_Id integer, Away_Id integer,
                            Home_Score integer, Away_Score integer, Winner_Id integer, Loser_Id integer, Playoffs text)''')
        except:
            print(Exception)
        try:
            cursor.execute('''CREATE TABLE Players
                            (Season integer, Player_Name text, Player_Team_Id integer, Player_Position text, Player_Points integer)''')
        except:
            print(Exception)
        try:
            cursor.execute('''CREATE TABLE Key
                            (Team_Id integer, Team_Name text)''')
        except:
            print(Exception)
        try:
            cursor.execute('''CREATE TABLE Other
                            (Season integer, Team_Id text, Position integer)''')
        except:
            print(Exception)
        db.commit()
        db.close()
    #creates and fills 'Games' table - contains every week in league since 2015
    def getGames():
        
        #connect to database
        db = sqlite3.connect('fantasyDb_' + LEAGUENAME + '.db')
        cursor = db.cursor()

        for currentYear in range(2016, 2021):
            
            #get league for current year
            league = League(league_id=currentLeague, year=currentYear, espn_s2=_espn_s2, swid=_swid)
            
            #code for current year

            for currentWeek in range(1, len(league.teams[0].scores)+1):

                matchups = league.scoreboard(currentWeek)
                
                if currentYear == 2020 and currentWeek > REALTIME :
                    pass
                else:
                    #print(math.ceil(len(league.teams)/2))
                    for i in range(0,len(matchups)) :
                        matchup = matchups[i]
                        if(matchup.away_team == 0 or matchup.home_team == 0) :
                            if matchup.away_team == 0 :
                                Home_Id = matchup.home_team.owner #matchup.data['home']['teamId'] - 1
                                Away_Id = None #matchup.data['away']['teamId'] - 1
                                Home_Score = matchup.home_score
                                Away_Score = None
                                Playoffs = matchup.data['playoffTierType']
                                Winner_Id = Home_Id
                                cursor.execute("INSERT INTO Games (Season, Week, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, Loser_Id, Playoffs) VALUES (?,?,?,?,?,?,?,?,?)",
                                (currentYear, currentWeek, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, None, Playoffs))
                                db.commit()
                            else : 
                                Away_Id = matchup.away_team.owner #matchup.data['home']['teamId'] - 1
                                Home_Id = None #matchup.data['away']['teamId'] - 1
                                Away_Score = matchup.away_score
                                Home_Score = None
                                Playoffs = matchup.data['playoffTierType']
                                Winner_Id = Away_Id
                                cursor.execute("INSERT INTO Games (Season, Week, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, Loser_Id, Playoffs) VALUES (?,?,?,?,?,?,?,?,?)",
                                (currentYear, currentWeek, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, None, Playoffs))
                                db.commit()
                        else :
                            Home_Id = matchup.home_team.owner #matchup.data['home']['teamId'] - 1
                            Away_Id = matchup.away_team.owner #matchup.data['away']['teamId'] - 1
                            Home_Score = matchup.home_score
                            Away_Score = matchup.away_score
                            Playoffs = matchup.data['playoffTierType']
                            if(Home_Score > Away_Score):
                                Winner_Id = Home_Id
                                Loser_Id = Away_Id
                            elif(Home_Score == Away_Score):
                                if (matchup.data['winner'] == "AWAY") :
                                    Winner_Id = Away_Id
                                    Loser_Id = Home_Id
                                else : 
                                    Winner_Id = Home_Id
                                    Loser_Id = Away_Id
                            else:
                                Winner_Id = Away_Id
                                Loser_Id = Home_Id
                            #print(currentYear, currentWeek, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, Loser_Id, Playoffs)
                            cursor.execute("INSERT INTO Games (Season, Week, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, Loser_Id, Playoffs) VALUES (?,?,?,?,?,?,?,?,?)",
                            (currentYear, currentWeek, Home_Id, Away_Id, Home_Score, Away_Score, Winner_Id, Loser_Id, Playoffs))
                            db.commit()
        db.close()
    #creates and fills 'Players' table - contains every player for each team every year
    def getPlayers():

        db = sqlite3.connect('fantasyDb_' + LEAGUENAME + '.db')
        cursor = db.cursor()
        
        for currentYear in range(2016, 2021):
            
            #get league for current year
            league = League(league_id=currentLeague, year=currentYear, espn_s2=_espn_s2, swid=_swid)
            
            #code for current year
            for Team_Id in range(0, len(league.teams)) :
        
                #get league with method arguments
                
                for player in range(0, len(league.teams[Team_Id].roster)):

                    roster = league.teams[Team_Id].roster[player]

                    cursor.execute("INSERT INTO Players (Season, Player_Name, Player_Team_Id, Player_Position, Player_Points) VALUES (?,?,?,?,?)",
                    (currentYear, roster.name, league.teams[Team_Id].owner#Team_Id
                    , roster.position, roster.stats[0]['points']))
                    db.commit()
        db.close()  
    #creates and fills 'Key' table - contains team id for each current team name
    def getKey():

        db = sqlite3.connect('fantasyDb_' + LEAGUENAME + '.db')
        cursor = db.cursor()

        teamsList = []

        for currentYear in reversed(range(2016, 2021)) :
            league = League(league_id=currentLeague, year=currentYear, espn_s2=_espn_s2, swid=_swid)
            for i in range (0, len(league.teams)) : 
                team = league.teams[i].owner
                if team in teamsList :
                    pass
                else : 
                    teamsList.append(team)
                    cursor.execute("INSERT INTO Key (Team_Id, Team_Name) VALUES (?,?)",
                    (team, league.teams[i].team_name))
                    db.commit()

        db.close()
    #creates and fills 'Other' table - contains final position of each team for each year
    def getRecords():
        #connect to database
        db = sqlite3.connect('fantasyDb_' + LEAGUENAME + '.db')
        cursor = db.cursor()

        for currentYear in range(2016, 2021):
            
            #get league for current year
            league = League(league_id=currentLeague, year=currentYear, espn_s2=_espn_s2, swid=_swid)
                
            for t in range(0, len(league.teams)) : 
                position = league.teams[t].final_standing
                cursor.execute("INSERT INTO Other (Season, Team_Id, Position) VALUES (?,?,?)",
                    (currentYear, league.teams[t].owner, position))
                db.commit()
        db.close()  
    
    #run each of above methods
    createDatabase()
    getGames()
    getPlayers()
    getKey()
    getRecords()  
#if __name__ == "__main__":
#    main(sys.argv)
