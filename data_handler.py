import pandas as pd
from dotenv import dotenv_values
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pprint import pprint

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

    def check_user_exists(self, user: dict):
        email = user.get("email")
        username = user.get("username")
        number = user.get("number")
        range_ = "formula!A1:C1"
        value_input_option = 'USER_ENTERED'
        search_params = {'username': 'user_data!B:B',
                         'email': 'user_data!C:C',
                         'phone': 'user_data!D:D'}

        # value_range_body = {'majorDimension': 'COLUMNS',
        #                     "values": [[f'=MATCH("{username}", {search_params.username})']]}

        batch_update_value_range_body = {"valueInputOption": value_input_option,
                                         "data": [{"range": "formula!A1",
                                                   'majorDimension': 'COLUMNS',
                                                   "values": [[f'=MATCH("{username}", {search_params.get("username")})']]},
                                                  {"range": "formula!B1",
                                                   'majorDimension': 'COLUMNS',
                                                   "values": [[f'=MATCH("{email}", {search_params.get("email")})']]},
                                                  {"range": "formula!C1",
                                                   'majorDimension': 'COLUMNS',
                                                   "values": [[f'=MATCH("{number}", {search_params.get("phone")})']]}
                                                  ]
                                         }

        batch_update = self.service.spreadsheets().values().batchUpdate(spreadsheetId=CONFIG.get("SPREADSHEET_ID"),
                                                                        body=batch_update_value_range_body).execute()

        pprint(batch_update)

        get_request = self.service.spreadsheets().values().get(spreadsheetId=CONFIG.get("SPREADSHEET_ID"),
                                                               range=range_).execute()
        print("Get Req:")
        pprint(get_request)

        clear_request = self.service.spreadsheets().values().clear(spreadsheetId=CONFIG.get("SPREADSHEET_ID"),
                                                                   range=range_).execute()
        print("Clear Req:")
        pprint(clear_request)

        print(get_request.get("values")[0])
        if get_request.get("values")[0]:
            return True


# dm = DataManager({"test": "response"})
