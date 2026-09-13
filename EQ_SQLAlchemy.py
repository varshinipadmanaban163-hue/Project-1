#SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine, URL

df = pd.read_csv("project_eq_clean.csv")

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="NewTempPassword123!",
    host="localhost",
    database="earthquake_db"
)

engine = create_engine(  "mysql+pymysql://root:NewTempPassword123!@localhost:3306/earthquake_db")

print("MySQL connection created")

df.to_sql(
    name="earthquake",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data inserted successfully") ;

