from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
import db

app = FastAPI()


class CreateTempAndHumidRequest(BaseModel):
    temp: int
    humid: int


@app.get("/list-temp-and-humid")
def get_humid_and_temp():
    cursor = db.get_dict_cursor()
    cursor.execute("select * from dadn.temp_and_humid")
    return cursor.fetchall()


@app.post("/create-temp-and-humid")
def create_temp_and_humid(request: CreateTempAndHumidRequest):
    cursor = db.get_dict_cursor()
    cursor.execute("insert into dadn.temp_and_humid (humid,temp,record_time) values (%(humid)s, %(temp)s, %(record_time)s) returning *",
                   {**request.dict(), "record_time": datetime.now()})
    return cursor.fetchone()
