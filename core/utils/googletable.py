import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def login(key):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key)
    client = gspread.authorize(credentials)
    return client.open('Данные Бота')


class AddMessage:
    def __init__(self, *args):
        self.args = args

    async def add_message(self):
        sheet = spreadsheet.worksheet('Сообщения')
        sheet.append_row(list(self.args))
        return

    async def add_reserv(self):
        sheet = spreadsheet.worksheet('Резервы')
        sheet.append_row(list(self.args))
        return

    async def add_card(self):
        sheet = spreadsheet.worksheet('Карты')
        sheet.append_row(list(self.args))
        return


async def valid_card():
    sheet = spreadsheet.worksheet('Карты')
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df


spreadsheet = login('bot-prototype-397012-1218891dfee0.json')
