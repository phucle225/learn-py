import datetime
from functools import wraps
from pydantic import BaseModel
import jwt
from flask import Response, request
from app import redis, app
from internals import response, errors

cookieName = "idk-cookie"
keyJWT = "wtf-idk"
expireTime = 60 * 60 * 8


def makeSessionRedisKey(uid: str) -> str:
    return cookieName + ":" + uid


class CacheData(BaseModel):
    UID: str = ""
    TokenHash: str = ""


class CookieClaim(BaseModel):
    UID: str = ""
    CreateTime: str = datetime.datetime.utcnow().__str__()


def Set(uid: str, response: Response) -> tuple[Exception, Response]:
    claim = CookieClaim(UID=uid)
    encoded = jwt.encode(claim.dict(), keyJWT, algorithm="HS256")

    response.set_cookie(cookieName, encoded.decode(), httponly=True, max_age=expireTime, path="/")

    # save key redis
    cache = CacheData(UID=uid, TokenHash=encoded.decode())
    hkey = makeSessionRedisKey(uid)
    try:
        redis.hmset(hkey, cache.dict())
    except Exception as err:
        return err, response
    try:
        redis.expire(hkey, expireTime)
    except Exception as err:
        return err, response

    return None, response


def Middleware(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        # get cookie
        cookieData = request.cookies.get(cookieName)

        if len(cookieData) != 0:
            decode = jwt.decode(cookieData.encode(), keyJWT, algorithms="HS256")
            try:
                claim = CookieClaim(**decode)
            except Exception as err:
                app.logger.error("decode cookie error : %s", str(err))
                return response.WriteJson(dict(), 403, err)

            hkey = makeSessionRedisKey(claim.UID)
            try:
                redisData = redis.hgetall(hkey)
                temp = {key.decode(): val.decode() for key, val in redisData.items()}
                print("===> temp: ", temp)
                cache = CacheData(**temp)
            except Exception as err:
                app.logger.error("get redis error : %s", str(err))
                return response.WriteJson(dict(), 403, err)

            if cache.TokenHash != cookieData:
                return response.WriteJson(dict(), 403, errors.SessionError)

        else:
            return response.WriteJson(dict(), 403, errors.SessionError)

        return func(*args, **kwds)

    return wrapper
