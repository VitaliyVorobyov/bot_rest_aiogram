import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}')"\
                f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

    async def add_reserv(self, timestamp, user_id, name, number_phone, location, date, time, count_guest):
        query = f"INSERT INTO reserv "\
                f"(timestamp, user_id, name, number_phone, location, date, time, guest_count, confirm)" \
                f"VALUES ('{timestamp}', {user_id}, '{name}', '{number_phone}', '{location}', '{date}', '{time}'," \
                f" '{count_guest}', 'неподтвержден')"
        await self.connector.execute(query)

    async def add_massage(self, time_step, user_id, name, number_phone, massage_text):
        query = f"INSERT INTO support (time_step, user_id, name, number_phone, message_text)"\
                f"VALUES ('{time_step}', {user_id}, '{name}', '{number_phone}', '{massage_text}')"
        await self.connector.execute(query)

    async def confirm_reserv(self, user_id, date, conf):
        query = f"UPDATE reserv SET confirm='{conf}' WHERE user_id={user_id} and date='{date}'"
        await self.connector.execute(query)

    async def create_card(self, user_id, timestamp, name, number_phone):
        query = f"INSERT INTO discount_card (timestamp, user_id, name, number_phone, discont_pesent, number_card)"\
                f"VALUES ('{timestamp}', {user_id}, '{name}', '{number_phone}', 10, {user_id})"
        await self.connector.execute(query)

    async def card_info(self, user_id):
        query = f"SELECT discont_pesent FROM discount_card WHERE user_id={user_id}"
        value = await self.connector.fetchval(query)
        return value

    async def reserv_edit(self, user_id):

        query = (f"SELECT date FROM reserv WHERE user_id={user_id} "
                 f"and ((confirm='неподтвержден' or confirm='подтвержден')"
                 f"and (confirm!='отменен' or confirm!='перенесен'))")
        value = await self.connector.fetch(query)
        return value

    async def reserv_info(self, user_id, date):
        query = (f"SELECT date, time, location, guest_count FROM reserv"
                 f" WHERE user_id={user_id} and date='{date}'")
        value = await self.connector.fetch(query)
        return value
