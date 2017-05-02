import baseball_reference_scraper
import csv

# Scraped strings are unicode, so we make them ascii
def encodeAscii(data_table):
    for i in range(len(data_table)):
        for j in range(len(data_table[i])):
            if data_table[i][j] is not None and type(data_table[i][j]) is str:
                data_table[i][j] = data_table[i][j].encode("ascii")

# baseball-reference.com has rows with header names in the middle of the tables 
# Therefore, if there are no numbers, then remove it
def checkTableForBadRows(table):
    for row in table:
        checkForNumbers = False
        for element in row:
            if any(char.isdigit() for char in element):
                checkForNumbers = True
        if not checkForNumbers:
            table.remove(row)

# Same idea as above
# Checks the whole dictionary rather than just one matrix
def checkDataForBadRows(all_data):
    for key in all_data.keys():
        for row in all_data[key]:
            checkForNumbers = False
            for element in row:
                element = str(element)
                if any(char.isdigit() for char in element):
                    checkForNumbers = True
            if not checkForNumbers:
                all_data[key].remove(row)

# Write all tables to a csv file
def writeToCSV(all_data, all_orders):
    with open('Baseball-Scrape.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for key in all_data.keys():
            writer.writerow([key])
            writer.writerow(all_orders[key])
            for row in range(len(all_data[key])):
                writer.writerow(all_data[key][row])
            writer.writerow("")
            writer.writerow("")
            writer.writerow("")

# Remove characters from names so that we can make the player URL properly
def removeCharacters(name):
    name = name.replace(' ', '')
    name = name.replace('.', '')
    name = name.replace(',', '')
    name = name.replace("'", '')
    name = name.replace('-', '')
    return name


if __name__ == "__main__":
    scraper = baseball_reference_scraper.BRScraper()

    # all team URLs
    resources = [["teams/ARI/2016.shtml", "teams/ATL/2016.shtml", 
        "teams/BAL/2016.shtml", "teams/BOS/2016.shtml", "teams/CHC/2016.shtml",
        "teams/CHW/2016.shtml", "teams/CIN/2016.shtml", "teams/CLE/2016.shtml",
        "teams/COL/2016.shtml", "teams/DET/2016.shtml", "teams/HOU/2016.shtml",
        "teams/KCR/2016.shtml", "teams/LAA/2016.shtml", "teams/LAD/2016.shtml",
        "teams/MIA/2016.shtml", "teams/MIL/2016.shtml", "teams/MIN/2016.shtml",
        "teams/NYM/2016.shtml", "teams/NYY/2016.shtml", "teams/OAK/2016.shtml", 
        "teams/PHI/2016.shtml", "teams/PIT/2016.shtml", "teams/SDP/2016.shtml", 
        "teams/SFG/2016.shtml", "teams/SEA/2016.shtml", "teams/STL/2016.shtml",
        "teams/TBR/2016.shtml", "teams/TEX/2016.shtml", "teams/TOR/2016.shtml", 
        "teams/WSN/2016.shtml"]]
    
    # shortened team name for URL mapped to true team names
    teams ={'ARI': 'Arizona Diamondbacks', 'ATL': 'Atlanta Braves', 
            'BOS': 'Boston Red Sox', 'CHC': 'Chicago Cubs', 
            'CHW': 'Chicago White Sox', 'CIN': 'Cincinnati Reds',
            'CLE': 'Cleveland Indians', 'COL': 'Colorado Rockies',
            'DET': 'Detroid Tigers', 'HOU': 'Houston Astros', 
            'KCR': 'Kansas City Royals', 'LAA': 'Los Angeles Angels of Anaheim',
            'LAD': 'Los Angeles Dodgers', 'MIA': 'Miami Marlins',
            'MIL': 'Milwaukee Brewers', 'MIN': 'Minnesota Twins',
            'NYM': 'New York Mets', 'NYY': 'New York Yankees',
            'OAK': 'Oakland Athletics', 'PHI': 'Philadelphia Phillies', 
            'PIT': 'Pittsbugh Pirates', 'SDP': 'San Diego Padres',
            'SFG': 'San Francisco Giants', 'SEA': 'Seattle Mariners',
            'STL': 'St. Louis Cardinals', 'TBR': 'Tampa Bay Rays',
            'TEX': 'Texas Rangers', 'TOR': 'Toronto Blue Jays', 
            'WSN': 'Washington Nationals', 'BAL': 'Baltimore Orioles'}
    
    # teamIDs are used for generating unique player-team-IDs
    teamIDs = {'Arizona Diamondbacks': 1, 'Atlanta Braves': 2, 
            'Boston Red Sox': 4, 'Chicago Cubs': 5, 
            'Chicago White Sox': 6, 'Cincinnati Reds': 7,
            'Cleveland Indians': 8, 'Colorado Rockies': 9,
            'Detroid Tigers': 10, 'Houston Astros': 11, 
            'Kansas City Royals': 12, 'Los Angeles Angels of Anaheim': 13,
            'Los Angeles Dodgers': 14, 'Miami Marlins': 15,
            'Milwaukee Brewers': 16, 'Minnesota Twins': 17,
            'New York Mets': 18, 'New York Yankees': 19,
            'Oakland Athletics': 20, 'Philadelphia Phillies': 21, 
            'Pittsbugh Pirates': 22, 'San Diego Padres': 23,
            'San Francisco Giants': 24, 'Seattle Mariners': 25,
            'St. Louis Cardinals': 26, 'Tampa Bay Rays': 27,
            'Texas Rangers': 28, 'Toronto Blue Jays': 29, 
            'Washington Nationals': 30, 'Baltimore Orioles' : 3}
    
    # all_categories contains information about the headers of the data
    # all_categories is what the headers of our tables should be

    # all_data is the data itself
    # all_data and all_categories will both have the same keys
    # So all_data['batting'] = the 2D array of batting data
    #    all_orders['batting'] = the headers for each column of batting data
    
    all_data = {}
    all_categories = {}
    
    team_batting_categories = ["player_team_id", "runs", "at_bats", "hits", 
                        "homeruns", "runs_batted_in", "stolen_bases"]
    
    team_pitching_categories = ["player_team_id", "wins", "losses", "saves",
                          "innings_pitched", "earned_run_average", "strikeouts"]
    
    team_fielding_categories = ["player_team_id", "position", "games_played", 
                          "put_outs", "assists", "errors", "fielding_percentage"]
    
    team_info_categories = ["team_name", "record", "conference", "division", 
                          "manager"]
    
    player_categories = ['player_id', 'first_name', 'last_name', 'position',
            'bats', 'throws', 'contract_status', 'full_legal_name']

    player_team_categories = ['player_id', 'player_team_id', 'team name']

    team_batting = []
    team_pitching = []
    team_fielding = []
    team_info = []

    for team_name in resources[0]:
        print team_name

        # Obtain all tables from URL team_name
        data = scraper.parse_tables(team_name)
        

        ###########
        # BATTING #
        ###########
        
        if "team_batting" in data.keys():
            for row in data["team_batting"]:
                team_batting.append([])
                team_batting[-1].append(row["Name"])
                team_batting[-1].append(teams[team_name[6:9]])
                team_batting[-1].append(row["R"])
                team_batting[-1].append(row["AB"])
                team_batting[-1].append(row["H"])
                team_batting[-1].append(row["HR"])
                team_batting[-1].append(row["RBI"])
                team_batting[-1].append(row["SB"])
    
        ############
        # PITCHING #
        ############
       
        if "team_pitching" in data.keys():
            for row in data["team_pitching"]:
                team_pitching.append([])
                team_pitching[-1].append(row["Name"])
                team_pitching[-1].append(teams[team_name[6:9]])
                team_pitching[-1].append(row["W"])
                team_pitching[-1].append(row["L"])
                team_pitching[-1].append(row["SV"])
                team_pitching[-1].append(row["ERA"])
                team_pitching[-1].append(row["SO"])
        
        ############
        # FIELDING #
        ############
        
        if "standard_fielding" in data.keys():
            for row in data["standard_fielding"]:
                team_fielding.append([])
                team_fielding[-1].append(row["Name"])
                team_fielding[-1].append(teams[team_name[6:9]])
                team_fielding[-1].append(row["G"])
                team_fielding[-1].append(row["PO"])
                team_fielding[-1].append(row["A"])
                team_fielding[-1].append(row["E"])
                team_fielding[-1].append(row["Fld%"])
        
        # Also scrape the webpage for the team_info that is not in a table
        team_data = scraper.parse_team(team_name)
        team_info.append([teams[team_name[6:9]]] + team_data)

    # Remove any rows that contain header names rather than the info itself
    checkTableForBadRows(team_batting)
    checkTableForBadRows(team_pitching)
    checkTableForBadRows(team_fielding)
    
    ##########################################################################
    ##########################################################################

    # First, make list of players from pitching, batting and fielding tables
    # Then, make url by player name and get data

    players = []
    
    # Compile list of all players
    for batter in team_batting:
        if batter[0] not in players:
            players.append(batter[0])

    for pitcher in team_pitching:
        if pitcher[0] not in players:
            players.append(pitcher[0])

    for fielder in team_fielding:
        if fielder[0] not in players:
            players.append(fielder[0])
  

    ##################
    # Player-Team ID #
    ##################

    # The purpose of player-team-ID is to manage any mid-season trades
    # If a player appears batting for two separate teams, then both those teams
    #       will be listed with his player_id
    # So this table comes out to [player_id, [player_team_ids], [team_names]]

    playerTeamIDs = [[] for i in range(len(players))]

    # Replace player/team_name with player_team_id
    # We don't pop batter[1] so that we can reference the team_name easily
    #       It is popped after the playerTeamID for loop
    for batter in team_batting:
        batter[0] =  players.index(batter[0]) + teamIDs[batter[1]] * 2000

    for pitcher in team_pitching:
        pitcher[0] = players.index(pitcher[0]) + teamIDs[pitcher[1]] * 2000
        pitcher.pop(1)

    for fielder in team_fielding:
        fielder[0] = players.index(fielder[0]) + teamIDs[fielder[1]] * 2000
        fielder.pop(1)

    # We make the playerTeamIDs as [playerID, playerTeamIDs, teamName]
    # Example:  Bob played for the Arizona Diamondbacks
    #           Bob's playerID is just his index in the players array
    #           Bob's playerTeamIDs is the list of playerTeamIDs associated with him in the batter/pitcher/fielder tables
    #           Team Name is self explanatory
    for i in range(len(players)):
        playerTeamID = playerTeamIDs[i] # Dereference it once
        playerTeamID.append(i) # i is just the playerID
        playerTeamID.append([])
        playerTeamID.append([])
        
        # if he has several playerTeamIDs, then he was traded midseason
        for batter in team_batting:
            batterID = batter[0]
            if batterID % 2000 == i:
                playerTeamID[1].append(batterID) # If same player, append teamID
                playerTeamID[2].append(batter[1]) # ............., append teamName
        
        # if len(playerTeamID[1]) > 1:
          #   print players[i]
    
        
    # Pop team_name from batters, since playerTeamID now has team_names stored
    #       Gets rid of redundant information between tables
    for batter in team_batting:
        batter.pop(1)


    ###########
    # PLAYERS #
    ###########
    # Now that we have a list of players from batting/pitching/fielding,
    #       we go to the URL for each player to find their personal information

    # Steps:
    #   1 - Make list into matrix form so we can add more columns
    #   2 - Create url of player's data
    #   3 - Collect data and fill in rest of columns of that player's row

    badURLs = []
    allURLs = []
    count = 0
    for i in range(len(players)):
        # print progress
        if count%50 == 0 and count != 0:
            print count,
        
        # List of players into matrix form so we can append more columns
        players[i] = [players[i]]
        
        # Get first/last names
        name = name.partition(' ')
        firstName = name[0]
        if firstName == 'Name': # Bad row
            continue
        lastName = ''.join(name[2:])

        # Input player_id, firstName, and lastName 
        players[i][0] = i
        players[i] += [firstName, lastName]

        # clean up names
        firstName = removeCharacters(firstName)
        lastName = removeCharacters(lastName)
        firstInitial = lastName[0]
        
        # Now we make the url for the player's information
        url = 'players/' + firstInitial + '/'
        if len(lastName) < 5:
            url += lastName
        else:    
            url += lastName[:5]
        url += firstName[:2]

        # Check that this URL isn't already taken by another player
        urlWithNum = url + '01.shtml'
        numCount = 1
        while urlWithNum in allURLs:
            numCount += 1
            urlWithNum = url + '0' + str(numCount) + '.shtml'
        url = urlWithNum
        
        allURLs.append(url)
        url = url.lower()
        
        # Try accessing the url.  If not, print player's name.
        try:
            data = scraper.parse_names(url)
            players[i] += data
        except (KeyboardInterrupt, SystemExit): # Allow for interrupting the program
            raise
        except:
            badURLs.append([firstName, lastName])
        count += 1

    print "URLs didn't work for:", badURLs

    encodeAscii(players)
    encodeAscii(team_batting)
    encodeAscii(team_pitching)
    encodeAscii(team_fielding)
    encodeAscii(team_info)

    all_data['players'] = players
    all_categories['players'] = player_categories
    
    all_data['pitching'] = team_pitching
    all_categories['pitching'] = team_pitching_categories

    all_data['batting'] = team_batting
    all_categories['batting'] = team_batting_categories

    all_data['fielding'] = team_fielding
    all_categories['fielding'] = team_fielding_categories

    all_data['teams'] = team_info
    all_categories['teams'] = team_info_categories

    all_data['team_player_ids'] = playerTeamIDs
    all_categories['team_player_ids'] = player_team_categories
    
    ##########################################################################
    checkDataForBadRows(all_data)
    writeToCSV(all_data, all_categories)
