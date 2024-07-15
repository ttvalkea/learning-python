# start by running "fastapi dev main.py"
from fastapi import FastAPI
import httpx

import sqlite3


connection = sqlite3.connect("database.db")

cursor = connection.cursor()

app = FastAPI()

@app.get("/")
async def root():
    message = "Hellurei vaan sinne"
    return {"message": message }

@app.get("/weather")
async def weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 60.2055,
        "longitude": 24.6559,
        "current": "temperature_2m"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()
    
@app.get("/initialize-db") # TODO: Obviously db init shouldn't be done in an endpoint, especially a GET endpoint 
async def initialize_db():
    try:    
        #cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
        cursor.execute("INSERT INTO fish VALUES ('Hai', 'shark', 1)")
        cursor.execute("INSERT INTO fish VALUES ('Tonni', 'tuna', 7)")
        connection.commit()
    except Exception as e:
        return e
    return "database initialized successfully"
    
@app.get("/fish")
async def initialize_db():
    rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    return rows