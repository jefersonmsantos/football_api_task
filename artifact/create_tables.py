import sqlalchemy
from time import sleep

def create_tables():
    sleep(35)

    engine = sqlalchemy.create_engine("mysql+pymysql://deeltask:deeltask@db:3306/deel_football_api")
    #establishing the connection
    # conn = mysql.connector.connect(
    #    user='deeltask', password='deeltask', host='127.0.0.1', database='deel_football_api', port = '3308'
    # )

    #Creating a cursor object using the cursor() method
    #cursor = conn.cursor()
    with engine.connect() as connection:
    #Dropping tables table if already exists.
        connection.execute(sqlalchemy.text("DROP TABLE IF EXISTS MATCHES"))
        connection.execute(sqlalchemy.text("DROP TABLE IF EXISTS CARDS"))
        connection.execute(sqlalchemy.text("DROP TABLE IF EXISTS GOALSCORER"))

        #Creating table as per requirement
        sql_matches ='''CREATE TABLE MATCHES(
        match_id INT,
        league_id INT,
        league_name VARCHAR(30),
        match_date DATE,
        match_hometeam_id INT,
        match_hometeam_name VARCHAR(50),
        match_hometeam_score INT,
        match_awayteam_id INT,
        match_awayteam_name VARCHAR(50),
        match_awayteam_score INT,
        match_round INT,
        match_referee VARCHAR(50)
        )'''
        connection.execute(sqlalchemy.text(sql_matches))

        sql_cards ='''CREATE TABLE CARDS(
        match_id INT,
        time VARCHAR(30),
        home_fault VARCHAR(30),
        card VARCHAR(30),
        away_fault VARCHAR(30),
        info VARCHAR(30),
        home_player_id BIGINT,
        away_player_id BIGINT,
        score_info_time VARCHAR(30)
        )'''
        connection.execute(sqlalchemy.text(sql_cards))

        sql_goalscorer ='''CREATE TABLE GOALSCORER(
        match_id INT,
        time VARCHAR(30),
        home_scorer VARCHAR(30),
        home_scorer_id BIGINT,
        home_assist VARCHAR(30),
        home_assist_id BIGINT,
        score VARCHAR(30),
        away_scorer VARCHAR(30),
        away_scorer_id BIGINT,
        away_assist VARCHAR(30),
        away_assist_id BIGINT,
        info VARCHAR(30),
        score_info_time VARCHAR(30)
        )'''
        connection.execute(sqlalchemy.text(sql_goalscorer))
    
    return "Created tables"



#Closing the connection
#conn.close()