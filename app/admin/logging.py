from app.admin import service
from app.admin import models
from app import app
import time


class Logging(service.Service):
    def Add(self, data: models.RequestAdd) -> dict:
        start = time.perf_counter()
        rep = super().Add(data)
        end = time.perf_counter()
        app.logger.info("time: %s", (end - start))
        app.logger.info("request : %s", data)
        app.logger.info("response : %s", rep)
        return rep.dict(exclude={"Err": {"err"}})

    def Login(self, data: models.RequestLogin) -> dict:
        start = time.perf_counter()
        rep = super().Login(data)
        end = time.perf_counter()
        app.logger.info("time: %s", (end - start))
        app.logger.info("request : %s", data)
        app.logger.info("response : %s", rep)
        return rep.dict(exclude={"Err": {"err"}})
