from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class CreateTempAndHumidRequest(BaseModel):
    temp: int
    humid: int


class SetFanRequest(BaseModel):
    fans: list[int]


class GetFanResponse(BaseModel):
    fans: list[int]
    timestamp: datetime


@app.get("/list-temp-and-humid")
def get_humid_and_temp():
    return MainServiceImpl.get_humid_and_temp()


@app.post("/create-temp-and-humid")
def create_temp_and_humid(request: CreateTempAndHumidRequest):
    return MainServiceImpl.create_temp_and_humid(request)


fans = [0, 0, 0]


@app.post("/set-fans")
def set_fans(request: SetFanRequest):
    return MainServiceImpl.set_fans(request)


@app.get("/get-fans")
def get_fans():
    return MainServiceImpl.get_fans()


class FakeMainService():
    def create_temp_and_humid():
        return

    def get_humid_and_temp():
        return

    def set_fans():
        return

    def get_fans():
        return


class MainServiceImpl():
    def create_temp_and_humid(request: CreateTempAndHumidRequest):
        return DatabaseFacade.create_temp_and_humid(request)

    def get_humid_and_temp():
        return DatabaseFacade.get_humid_and_temp()

    def set_fans(request: SetFanRequest):
        global fans
        fans = request.fans
        return fans

    def get_fans():
        global fans
        return GetFanResponse(fans=fans, timestamp=datetime.now())


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
