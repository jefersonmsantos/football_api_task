import requests
import sqlalchemy
import os
from utils import read_data_from_api, fix_team_names,extract_match_data,extract_goalscorer_data,extract_cards_data,insert_data_into_db

def import_data():
    url = "https://apiv3.apifootball.com/?action=get_events"
    API_KEY = os.getenv('API_KEY')

    #Get data from API Football
    data = read_data_from_api(url,API_KEY)

    matches=[]
    goalscorer = []
    cards = []

    # Extract match, cards and goalscorer data
    for match in data:
        match = fix_team_names(match)

        matches.append(extract_match_data(match))
        
        goalscorer = goalscorer+extract_goalscorer_data(match)

        cards = cards+extract_cards_data(match)

    # Insert data on database
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

    engine = sqlalchemy.create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@db:3306/deel_football_api")

    with engine.connect() as connection:
        insert_data_into_db("MATCHES",matches,connection)
        insert_data_into_db("GOALSCORER",goalscorer,connection)
        insert_data_into_db("CARDS",cards,connection)

    return "Imported data"

if __name__=="__main__":
    import_data()

