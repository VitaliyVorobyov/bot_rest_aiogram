import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}')"\
                f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        try:
            await self.connector.execute(query)
        except asyncpg.exceptions.UndefinedTableError:
            create = f"CREATE TABLE IF NOT EXISTS datausers (user_id INTEGER PRIMARY KEY, user_name VARCHAR)"
            await self.connector.execute(create)
            await self.connector.execute(query)

    async def add_reserv(self, timestamp, user_id, name, number_phone, location, date, time, count_guest):
        query = f"INSERT INTO reserv "\
                f"(timestamp, user_id, name, number_phone, location, date, time, guest_count, confirm)" \
                f"VALUES ('{timestamp}', {user_id}, '{name}', '{number_phone}', '{location}', '{date}', '{time}'," \
                f" '{count_guest}', 'неподтвержден')"
        try:
            await self.connector.execute(query)
        except asyncpg.exceptions.UndefinedTableError:
            create = (f"CREATE TABLE IF NOT EXISTS reserv (timestamp VARCHAR,"
                      f" user_id INTEGER REFERENCES datausers(user_id), name VARCHAR(255), number_phone VARCHAR(255),"
                      f" location VARCHAR(255), date VARCHAR, time VARCHAR, guest_count INTEGER, confirm VARCHAR(255))")
            await self.connector.execute(create)
            await self.connector.execute(query)

    async def add_massage(self, timestamp, user_id, name, number_phone, message_text):
        query = f"INSERT INTO support (timestamp, user_id, name, number_phone, message_text)"\
                f"VALUES ('{timestamp}', {user_id}, '{name}', '{number_phone}', '{message_text}')"
        try:
            await self.connector.execute(query)
        except asyncpg.exceptions.UndefinedTableError:
            create = (f"CREATE TABLE IF NOT EXISTS support (timestamp VARCHAR,"
                      f" user_id INTEGER REFERENCES datausers(user_id), name VARCHAR(255), number_phone VARCHAR(255),"
                      f" message_text VARCHAR)")
            await self.connector.execute(create)
            await self.connector.execute(query)

    async def confirm_reserv(self, user_id, date, conf):
        query = f"UPDATE reserv SET confirm='{conf}' WHERE user_id={user_id} and date='{date}'"
        await self.connector.execute(query)

    async def create_card(self, user_id, timestamp, name, number_phone):
        query = f"INSERT INTO discount_card (timestamp, user_id, name, number_phone, discont_pesent, number_card)"\
                f"VALUES ('{timestamp}', {user_id}, '{name}', '{number_phone}', 10, {user_id})"
        try:
            await self.connector.execute(query)
        except asyncpg.exceptions.UndefinedTableError:
            create = (f"CREATE TABLE IF NOT EXISTS discount_card (timestamp VARCHAR,"
                      f" user_id INTEGER REFERENCES datausers(user_id), name VARCHAR(255), number_phone VARCHAR(255),"
                      f" discont_pesent int, visit_count int, number_card int)")
            await self.connector.execute(create)
            await self.connector.execute(query)

    async def card_info(self, user_id):
        query = f"SELECT discont_pesent FROM discount_card WHERE user_id={user_id}"
        value = await self.connector.fetchval(query)
        return value

    async def reserv_edit(self, user_id):
        query = (f"SELECT date FROM reserv WHERE user_id={user_id} "
                 f"and ((confirm='неподтвержден' or confirm='подтвержден')"
                 f"and (confirm!='отменен' or confirm!='перенесен'))")
        try:
            value = await self.connector.fetch(query)
            return value
        except asyncpg.exceptions.UndefinedTableError:
            create = (f"CREATE TABLE IF NOT EXISTS reserv (timestamp VARCHAR,"
                      f" user_id INTEGER REFERENCES datausers(user_id), name VARCHAR(255), number_phone VARCHAR(255),"
                      f" location VARCHAR(255), date VARCHAR, time VARCHAR, guest_count INTEGER, confirm VARCHAR(255))")
            await self.connector.execute(create)
            value = await self.connector.fetch(query)
            return value

    async def reserv_info(self, user_id, date):
        query = (f"SELECT date, time, location, guest_count FROM reserv"
                 f" WHERE user_id={user_id} and date='{date}'")
        try:
            value = await self.connector.fetch(query)
            return value
        except asyncpg.exceptions.UndefinedTableError:
            create = (f"CREATE TABLE IF NOT EXISTS reserv (timestamp VARCHAR,"
                      f" user_id INTEGER REFERENCES datausers(user_id), name VARCHAR(255), number_phone VARCHAR(255),"
                      f" location VARCHAR(255), date VARCHAR, time VARCHAR, guest_count INTEGER, confirm VARCHAR(255))")
            await self.connector.execute(create)
            value = await self.connector.fetch(query)
            return value
