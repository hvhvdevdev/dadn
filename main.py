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
    return MainServiceImpl.get_humid_and_temp()


@app.post("/create-temp-and-humid")
def create_temp_and_humid(request: CreateTempAndHumidRequest):
    return MainServiceImpl.create_temp_and_humid(request)


class FakeMainService():
    def create_temp_and_humid():
        return

    def get_humid_and_temp():
        return


class MainServiceImpl():
    def create_temp_and_humid(request: CreateTempAndHumidRequest):
        return DatabaseFacade.create_temp_and_humid(request)

    def get_humid_and_temp():
        return DatabaseFacade.get_humid_and_temp()


class DatabaseFacade():
    def create_temp_and_humid(request: CreateTempAndHumidRequest):
        sql = """
        insert into dadn.temp_and_humid (humid, temp, record_time)
        values (%(humid)s, %(temp)s, %(record_time)s)
        returning *
        """

        params = {
            **request.dict(),
            "record_time": datetime.now()
        }

        return db.DatabaseConnection.get_instance().execute_query(sql, params)

    def get_humid_and_temp():
        return db.DatabaseConnection.get_instance().execute_query("select * from dadn.temp_and_humid order by id desc limit 10", {})
