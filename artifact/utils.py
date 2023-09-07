import requests
import sqlalchemy

def read_data_from_api(url,API_KEY):
    data=[]

    for date in [{"from": "2022-08-11", "to": "2022-11-11"},{"from": "2022-11-12", "to": "2023-05-29"}]:

        PARAMS = {"from": date["from"], "to": date["to"],"APIkey":API_KEY,"league_id":"152"}

        r = requests.get(url=url, params=PARAMS)
        data = data+r.json()
    
    return data

def fix_team_names(match):
    team_name_corrections_map={
        "Newcastle":"Newcastle United",
        "Manchester Utd":"Manchester United",
        "Tottenham":"Tottenham Hotspur",
        "West Ham":"West Ham United"
    }

    if match["match_hometeam_name"] in team_name_corrections_map.keys():
        match["match_hometeam_name"] = team_name_corrections_map[match["match_hometeam_name"]]

    if match["match_awayteam_name"] in team_name_corrections_map.keys():
        match["match_awayteam_name"] = team_name_corrections_map[match["match_awayteam_name"]]
    
    return match

def extract_match_data(match):
    match_data = {
        "match_id":match["match_id"],
        "league_id":match["league_id"],
        "league_name":match["league_name"],
        "match_date":match["match_date"],
        "match_hometeam_id":match["match_hometeam_id"],
        "match_hometeam_name":match["match_hometeam_name"],
        "match_hometeam_score": 0 if match["match_hometeam_score"]=='' else match["match_hometeam_score"],
        "match_awayteam_id":match["match_awayteam_id"],
        "match_awayteam_name":match["match_awayteam_name"],
        "match_awayteam_score":0 if match["match_awayteam_score"]=='' else match["match_awayteam_score"],
        "match_round":match["match_round"],
        "match_referee":match["match_referee"]
    } 
    return match_data

def extract_goalscorer_data(match):
    matches_goals = []
    for goal in match["goalscorer"]:
        goal["match_id"]=match["match_id"]
        goal["home_scorer_id"] = 0 if goal["home_scorer_id"]=="" else goal["home_scorer_id"]
        goal["home_assist_id"]=0 if goal["home_assist_id"]=="" else goal["home_assist_id"]
        goal["away_scorer_id"]=0 if goal["away_scorer_id"]=="" else goal["away_scorer_id"]
        goal["away_assist_id"]=0 if goal["away_assist_id"]=="" else goal["away_assist_id"]
        matches_goals.append(goal)
    return matches_goals

def extract_cards_data(match):
    matches_cards=[]
    for card in match["cards"]:
        card["match_id"]=match["match_id"]
        card["home_player_id"] = 0 if card["home_player_id"]=="" else card["home_player_id"]
        card["away_player_id"]=0 if card["away_player_id"]=="" else card["away_player_id"]

        matches_cards.append(card)
    return matches_cards

def insert_data_into_db(table_name,data_list, connection):
    connection.execute(
        sqlalchemy.text(
            f"INSERT INTO {table_name} ({', '.join(list(data_list[0].keys()))}) VALUES ({', '.join([':'+x for x in list(data_list[0].keys())])})"
        ),
        data_list,
    )
    connection.commit()
