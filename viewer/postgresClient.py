# import json
import psycopg2
from datetime import datetime, timedelta, timezone

tables = ["temperature"]


class Client:
    def __init__(self):
        self.connection = psycopg2.connect(
            "dbname=iot-project \
            user=iot-project \
            password=iot-project-password \
            host=192.168.1.35 \
            port=5432"
        )
        self.cursor = self.connection.cursor()

    def getListFromFetchAll(self, querry):
        self.cursor.execute(querry)
        res = [r[0] for r in self.cursor.fetchall()]
        return res

    def getAllTables(self):
        querry = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"
        return self.getListFromFetchAll(querry)

    def getDistinctRow(self, table, column):
        querry = "SELECT DISTINCT(data->>'{}') FROM {}".format(column, table)
        return self.getListFromFetchAll(querry)

    def getDevices(self, table):
        querry = "SELECT DISTINCT(data->>'device') FROM {}".format(table)
        return self.getListFromFetchAll(querry)

    def getLocations(self, table):
        querry = "SELECT DISTINCT(data->>'location') FROM {}".format(table)
        return self.getListFromFetchAll(querry)

    def getLatestEntry(self, table):
        querry = "SELECT data FROM {} ORDER BY data->>'time' DESC LIMIT(1)".format(
            table
        )
        return self.getListFromFetchAll(querry)

    def getTimeSeries(self, table, timeInterval, location = None, device = None):
        # print("Postgres timeInterval: {}".format(timeInterval))
        if timeInterval == "3days":
            startTime = datetime.today() - timedelta(days=2)
            startTime = startTime.replace(
                hour=0, minute=0, second=0, microsecond=0
            ).astimezone(timezone.utc)
        elif timeInterval == "1week":
            startTime = datetime.today() - timedelta(days=6)
            startTime = startTime.replace(
                hour=0, minute=0, second=0, microsecond=0
            ).astimezone(timezone.utc)
        elif timeInterval == "2weeks":
            startTime = datetime.today() - timedelta(days=13)
            startTime = startTime.replace(
                hour=0, minute=0, second=0, microsecond=0
            ).astimezone(timezone.utc)
        elif timeInterval == "1month":
            startTime = datetime.today() - timedelta(weeks=3, days=6)
            startTime = startTime.replace(
                hour=0, minute=0, second=0, microsecond=0
            ).astimezone(timezone.utc)
        else:  # 1day
            startTime = (
                datetime.today()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .astimezone(timezone.utc)
            )

        querry = (
            "SELECT data->>'time', (data->>'value')::numeric FROM {} "
            "WHERE data->>'time' >= '{}' ".format(
                table, startTime.isoformat())
            )
        if not (location is None):
            querry += ("AND data->>'location' = '{}' ".format(location))
        if not (device is None):
            querry += ("AND data->>'device' = '{}' ".format(device))
        
        querry += ("ORDER BY data->>'time' DESC;")
        print(querry)
        
        self.cursor.execute(querry)
        res = self.cursor.fetchall()
        time = [r[0] for r in res]
        value = [r[1] for r in res]
        return time, value
