import pandas as pd
from dotenv import dotenv_values
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pprint import  pprint

CONFIG = dotenv_values('.env')
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
MAJOR_DIMENSIONS = "ROWS"


class DataManager:
    def __init__(self, data: dict):
        self.service = None
        self.dataFrame = None
        self.creds = None
        self.data = data
        self.sheet = None
        self.enable_service()

    def enable_service(self):
        self.creds = service_account.Credentials.from_service_account_file(filename=CONFIG.get("KEYS_FILE"),
                                                                           scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=self.creds)

    def create_spreadsheet(self):
        spreadsheet_body = {
                "properties": {
                        "title": "Price Tracker Service"
                        }
                }
        spreadsheet = self.service.spreadsheets().create(body=spreadsheet_body,
                                                         fields='spreadsheetId').execute()
        self.sheet = spreadsheet

    def get_user_data(self):
        sheet = self.service.spreadsheets()
        request = sheet.values().get(spreadsheetId=CONFIG.get("SPREADSHEET_ID"),
                                     range=CONFIG.get("USERS_RANGE"),
                                     majorDimension=MAJOR_DIMENSIONS)
        response = request.execute()
        print(response)

        values = response.get('values', [])

        if not values:
            print("No data found!")
        else:
            data = response.get("values")
            self.dataFrame = pd.DataFrame(data[1:], columns=data[0])

            self.dataFrame = self.dataFrame.astype({'Username': str, 'Email': str, 'Phone': str, 'Password': str})
            self.dataFrame['Date Added'] = pd.to_datetime(self.dataFrame['Date Added'], format='%d-%m-%Y')

            return self.dataFrame

    def add_users(self, **kwargs):
        range_ = 'user_data!A:E'
        insert_data_option = 'INSERT_ROWS'
        value_input_option = 'USER_ENTERED'

        value_range_body = {
                'majorDimension': 'COLUMNS',
                'values': [[f"{kwargs.get('date_added')}"],
                           [f"{kwargs.get('username')}"],
                           [f"{kwargs.get('email')}"],
                           [f"{kwargs.get('phone')}"],
                           [f"{kwargs.get('password')}"]]
                }

        request = self.service.spreadsheets().values().append(spreadsheetId=CONFIG.get("SPREADSHEET_ID"),
                                                              range=range_,
                                                              valueInputOption=value_input_option,
                                                              insertDataOption=insert_data_option,
                                                              body=value_range_body)
        response = request.execute()
        pprint(response)
