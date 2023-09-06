import requests
import sqlalchemy
import os

def import_data():
    url = "https://apiv3.apifootball.com/?action=get_events"
    API_KEY = os.getenv('API_KEY')
    data=[]

    for date in [{"from": "2022-08-11", "to": "2022-11-11"},{"from": "2022-11-12", "to": "2023-05-29"}]:

        PARAMS = {"from": date["from"], "to": date["to"],"APIkey":API_KEY,"league_id":"152"}

        r = requests.get(url=url, params=PARAMS)
        data = data+r.json()

    matches=[]
    goalscorer = []
    cards = []

    for match in data:

        matches.append({"match_id":match["match_id"],
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
                    "match_referee":match["match_referee"]} )
        
        for goal in match["goalscorer"]:
            goal["match_id"]=match["match_id"]
            goal["home_scorer_id"] = 0 if goal["home_scorer_id"]=="" else goal["home_scorer_id"]
            goal["home_assist_id"]=0 if goal["home_assist_id"]=="" else goal["home_assist_id"]
            goal["away_scorer_id"]=0 if goal["away_scorer_id"]=="" else goal["away_scorer_id"]
            goal["away_assist_id"]=0 if goal["away_assist_id"]=="" else goal["away_assist_id"]
            goalscorer.append(goal)

        for card in match["cards"]:
            card["match_id"]=match["match_id"]
            card["home_player_id"] = 0 if card["home_player_id"]=="" else card["home_player_id"]
            card["away_player_id"]=0 if card["away_player_id"]=="" else card["away_player_id"]

            cards.append(card)

    engine = sqlalchemy.create_engine("mysql+pymysql://deeltask:deeltask@db:3306/deel_football_api")

    with engine.connect() as connection:
        connection.execute(
            sqlalchemy.text(f"INSERT INTO MATCHES ({', '.join(list(matches[0].keys()))}) VALUES ({', '.join([':'+x for x in list(matches[0].keys())])})"),
            matches,
        )
        connection.commit()

        connection.execute(
            sqlalchemy.text(f"INSERT INTO GOALSCORER ({', '.join(list(goalscorer[0].keys()))}) VALUES ({', '.join([':'+x for x in list(goalscorer[0].keys())])})"),
            goalscorer,
        )
        connection.commit()

        connection.execute(
            sqlalchemy.text(f"INSERT INTO CARDS ({', '.join(list(cards[0].keys()))}) VALUES ({', '.join([':'+x for x in list(cards[0].keys())])})"),
            cards,
        )
        connection.commit()

    return "Imported data"

if __name__=="__main__":
    import_data()

