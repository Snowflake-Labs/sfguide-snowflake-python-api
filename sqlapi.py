import config
import requests
import uuid
from datetime import timedelta
from flask import Blueprint, request

from api_auth import JWTGenerator
from utils import api_response, params_valid


sqlapi = Blueprint('sqlapi', __name__)
authfn = JWTGenerator(config.SNOWFLAKE_ACCOUNT, config.SNOWFLAKE_USER, config.SNOWFLAKE_PRIVATE_KEY, timedelta(59), timedelta(54)).get_token
http_session = requests.Session()
url_base = f"https://{config.SNOWFLAKE_ACCOUNT}.snowflakecomputing.com"

HEADERS = {
    "Authorization": "Bearer " + authfn(),
    "Content-Type": "application/json",
    "Snowflake-Account": config.SNOWFLAKE_ACCOUNT,
    "Accept": "application/json",
    "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT"
}


def sql2body(sql):
    result = {
        "statement": f"{sql}",
        "timeout": 60,
        "resultSetMetaData": {
            "format": "json"
        },
        "database": config.SNOWFLAKE_DATABASE,
        "schema": config.SNOWFLAKE_SCHEMA,
        "warehouse": config.SNOWFLAKE_WAREHOUSE,
        "parameters": {"query_tag": "Snowflake-Python-SQLApi"},
        }
    return result


def exec_and_fetch(sql):
    jsonBody = sql2body(sql)
    r = http_session.post(f"{url_base}/api/v2/statements?requestId={str(uuid.uuid4())}&retry=true", json=jsonBody, headers=HEADERS)
    if r.status_code == 200:
        result = r.json()['data']
        return result
    else:
        print(f"ERROR: Status code from {sql}: {r.status_code}")
        raise Exception("Invalid response from API")


@sqlapi.route("/sqlapi/trips/monthly")
@api_response
def get_trips_monthly():
    start_range = request.args.get('start_range')
    end_range = request.args.get('end_range')
    if start_range and end_range and params_valid(start_range, end_range):
        sql = f"select COUNT(*) as trip_count, MONTHNAME(starttime) as month from demo.trips where starttime between '{start_range}' and '{end_range}' group by MONTH(starttime), MONTHNAME(starttime) order by MONTH(starttime);"
        return exec_and_fetch(sql)
    sql = "select COUNT(*) as trip_count, MONTHNAME(starttime) as month from demo.trips group by MONTH(starttime), MONTHNAME(starttime) order by MONTH(starttime);"
    return exec_and_fetch(sql)


@sqlapi.route("/sqlapi/trips/day_of_week")
@api_response
def get_day_of_week():
    start_range = request.args.get('start_range')
    end_range = request.args.get('end_range')
    if start_range and end_range and params_valid(start_range, end_range):
        sql = f"select COUNT(*) as trip_count, DAYNAME(starttime) as day_of_week from demo.trips where starttime between '{start_range}' and '{end_range}' group by DAYOFWEEK(starttime), DAYNAME(starttime) order by DAYOFWEEK(starttime);"
        return exec_and_fetch(sql)
    sql = "select COUNT(*) as trip_count, DAYNAME(starttime) as day_of_week from demo.trips group by DAYOFWEEK(starttime), DAYNAME(starttime) order by DAYOFWEEK(starttime);"
    return exec_and_fetch(sql)


@sqlapi.route("/sqlapi/trips/temperature")
@api_response
def get_temperature():
    start_range = request.args.get('start_range')
    end_range = request.args.get('end_range')
    if start_range and end_range and params_valid(start_range, end_range):
        sql = f"with weather_trips as (select * from demo.trips t inner join demo.weather w on date_trunc(\"day\", t.starttime) = w.observation_date) select round(temp_avg_f, -1) as temp, count(*) as trip_count from weather_trips where starttime between '{start_range}' and '{end_range}' group by round(temp_avg_f, -1) order by round(temp_avg_f, -1) asc;"
        return exec_and_fetch(sql)
    sql = "with weather_trips as (select * from demo.trips t inner join demo.weather w on date_trunc(\"day\", t.starttime) = w.observation_date) select round(temp_avg_f, -1) as temp, count(*) as trip_count from weather_trips group by round(temp_avg_f, -1) order by round(temp_avg_f, -1) asc;"
    return exec_and_fetch(sql)