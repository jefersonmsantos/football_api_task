import pandas as pd
import sqlalchemy
import os

def query_and_export_data():
    engine = sqlalchemy.create_engine("mysql+pymysql://deeltask:deeltask@db:3306/deel_football_api")

    with engine.connect() as connection:

        for filename in os.listdir("queries"):
            with open("queries/"+filename) as file:
                query = sqlalchemy.text(file.read())
                final_table = pd.read_sql(query, connection)
                
                final_table.to_csv(f"files/{filename.split('.')[0]}.csv",index=False)
    
    return "Exported final files"