import gspread as gs
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

class GoogleAuthenticate:
    def __init__(self, credentials_path="/Users/dennisoshea/Documents/Python_Scripts/client_secret.json"):
        """
        Initializes the GoogleAuthenticate class with the path to the credentials file.

        :param credentials_path: str
            Path to the Google API credentials JSON file.
        """
        self.credentials_path = credentials_path
        self.credentials = None

    def authenticate(self, scopes, **kwargs):
        """
        Authenticates the user with the provided scopes and optional arguments.

        :param scopes: list
            List of scopes to authorize the API access.
        :param kwargs: dict
            Optional arguments to be passed during the authentication process.
        """
        self.credentials = service_account.Credentials.from_service_account_file(filename=self.credentials_path, scopes=scopes, **kwargs)

class GoogleDriveAPI(GoogleAuthenticate):
    def __init__(self):
        """
        Initializes the GoogleDriveAPI class for interacting with Google Drive API.
        """
        self.scopes = ['https://www.googleapis.com/auth/drive']
        super().__init__()
        self.authenticate(self.scopes)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def create_form(self, form_name):
        """
        Creates a new Google Form.

        :param form_name: str
            Name of the form to be created.
        :return: str
            ID of the created form.
        """
        form_metadata = {'name': form_name, 'mimeType': 'application/vnd.google-apps.form'}
        form = self.drive_service.files().create(body=form_metadata).execute()
        return form['id']

class GoogleFormsAPI(GoogleAuthenticate):
    def __init__(self):
        """
        Initializes the GoogleFormsAPI class for interacting with Google Forms API.
        """
        self.scopes = ['https://www.googleapis.com/auth/forms']
        super().__init__()
        self.forms_service = None
        self.authenticate(self.scopes)
        self.forms_service = build('forms', 'v1', credentials=self.credentials)

    def create_form_from_data(self, form_id, form_data):
        """
        Creates a new form element in an existing Google Form.

        :param form_id: str
            ID of the Google Form.
        :param form_data: list
            List of form data containing question, question type, and options.
        """
        for row in form_data:
            question, question_type, options = row
            question_body = {'title': question, 'questionType': question_type, 'options': options}
            # self.forms_service.forms().get(formId=form_id).execute()['elements'].append(question_body)
            self.forms_service.forms().get(formId=form_id).execute()

class GoogleSheetsAPI(GoogleAuthenticate):
    def __init__(self, url: str, worksheet_name='Sheet1'):
        """
        Initializes the GoogleSheetsAPI class for interacting with Google Sheets API.

        :param url: str
            URL of the Google Sheet.
        :param worksheet_name: str
            Name of the worksheet, default is 'Sheet1'.
        """
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        super().__init__()
        self.authenticate(self.scopes)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.url = url
        self.worksheet_name = worksheet_name

    def open_google_worksheet(self):
        """
        Opens the specified worksheet in the Google Sheet.
        """
        self.open_google_sheet()
        self.ws = self.sh.worksheet(self.worksheet_name)

    def open_google_sheet(self):
        """
        Opens the Google Sheet specified by the URL.
        """
        gc = gs.service_account(filename=self.credentials_path)
        self.sh = gc.open_by_url(self.url)

    def open_csv(self) -> pd.DataFrame:
        """
        Converts a Google Sheet into a Pandas DataFrame.

        :return: pd.DataFrame
            Pandas DataFrame object representing the Google Sheet.
        """
        self.open_google_worksheet()
        df = pd.DataFrame(self.ws.get_all_records())
        return df

    def new_sheet(self, worksheet: str, df: pd.DataFrame, format_sheet=True):
        """
        Creates a new sheet from a DataFrame and saves it to the Google Sheet.

        :param worksheet: str
            Title of the new sheet.
        :param df: pd.DataFrame
            DataFrame object to save.
        :param format_sheet: bool
            Whether or not to format the sheet with pre-specified formatting, default is True.
        """
        self.open_google_sheet()

        df = df.fillna('')

        self.worksheet_name = worksheet
        self.worksheet_name = self.sh.add_worksheet(title=worksheet, rows=len(df), cols=len(df.columns))

        self.worksheet_name.update([df.columns.values.tolist()] + df.values.tolist())
        if format_sheet:
            self.format(self.worksheet_name)

    def update_sheet(self, worksheet_name, df, format_sheet=True):
        """
        Updates an existing sheet with a DataFrame.

        :param worksheet_name: str
            Name of the worksheet to update.
        :param df: pd.DataFrame
            DataFrame object to save.
        :param format_sheet: bool
            Whether or not to format the sheet with pre-specified formatting, default is True.
        """
        self.open_google_sheet()

        self.worksheet_name = self.sh.worksheet(worksheet_name)
        self.worksheet_name.clear()

        df = df.fillna('')
        self.worksheet_name.update([df.columns.values.tolist()] + df.values.tolist())

        if format_sheet:
            self.format(self.worksheet_name)

    def format(self, worksheet):
        """
        Applies formatting to the specified worksheet.

        :param worksheet:
            Worksheet to format.
        """
        set_frozen(worksheet, rows=1, cols=1)
        header_format = CellFormat(
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
            textFormat=textFormat(bold=True))
        data_format = CellFormat(
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE', )
        format_cell_range(worksheet, "1", header_format)
        format_cell_range(worksheet, "F2:Z", data_format)
        set_column_width(worksheet, "A", 25)
