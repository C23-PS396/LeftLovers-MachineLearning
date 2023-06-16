#!/Users/rainataputra/6th Term/content-based_filtering/bin/python3
import psycopg2
import os
from configparser import ConfigParser
import asyncio

config_file = "database.ini"

class DbConnection():
    def __init__(self):
        self._config = ConfigParser()
        self._config.read(os.path.join(os.getcwd(), config_file))
        self._section = "postgresql"
        self._host = self._config.get(self._section, "host")
        self._port = self._config.get(self._section, "port")
        self._database = self._config.get(self._section, "database")
        self._password = self._config.get(self._section, "password")
        self._user = self._config.get(self._section, "user")
        self.lock = asyncio.Lock()
        self._conn = self._create_connection()
        self._connection_established = False
        self._connection_waiters = []
        

    async def establish_connection(self):
        await self.lock.acquire()
        try:
            if not self._connection_established:
                try:
                    self._conn = await asyncio.get_event_loop().run_in_executor(None, self._create_connection)
                    self._connection_established = True
                    for waiter in self._connection_waiters:
                        waiter.set_result(None)
                    self._connection_waiters.clear()
                except psycopg2.InterfaceError:
                    # Handle connection error here
                    self._conn = None
                    self._connection_established = False
                    raise
        finally:
            self.lock.release()

    def _create_connection(self):
        return psycopg2.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            password=self._password,
            user=self._user
        )
    
    async def execute(self, query, categories=""):
        if not self._connection_established:
            connection_waiter = asyncio.get_event_loop().create_future()
            self._connection_waiters.append(connection_waiter)
            await connection_waiter

        try:
            cursor = await self._conn.cursor()
            if categories == "":
                await cursor.execute(query)
            else:
                await cursor.execute(query, categories)
            return cursor.fetchall()
        except psycopg2.InterfaceError:
            # Handle connection error here
            await self.establish_connection()
            cursor = await self._conn.cursor()
            if categories == "":
                await cursor.execute(query)
            else:
                await cursor.execute(query, categories)
            return cursor.fetchall()



