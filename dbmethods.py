class FetchStats : 

    cursor = None
    team = 0

    def __init__(self, c):
        self.cursor = c
        self.team = self.getTeam(1)

    def sortList(self, listToBeSorted):
        list2 = list(zip(*listToBeSorted[1:len(listToBeSorted)][::1]))

        list3 = []

        index = 0
        for i in list2[1:len(list2)]:
            list3.append([])
            for j in range(len(i)) :
                list3[index].append([list2[0][j], i[j]])
            index += 1

        sortedList = []
        for i in range(len(list3)) :
            sortedList.append(sorted(list3[i][1:len(list3[i])], reverse = True, key = lambda x : x[1]))
            sortedList[i].insert(0, ["Category", list3[i][0][1]])
        finalList = []

        for i in sortedList :
            counter = 0
            for j in i :
                counter += 1
                if j[0] == self.team :
                    finalList.append(counter)
 
        return finalList

    def getTeam(self, index) :
        self.cursor.execute("""SELECT Team_Id from Key where rowid = ?""", (index,))
        results = self.cursor.fetchall()
        return results[0][0]
        
    def getAllTeams(self) :
        allTeams = []
        self.cursor.execute("select count(*) from Key")
        temp = self.cursor.fetchall()
        total = temp[0][0]
        for i in range (1, total+1):
            allTeams.append(self.getTeam(i))
        return allTeams
        
    #record methods - Playoffs not included except for teamPlayoffRecord

    def teamOverallRecord(self) :
        
        self.cursor.execute("""SELECT * from Games where Winner_Id = ? and Loser_Id is not null and Playoffs = 'NONE'""", (self.team,))
        wins = len(self.cursor.fetchall())
        self.cursor.execute("""SELECT * from Games where Loser_Id = ? and Playoffs = 'NONE'""",(self.team,))
        losses = len(self.cursor.fetchall())
        return wins, losses

    def teamPlayoffRecord(self) :
        self.cursor.execute("""SELECT * from Games where Winner_Id = ? and Loser_Id is not null and Playoffs = 'WINNERS_BRACKET' """, (self.team,))
        wins = len(self.cursor.fetchall())
        self.cursor.execute("""SELECT * from Games where Loser_Id = ? and Playoffs = 'WINNERS_BRACKET'""",(self.team,))
        losses = len(self.cursor.fetchall())
        return wins, losses

    def teamRecordYear(self, year) : 
        self.cursor.execute("""SELECT * from Games where Season = ? and Winner_Id = ? and Loser_Id is not null and Playoffs = 'NONE'""", (year, self.team,))
        wins = len(self.cursor.fetchall())
        self.cursor.execute("""SELECT * from Games where Season = ? and Loser_Id = ? and Playoffs = 'NONE'""", (year, self.team,))
        losses = len(self.cursor.fetchall())
        if (wins or losses) == 0 :
            return 0, 0, 0
        else :
            return wins, losses, year

    def teamRecordAgainst(self, teamagainst) :
        self.cursor.execute("""SELECT * from Games where Winner_Id = ? and Loser_Id = ?""", (self.team,teamagainst))
        wins = len(self.cursor.fetchall())
        self.cursor.execute("""SELECT * from Games where Loser_Id = ? and Winner_Id = ?""",(self.team,teamagainst))
        losses = len(self.cursor.fetchall())
        return wins, losses, teamagainst

    #pts methods - Playoffs not included
    def teamAveragePointsScored(self) :
        total = 0 

        self.cursor.execute("""SELECT Home_Score from Games where Home_Id = ? and Loser_Id is not null and Playoffs = 'NONE'""", (self.team,))
        homes = self.cursor.fetchall()

        self.cursor.execute("""SELECT Away_Score from Games where Away_Id = ? and Playoffs = 'NONE'""", (self.team,))
        aways = self.cursor.fetchall()

        gamesPlayed = len(homes) + len(aways)

        for i in homes:
            total += i[0]
        for i in aways:
            total += i[0]

        return round((total / gamesPlayed), 2)

    def teamAveragePointsAllowed(self) :
        total = 0 

        self.cursor.execute("""SELECT Away_Score from Games where Home_Id = ? and Loser_Id is not null and Playoffs = 'NONE'""", (self.team,))
        homes = self.cursor.fetchall()

        self.cursor.execute("""SELECT Home_Score from Games where Away_Id = ? and Playoffs = 'NONE'""", (self.team,))
        aways = self.cursor.fetchall()

        gamesPlayed = len(homes) + len(aways)

        for i in homes:
            total += i[0]
        for i in aways:
            total += i[0]

        return round((total / gamesPlayed), 2)

    def teamAveragePointsScoredYear(self, year) : 
        total = 0 

        self.cursor.execute("""SELECT Home_Score from Games where Season = ? and Home_Id = ? and Loser_Id is not null  and Playoffs = 'NONE'""", (year, self.team,))
        homes = self.cursor.fetchall()

        self.cursor.execute("""SELECT Away_Score from Games where Season = ? and Away_Id = ? and Playoffs = 'NONE'""", (year, self.team,))
        aways = self.cursor.fetchall()

        gamesPlayed = len(homes) + len(aways)

        for i in homes:
            total += i[0]
        for i in aways:
            total += i[0]
        if total != 0 :
            return round((total / gamesPlayed), 2)
        else : 
            return 0

    def teamAveragePointsAllowedYear(self, year) :
        total = 0 

        self.cursor.execute("""SELECT Away_Score from Games where Season = ? and Home_Id = ? and Loser_Id is not null  and Playoffs = 'NONE'""", (year, self.team,))
        homes = self.cursor.fetchall()

        self.cursor.execute("""SELECT Home_Score from Games where Season = ? and Away_Id = ? and Playoffs = 'NONE'""", (year, self.team,))
        aways = self.cursor.fetchall()

        gamesPlayed = len(homes) + len(aways)

        for i in homes:
            total += i[0]
        for i in aways:
            total += i[0]
        if total != 0 :
            return round((total / gamesPlayed), 2)
        else : 
            return 0

    #playoffs/position methods

    def championships(self):
        
        self.cursor.execute("""SELECT * from Other where Team_Id = ? and Position = '1'""", (self.team,))
        championshipYears = self.cursor.fetchall()

        return(len(championshipYears))

    def playoffAppeareances(self):
        yearsInPlayoffs = 0
        
        for year in range (2016, 2021) :
            self.cursor.execute("""SELECT * from Games where Season = ? and (Home_Id = ? or Away_Id = ?) and Playoffs = 'WINNERS_BRACKET' and Loser_Id is not null """, (year, self.team, self.team,))
            c = self.cursor.fetchall()
            if (len(c) == 0) :
                pass
            else:
                yearsInPlayoffs = yearsInPlayoffs + 1
        
        return yearsInPlayoffs
            
    def positionForYear(self, year) :
        self.cursor.execute("""SELECT Position from Other where Team_Id = ? and Season = ? """, (self.team, year,))
        posYear = self.cursor.fetchall()

        if(len(posYear) == 0) :
            return 0
        else :
           return posYear[0][0], year

    def avgPosition(self) :
        positionTally = 0
        yearsPlayed = 0

        for year in range(2016, 2021) :
            if type(self.positionForYear(year)) is tuple:
                position = self.positionForYear(year)[0]
                if (position != 0) :
                    positionTally = positionTally + position
                    yearsPlayed = yearsPlayed + 1
        return positionTally / yearsPlayed#, yearsPlayed

    #player methods

    def highestScoringPerPosition(self, year) :
        if year == "ALL" :
            bestPlayers = []
            pos = ('QB', 'RB', 'WR', 'TE', 'K', 'D/ST')
            for p in pos :
                self.cursor.execute("""SELECT Player_Name, Player_Points, Season from Players where Player_Team_Id = ? and Player_Position = ?""", (self.team, p))
                players = self.cursor.fetchall()
                players.sort(reverse=True, key = lambda pts:pts[1])
                bestPlayers.append(players[0])
        else :
            bestPlayers = []
            pos = ('QB', 'RB', 'WR', 'TE', 'K', 'D/ST')
            for p in pos :
                self.cursor.execute("""SELECT Player_Name, Player_Points from Players where Player_Team_Id = ? and Player_Position = ? and Season = ?""", (self.team, p, year))
                players = self.cursor.fetchall()
                players.sort(reverse=True, key = lambda pts:pts[1])
                bestPlayers.append(players[0])
        newBestPlayers = []
        for i in bestPlayers :
            newBestPlayers.append([i[0], i[1] / 16, year])
        
        return newBestPlayers

    #method for playoff bracket
    def getPlayoffBracket(self, year) :
        
        self.cursor.execute("""SELECT Week, Home_Id, Away_Id, Home_Score, Away_Score from Games where Playoffs = 'WINNERS_BRACKET' and Season = ?""", (year,))
        playoffs2 = self.cursor.fetchall()
        #transform db list from list[tuple] into list[list], make entirely mutable
        playoffs = []
        for i in playoffs2:
            playoffs.append(list(i))
        #collecting all teams in playoffs
        totalTeams = []
        totalWeeks = 1

        temp = playoffs[0][0] 
        for p in playoffs :
            if p[1] not in totalTeams :
                totalTeams.append(p[1])         
            if p[2] not in totalTeams :
                totalTeams.append(p[2])
            if temp != p[0] :
                totalWeeks += 1
                temp = p[0]
        #if playoff has teams with byes
        if len(totalTeams) != 2**totalWeeks :

            firstWeek = 14
            temp = 0
            index = 0
            bracketList = [[] for i in range(totalWeeks)]

            while temp + 1 <= totalWeeks :
                bracketList[index] = [[] for i in range(2 ** temp)]
                temp +=1
                index +=1
            
            temp = 0
            weekIndex = 0
            currWeek = playoffs[len(playoffs) - 1][0]
            gameIndex = 0 

            for i in reversed(playoffs) :

                if i[0] != firstWeek :
                    if currWeek != i[0] :
                        weekIndex += 1
                        gameIndex = 0
                        currWeek = i[0]
                    
                    bracketList[weekIndex][gameIndex] = i
                    playoffs.remove(i)
                    gameIndex +=1 


            newList = []
            section = bracketList[len(bracketList) - 2].copy()
            index = 0 

            for j in reversed(playoffs) :

                for i in section :
                    if(j[1] == i[1] or j[2] == i[1]) :
                        newList.append([j[1], j[2], j[3], j[4]])
                        newList.append(["null", i[2]])
                        playoffs.remove(j)
                        section.remove(i)
                        break
                    elif(j[1] == i[2] or j[2] == i[2]) :
                        newList.append([j[1], j[2], j[3],j[4]])
                        newList.append([i[1], "null"])
                        playoffs.remove(j)
                        section.remove(i)
                        break
                    else :
                        newList.append([i[1], "null"])
                        newList.append([i[2], "null"])

            for i in bracketList:
                for j in i :
                    if j != [] :
                        j[1], j[2] = j[2], j[1]
                        j[3], j[4] = j[4], j[3]
                i.reverse()

            for k in newList :
                k[0], k[1] = k[1], k[0]
            
            bracketList[len(bracketList) - 1] = newList  

        #playoff with no byes
        else :

            #code for error where final round result opposite
            playoffs[len(playoffs) - 1][4], playoffs[len(playoffs) - 1][3] = playoffs[len(playoffs) - 1][3], playoffs[len(playoffs) - 1][4]

            bracketList = [[]]
            highestWeek = playoffs[len(playoffs) - 1][0] 
            temp = highestWeek
            for i in reversed(playoffs) :
                
                if (i[0] != temp) :
                    temp = i[0]
                    bracketList.append([])
                bracketList[highestWeek - temp].append(i)
            
        results = [[]]
        teams = []

        for i in reversed(bracketList) : 
            blank = []
            for j in i :
                if(len(j) == 2) :
                    blank.append([None, None])
                else : 
                    blank.append([j[len(j) - 2], j[len(j) - 1]])
            results[0].append(blank)

        for i in bracketList[len(bracketList) - 1] :
            temp = []
            for j in i :
                if(j == 'null') :
                    temp.append(None)
                elif(type(j) == str) :
                    temp.append(j)
            teams.append(temp)
        return teams, results

    def getBracket(self, year) :
        self.cursor.execute("""SELECT Week, Home_Id, Away_Id, Home_Score, Away_Score from Games where Playoffs = 'WINNERS_BRACKET' and Season = ?""", (year,))
        playoffWeeks = self.cursor.fetchall()

        return playoffWeeks
    
    def finalBracket(self, year) :
        
        teams = []

        f = self.getBracket(year)
        for i in f :
            if i[0] == f[0][0] :
                teams.append([i[1], i[2]])

        week = f[0][0]
        temp = []
        results = []
        for i in f:
            if week != i[0] :
                week = i[0]
                results.append(temp)
                temp = []
            temp.append([i[3], i[4]])
        results.append([[f[len(f) - 1][3], f[len(f) - 1][4]]])

        return teams, results